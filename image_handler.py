#!/usr/bin/env python

from gi.repository import Gtk
from matplotlib.figure import Figure
from seam_carving import SeamCarving
import cv2
import numpy
import copy

class ImageHandler:
    def __init__(self):
        self.current_image = None
        self.resulted_image = None
        self.secondary_image = None
        self.original_image = None
        self.seam_carving = SeamCarving()

#################################################################
#                         Utilities                             #
    def read_image(self, img_path):
        self.img_path = img_path
        img = cv2.imread(img_path)
        return img

    def read_main_image(self, img_path):
        self.original_image = self.read_image(img_path)
        self.current_image = self.original_image
        self.resulted_image = self.current_image
        return self.set_figure(self.current_image, 'Original')

    def read_secondary_image(self, img_path):
        self.secondary_image = self.read_image(img_path)
        return self.set_figure(self.secondary_image, 'Operand')

    def set_figure(self, img, title=None):
        figure = Figure()
        ax = figure.add_subplot(111)
        try:
            ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        except:
            ax.imshow(img, 'gray')
        ax.autoscale(False)
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
        return figure

    def get_current_img_width(self):
        return list(self.current_image.shape)[1]

    def replace_current_img(self):
        self.current_image = self.resulted_image
        return self.set_figure(self.current_image, 'Current')

    def recover_original_img(self):
        self.current_image = self.original_image
        self.resulted_image = self.current_image
        return self.set_figure(self.current_image, 'Original')

    def salt_and_pepper(self):
        image_dimension = list(self.current_image.shape)[:2]
        s_vs_p = 0.5
        amount = 0.004
        noised_image = copy.copy(self.current_image)

        # Salt mode
        num_salt = numpy.ceil(amount * self.current_image.size * s_vs_p)
        coords = [numpy.random.randint(0, i - 1, int(num_salt)) for i in image_dimension]
        noised_image[coords] = 255

        # Pepper mode
        num_pepper = numpy.ceil(amount * self.current_image.size * (1. - s_vs_p))
        coords = [numpy.random.randint(0, i - 1, int(num_pepper)) for i in image_dimension]
        noised_image[coords] = 0

        self.resulted_image = noised_image
        return self.set_figure(self.resulted_image, 'Noised')

    def convert_current_to_gray(self):
        self.resulted_image = self.gray_scale(self.current_image)
        return self.set_figure(self.resulted_image, 'Gray Scale')

    def gray_scale(self, img):
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except:
            print('Image is already in gray scale')
            return img
        return gray

    def threshold(self, threshold_value, is_adaptive):
        gray_image = self.gray_scale(self.current_image)
        if is_adaptive:
            self.resulted_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            output_value = 'Adaptive'
        else:
            ret, self.resulted_image = cv2.threshold(gray_image,threshold_value,255,cv2.THRESH_BINARY)
            output_value = threshold_value
        return self.set_figure(self.resulted_image, 'Thresholding({})'.format(output_value))

    def color_extract(self, color, t):
        r, g, b = color
        lower = numpy.array([b-t, g-t, r-t])
        upper = numpy.array([b+t, g+t, r+t])

        mask = cv2.inRange(self.current_image, lower, upper)
        self.resulted_image = cv2.bitwise_and(self.current_image, self.current_image, mask=mask)

        return self.set_figure(self.resulted_image, 'Color Extraction')

    def complement(self):
        # operand1 = self.gray_scale(self.current_image)


        self.resulted_image = cv2.bitwise_not(self.current_image)
        return self.set_figure(self.resulted_image, 'Complement')

#################################################################


#################################################################
#                         Suavization                           #
    def average(self, mask_size):
        self.resulted_image = cv2.blur(self.current_image, (mask_size, mask_size))
        return self.set_figure(self.resulted_image, 'Average({})'.format(mask_size))

    def median(self, mask_size):
        if(mask_size % 2 == 0):
            mask_size += 1
        self.resulted_image = cv2.medianBlur(self.current_image, mask_size)
        return self.set_figure(self.resulted_image, 'Median({})'.format(mask_size))
#################################################################


#################################################################
#                           Atenuation                          #
    def apply_filter(self, kernel):
        kernel = numpy.asanyarray(kernel, numpy.float32)
        return  cv2.filter2D(self.current_image, -1, kernel)

    def high_pass(self):
        kernel = [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]
        self.resulted_image = self.apply_filter(kernel)
        return self.set_figure(self.resulted_image, 'Basic High Pass')

    def horizontal(self):
        kernel = [[-1,-1,-1],[2,2,2],[-1,-1,-1]]
        self.resulted_image = self.apply_filter(kernel)
        return self.set_figure(self.resulted_image, 'Horizontal')

    def vertical(self):
        kernel = [[-1,2,-1],[-1,2,-1],[-1,2,-1]]
        self.resulted_image = self.apply_filter(kernel)
        return self.set_figure(self.resulted_image, 'Vertical')

    def plus_45(self):
        kernel = [[-1,-1,2],[-1,2,-1],[2,-1,-1]]
        self.resulted_image = self.apply_filter(kernel)
        return self.set_figure(self.resulted_image, '45 Degrees')

    def minus_45(self):
        kernel = [[2,-1,-1],[-1,2,-1],[-1,-1,2]]
        self.resulted_image = self.apply_filter(kernel)
        return self.set_figure(self.resulted_image, '-45 Degrees')

    def sobel(self):
        ddepth = cv2.CV_64F

        sobel_x = cv2.Sobel(self.current_image, ddepth, 1, 0)
        sobel_y = cv2.Sobel(self.current_image, ddepth, 0, 1)

        sobel_x = cv2.convertScaleAbs(sobel_x)
        sobel_y = cv2.convertScaleAbs(sobel_y)

        self.resulted_image = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
        return self.set_figure(self.resulted_image, 'Sobel')

    def prewitt(self):
        kernel_x = [[-1,-1,-1],[0,0,0],[1,1,1]]
        kernel_y = [[-1,0,1],[-1,0,1],[-1,0,1]]

        prewitt_x = self.apply_filter(kernel_x)
        prewitt_y = self.apply_filter(kernel_y)

        self.resulted_image = cv2.addWeighted(prewitt_x, 0.5, prewitt_y, 0.5, 0)
        return self.set_figure(self.resulted_image, 'Prewitt')

    def roberts(self):
        kernel_x = [[1,0],[0,-1]]
        kernel_y = [[0,1],[-1,0]]

        roberts_x = self.apply_filter(kernel_x)
        roberts_y = self.apply_filter(kernel_y)

        self.resulted_image = cv2.addWeighted(roberts_x, 0.5, roberts_y, 0.5, 0)
        return self.set_figure(self.resulted_image, 'Roberts')
#################################################################


#################################################################
#                           Detection                           #
    def hough_line(self, threshold):
        gray_image = self.gray_scale(self.current_image)
        self.resulted_image = copy.copy(self.current_image)

        edges = cv2.Canny(gray_image,50,150,apertureSize = 3)

        lines = cv2.HoughLines(edges, 1, numpy.pi/180, threshold)

        for rho, theta in lines[0]:
            a = numpy.cos(theta)
            b = numpy.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(self.resulted_image,(x1,y1),(x2,y2),(0,0,255),1)

        return self.set_figure(self.resulted_image, "Hough Line")
#################################################################


#################################################################
#                           Operation                           #
    def union(self):
        operand1 = self.gray_scale(self.current_image)
        operand2 = self.gray_scale(self.secondary_image)

        self.resulted_image = cv2.bitwise_or(operand1, operand2)
        return self.set_figure(self.resulted_image, 'Union')

    def intersection(self):
        operand1 = self.gray_scale(self.current_image)
        operand2 = self.gray_scale(self.secondary_image)

        self.resulted_image = cv2.bitwise_and(operand1, operand2)
        return self.set_figure(self.resulted_image, 'Intersction')

    def subtraction(self):
        operand1 = self.gray_scale(self.current_image)
        operand2 = self.gray_scale(self.secondary_image)

        self.resulted_image = cv2.subtract(operand1, operand2)
        return self.set_figure(self.resulted_image, 'Subtraction')

#################################################################

    def apply_seam_carving(self, amount):
        print("Wait...")
        self.resulted_image = self.seam_carving.resize(self.current_image, amount, 0, 0)
        self.resulted_image = cv2.convertScaleAbs(self.resulted_image)
        return self.set_figure(self.resulted_image, 'Seam Carving')
