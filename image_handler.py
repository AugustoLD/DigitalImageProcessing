#!/usr/bin/env python

from gi.repository import Gtk
from matplotlib.figure import Figure
import cv2
import numpy

class ImageHandler:
    def __init__(self):
        self.img = None
        self.resulted_image = None
        self.secondary_image = None

#################################################################
#                         Utilities                             #
    def replace_img(self):
        self.img = self.resulted_image
        return self.set_figure(self.img, 'Original')

    def read_image(self, img_path):
        img = cv2.imread(img_path)
        b, g, r = cv2.split(img)
        img = cv2.merge([r,g,b])
        return img

    def read_main_image(self, img_path):
        self.img = self.read_image(img_path)
        self.resulted_image = self.img
        return self.set_figure(self.img, 'Original')

    def read_secondary_image(self, img_path):
        self.secondary_image = self.read_image(img_path)
        return self.set_figure(self.secondary_image, 'Operando')

    def set_figure(self, img, title=None):
        figure = Figure(figsize=(10,8), dpi=100)
        ax = figure.add_subplot(111)
        ax.imshow(img, 'gray')
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
        return figure

    def salt_and_pepper(self):
        s_vs_p = 0.5
        amount = 0.020

        # Salt mode
        num_salt = numpy.ceil(amount * self.img.size * s_vs_p)
        coords = [numpy.random.randint(0, i - 1, int(num_salt)) for i in self.img.shape]
        self.img[coords] = 1

        # Pepper mode
        num_pepper = numpy.ceil(amount * self.img.size * (1. - s_vs_p))
        coords = [numpy.random.randint(0, i - 1, int(num_pepper)) for i in self.img.shape]
        self.img[coords] = 0

        return self.set_figure(self.img, 'Original')

    def convert_main_to_gray(self):
        self.img = self.gray_scale(self.img)
        return self.set_figure(self.img, 'Original')

    def gray_scale(self, img):
        try:
            img = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        except:
            print('Image is already in gray scale')
        return img
#################################################################


#################################################################
#                         Simple Filters                        #
    def threshold(self, threshold_value, is_adaptive):
        gray_image = self.gray_scale(self.img)
        if is_adaptive:
            self.resulted_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            output_value = 'Adaptive'
        else:
            ret, self.resulted_image = cv2.threshold(gray_image,threshold_value,255,cv2.THRESH_BINARY)
            output_value = threshold_value
        return self.set_figure(self.resulted_image, 'Thresholding({})'.format(output_value))

    def average(self, mask_size):
        self.resulted_image = cv2.blur(self.img, (mask_size, mask_size))
        return self.set_figure(self.resulted_image, 'Average({})'.format(mask_size))

    def median(self, mask_size):
        if(mask_size % 2 == 0):
            mask_size += 1
        self.resulted_image = cv2.medianBlur(self.img, mask_size)
        return self.set_figure(self.resulted_image, 'Median({})'.format(mask_size))
#################################################################


#################################################################
#               Filters with customized masks                   #
    def apply_filter(self, kernel):
        kernel = numpy.asanyarray(kernel, numpy.float32)
        self.resulted_image = cv2.filter2D(self.img, -1, kernel)
        return self.set_figure(self.resulted_image, 'Basic High Pass')

    def high_pass(self):
        kernel = [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]
        return self.apply_filter(kernel)

    def horizontal(self):
        kernel = [[-1,-1,-1],[2,2,2],[-1,-1,-1]]
        return self.apply_filter(kernel)

    def vertical(self):
        kernel = [[-1,2,-1],[-1,2,-1],[-1,2,-1]]
        return self.apply_filter(kernel)

    def plus_45(self):
        kernel = [[-1,-1,2],[-1,2,-1],[2,-1,-1]]
        return self.apply_filter(kernel)

    def minus_45(self):
        kernel = [[2,-1,-1],[-1,2,-1],[-1,-1,2]]
        return self.apply_filter(kernel)
#################################################################


#################################################################
#                           Derivadas                           #
    def sobel(self):
        gray_image = self.gray_scale(self.img)
        ddepth = cv2.CV_64F

        sobel_x = cv2.Sobel(gray_image, ddepth, 1, 0)
        sobel_y = cv2.Sobel(gray_image, ddepth, 0, 1)

        sobel_x = cv2.convertScaleAbs(sobel_x)
        sobel_y = cv2.convertScaleAbs(sobel_y)

        self.resulted_image = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
        return self.set_figure(self.resulted_image, 'Sobel')

    def prewitt(self):
        gray_image = self.gray_scale(self.img)

        kernel_x = [[-1,-1,-1],[0,0,0],[1,1,1]]
        kernel_x = numpy.asanyarray(kernel_x, numpy.float32)
        kernel_y = [[-1,0,1],[-1,0,1],[-1,0,1]]
        kernel_y = numpy.asanyarray(kernel_y, numpy.float32)

        prewitt_x = cv2.filter2D(self.img, -1, kernel_x)
        prewitt_y = cv2.filter2D(self.img, -1, kernel_y)

        self.resulted_image = cv2.addWeighted(prewitt_x, 0.5, prewitt_y, 0.5, 0)
        return self.set_figure(self.resulted_image, 'Prewitt')

    def roberts(self):
        gray_image = self.gray_scale(self.img)

        roberts_x = [[1,0],[0,-1]]
        roberts_x = numpy.asanyarray(roberts_x, numpy.float32)
        roberts_y = [[0,1],[-1,0]]
        roberts_y = numpy.asanyarray(roberts_y, numpy.float32)

        roberts_x = cv2.filter2D(self.img, -1, roberts_x)
        roberts_y = cv2.filter2D(self.img, -1, roberts_y)

        self.resulted_image = cv2.addWeighted(roberts_x, 0.5, roberts_y, 0.5, 0)
        return self.set_figure(self.resulted_image, 'Roberts')
#################################################################

    def hough_line(self):
        gray_image = self.gray_scale(self.img)

        edges = cv2.Canny(gray_image,50,150,apertureSize = 3)

        lines = None
        lines = cv2.HoughLines(edges, 0.8, numpy.pi/180, 150)

        for rho, theta in lines[0]:
            a = numpy.cos(theta)
            b = numpy.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(self.resulted_image,(x1,y1),(x2,y2),(255,0,0),1)

        return self.set_figure(self.resulted_image, "Hough Line")

    def union(self):
        operand1 = self.gray_scale(self.img)
        operand2 = self.gray_scale(self.secondary_image)

        self.resulted_image = cv2.bitwise_or(operand1, operand2)
        return self.set_figure(self.resulted_image, 'Union')

    def intersection(self):
        operand1 = self.gray_scale(self.img)
        operand2 = self.gray_scale(self.secondary_image)

        self.resulted_image = cv2.bitwise_and(operand1, operand2)
        return self.set_figure(self.resulted_image, 'Intersction')

    def complement(self):
        operand1 = self.gray_scale(self.img)

        self.resulted_image = cv2.bitwise_not(operand1)
        return self.set_figure(self.resulted_image, 'Complement')

    def difference(self):
        operand1 = self.gray_scale(self.img)
        operand2 = self.gray_scale(self.secondary_image)

        self.resulted_image = cv2.subtract(operand1, operand2)
        return self.set_figure(self.resulted_image, 'Difference')

    def color_extract(self, color):
        r, g, b = color
        t = 100
        lower = numpy.array([r-t, g-t, b-t])
        upper = numpy.array([r+t, g+t, b+t])

        mask = cv2.inRange(self.img, lower, upper)
        self.resulted_image = cv2.bitwise_and(self.img, self.img, mask=mask)

        return self.set_figure(self.resulted_image, 'Color Extraction')
