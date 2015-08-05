#!/usr/bin/env python

from gi.repository import Gtk

class ColorDialog:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.color = None

    def select(self):
        self.dialog = Gtk.ColorChooserDialog('Select a color', self.parent_window)
        self.dialog.set_use_alpha(False)

        response = self.dialog.run()
        if response == -5:
            self.color = self.convert_color_to_rgb(self.dialog.get_rgba())
        self.dialog.destroy()

        return self.color

    def convert_color_to_rgb(self, gdk_color):
        rgb_color = gdk_color.to_string().rstrip(')').lstrip('rgb(')
        rgb_color = [int(color) for color in rgb_color.split(',')]

        return rgb_color
