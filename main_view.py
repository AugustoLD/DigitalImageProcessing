#!/usr/bin/env python

from gi.repository import Gtk
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from image_handler import ImageHandler
from file_dialog import FileDialog
from threshold_dialog import ThresholdDialog
from mask_dialog import MaskDialog
from color_dialog import ColorDialog

class MainView:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('gui_pdi.glade')
        self.builder.connect_signals(self)

        self.box = self.builder.get_object('inner_box')
        self.window = self.builder.get_object('main_window')
        self.window.set_default_size(600, 400)

        self.image_handler = ImageHandler()

        self.main_canvas = FigureCanvas(self.image_handler.read_image('lena.jpg'))
        self.box.pack_start(self.main_canvas, True, True, 0)
        self.window.show_all()

    def on_delete_window(self, *args):
        Gtk.main_quit(*args)

    def on_open_file(self, widget):
        self.file_dialog = FileDialog(self.window)
        file_path = self.file_dialog.choose_file()
        if(file_path):
            self.set_main_image(self.image_handler.read_image(file_path))

    def on_thresholding(self, widget):
        self.threshold_dialog = ThresholdDialog(self.window)
        threshold_value, is_adaptive = self.threshold_dialog.open_dialog()
        if(threshold_value != None):
            gray_figure, resulted_figure = self.image_handler.threshold(threshold_value, is_adaptive)
            self.set_resulted_image(resulted_figure)
            self.middle_canvas = FigureCanvas(gray_figure)
            self.box.pack_start(self.middle_canvas, True, True, 0)
            self.window.show_all()

    def on_average(self, widget):
        self.mask_dialog = MaskDialog(self.window)
        mask_value = self.mask_dialog.open_dialog()
        if(mask_value != None):
            resulted_figure = self.image_handler.average(mask_value)
            self.set_resulted_image(resulted_figure)

    def on_median(self, widget):
        self.mask_dialog = MaskDialog(self.window)
        mask_value = self.mask_dialog.open_dialog()
        if(mask_value != None):
            resulted_figure = self.image_handler.median(mask_value)
            self.set_resulted_image(resulted_figure)

    def on_high_pass(self, widget):
        resulted_figure, resulted_image2 = self.image_handler.high_pass()
        self.set_resulted_image(resulted_figure)
        self.middle_canvas = FigureCanvas(resulted_image2)
        self.box.pack_start(self.middle_canvas, True, True, 0)
        self.window.show_all()

    def on_sobel(self, widget):
        resulted_figure = self.image_handler.sobel()
        self.set_resulted_image(resulted_figure)

    def on_color_extract(self, widget):
        self.colorDialog = ColorDialog(self.window)
        color = self.colorDialog.select()
        if color != None:
            resulted_figure = self.image_handler.color_extract(color)
            self.set_resulted_image(resulted_figure)

    def set_main_image(self, figure):
        self.remove_current_images(all=True)
        self.main_canvas = FigureCanvas(figure)
        self.box.pack_start(self.main_canvas, True, True, 0)
        self.window.show_all()

    def set_resulted_image(self, figure):
        self.remove_current_images()
        self.filtered_canvas = FigureCanvas(figure)
        self.box.pack_end(self.filtered_canvas, True, True, 0)
        self.window.show_all()

    def remove_current_images(self, all=False):
        if len(self.box.get_children()) > 2:
            self.box.remove(self.middle_canvas)
        if len(self.box.get_children()) > 1:
            self.box.remove(self.filtered_canvas)
        if all:
            self.box.remove(self.main_canvas)

if __name__ == '__main__':
    mv = MainView()
    Gtk.main()