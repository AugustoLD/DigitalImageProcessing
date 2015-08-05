#!/usr/bin/env python

from gi.repository import Gtk
from matplotlib.figure import Figure
import cv2
import numpy

class ImageHandler:
    def __init__(self):
        self.img = None

    def read_image(self, img_path):
        self.img = cv2.imread(img_path)
        b, g, r = cv2.split(self.img)
        self.img = cv2.merge([r,g,b])
        return self.set_figure(self.img, 'Original')

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
        amount = 0.004

        # Salt mode
        num_salt = numpy.ceil(amount * self.img.size * s_vs_p)
        coords = [numpy.random.randint(0, i - 1, int(num_salt)) for i in self.img.shape]
        self.img[coords] = 1

        # Pepper mode
        num_pepper = numpy.ceil(amount * self.img.size * (1. - s_vs_p))
        coords = [numpy.random.randint(0, i - 1, int(num_pepper)) for i in self.img.shape]
        self.img[coords] = 0

        return self.set_figure(self.img, 'Original')

    def threshold(self, threshold_value, is_adaptive):
        gray_image = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        if is_adaptive:
            resulted_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            output_value = 'Adaptive'
        else:
            ret, resulted_image = cv2.threshold(gray_image,threshold_value,255,cv2.THRESH_BINARY)
            output_value = threshold_value
        return self.set_figure(gray_image, 'Gray Scale'), self.set_figure(resulted_image, 'Thresholding({})'.format(output_value))

    def average(self, mask_size):
        resulted_image = cv2.blur(self.img, (mask_size, mask_size))
        return self.set_figure(resulted_image, 'Average({})'.format(mask_size))

    def median(self, mask_size):
        if(mask_size % 2 == 0):
            mask_size += 1
        resulted_image = cv2.medianBlur(self.img, mask_size)
        return self.set_figure(resulted_image, 'Median({})'.format(mask_size))

    def high_pass(self):
        kernel = [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]
        kernel = numpy.asanyarray(kernel, numpy.float32)

        resulted_image = cv2.filter2D(self.img, -1, kernel)
        blur = cv2.blur(self.img, (5, 5))
        resulted_image2 = cv2.subtract(self.img, blur)
        return self.set_figure(resulted_image, 'Basic High Pass'), self.set_figure(resulted_image2, 'Basic High Pass')

    def sobel(self):
        gray_image = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        ddepth = cv2.CV_64F

        sobel_x = cv2.Sobel(gray_image, ddepth, 1, 0)
        sobel_y = cv2.Sobel(gray_image, ddepth, 0, 1)

        sobel_x = cv2.convertScaleAbs(sobel_x)
        sobel_y = cv2.convertScaleAbs(sobel_y)

        resulted_image = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
        return self.set_figure(resulted_image, 'Sobel')

    def color_extract(self, color):
        r, g, b = color
        t = 100
        lower = numpy.array([r-t, g-t, b-t])
        upper = numpy.array([r+t, g+t, b+t])

        mask = cv2.inRange(self.img, lower, upper)
        resulted_image = cv2.bitwise_and(self.img, self.img, mask=mask)

        return self.set_figure(resulted_image, 'Color Extraction')
