#!/usr/bin/env python

from gi.repository import Gtk
from matplotlib.figure import Figure
import cv2
import numpy as np
import matplotlib.image as mpimg

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

    def threshold(self, threshold_value, is_automatic):
        gray_image = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        if is_automatic:
            thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        else:
            ret, thresh = cv2.threshold(gray_image,threshold_value,255,cv2.THRESH_BINARY)
        return self.set_figure(gray_image, 'Gray Scale'), self.set_figure(thresh, 'Thresholding({})'.format(threshold_value))
