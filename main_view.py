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
        self.builder.add_from_file('main_gui.glade')
        self.builder.connect_signals(self)

        self.box = self.builder.get_object('inner_box')
        self.window = self.builder.get_object('main_window')
        self.window.set_default_size(600, 400)

        self.image_handler = ImageHandler()

        self.main_canvas = FigureCanvas(self.image_handler.read_main_image('lena.jpg'))
        self.box.pack_start(self.main_canvas, True, True, 0)
        self.filtered_canvas = None
        self.secondary_canvas = None
        self.window.show_all()

    def set_main_image(self, figure):
        self.remove_current_images(all=True)
        self.main_canvas = FigureCanvas(figure)
        self.box.pack_start(self.main_canvas, True, True, 0)
        self.window.show_all()

    def set_resulted_image(self, figure, preserve_middle=False):
        self.remove_current_images(preserve_middle=preserve_middle)
        self.filtered_canvas = FigureCanvas(figure)
        self.box.pack_end(self.filtered_canvas, True, True, 0)
        self.window.show_all()

    def set_secondary_image(self, figure):
        self.remove_current_images()
        self.secondary_canvas = FigureCanvas(figure)
        self.box.pack_start(self.secondary_canvas, True, True, 0)
        self.window.show_all()

    def remove_current_images(self, all=False, preserve_middle=False):
        if not preserve_middle and self.secondary_canvas in self.box.get_children():
            self.box.remove(self.secondary_canvas)
        if self.filtered_canvas in self.box.get_children():
            self.box.remove(self.filtered_canvas)
        if all:
            self.box.remove(self.main_canvas)

#################################################################
#                   Signal Handlers                          #
    def on_delete_window(self, *args):
        Gtk.main_quit(*args)

    def on_open_file(self, widget):
        self.file_dialog = FileDialog(self.window)
        file_path = self.file_dialog.choose_file()
        if(file_path):
            self.set_main_image(self.image_handler.read_main_image(file_path))

    def on_salt_and_pepper(self, widget):
        resulted_figure = self.image_handler.salt_and_pepper()
        self.set_resulted_image(resulted_figure)

    def on_gray_scale(self, widget):
        resulted_figure = self.image_handler.convert_current_to_gray()
        self.set_resulted_image(resulted_figure)

    def on_replace(self, widget):
        self.set_main_image(self.image_handler.replace_current_img())

    def on_recover(self, widget):
        self.set_main_image(self.image_handler.recover_original_img())

    def on_thresholding(self, widget):
        self.threshold_dialog = ThresholdDialog(self.window)
        threshold_value, is_adaptive = self.threshold_dialog.open_dialog()
        if(threshold_value != None):
            resulted_figure = self.image_handler.threshold(threshold_value, is_adaptive)
            self.set_resulted_image(resulted_figure)

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
        resulted_figure = self.image_handler.high_pass()
        self.set_resulted_image(resulted_figure)

    def on_horizontal(self, widget):
        resulted_figure = self.image_handler.horizontal()
        self.set_resulted_image(resulted_figure)

    def on_vertical(self, widget):
        resulted_figure = self.image_handler.vertical()
        self.set_resulted_image(resulted_figure)

    def on_plus_45(self, widget):
        resulted_figure = self.image_handler.plus_45()
        self.set_resulted_image(resulted_figure)

    def on_minus_45(self, widget):
        resulted_figure = self.image_handler.minus_45()
        self.set_resulted_image(resulted_figure)

    def on_sobel(self, widget):
        resulted_figure = self.image_handler.sobel()
        self.set_resulted_image(resulted_figure)

    def on_prewitt(self, widget):
        resulted_figure = self.image_handler.prewitt()
        self.set_resulted_image(resulted_figure)

    def on_roberts(self, widget):
        resulted_figure = self.image_handler.roberts()
        self.set_resulted_image(resulted_figure)

    def on_hough_line(self, widget):
        resulted_figure = self.image_handler.hough_line()
        self.set_resulted_image(resulted_figure)

    def on_color_extract(self, widget):
        self.colorDialog = ColorDialog(self.window)
        color = self.colorDialog.select()
        if color != None:
            resulted_figure = self.image_handler.color_extract(color)
            self.set_resulted_image(resulted_figure)

    def on_operand_file(self, widget):
        file_dialog = FileDialog(self.window)
        file_path = file_dialog.choose_file()
        if(file_path):
            self.set_secondary_image(self.image_handler.read_secondary_image(file_path))

    def on_union(self, widget):
        resulted_figure = self.image_handler.union()
        self.set_resulted_image(resulted_figure, preserve_middle=True)

    def on_intersection(self, widget):
        resulted_figure = self.image_handler.intersection()
        self.set_resulted_image(resulted_figure, preserve_middle=True)

    def on_subtraction(self, widget):
        resulted_figure = self.image_handler.subtraction()
        self.set_resulted_image(resulted_figure, preserve_middle=True)

    def on_complement(self, widget):
        resulted_figure = self.image_handler.complement()
        self.set_resulted_image(resulted_figure)
#################################################################

if __name__ == '__main__':
    mv = MainView()
    Gtk.main()
