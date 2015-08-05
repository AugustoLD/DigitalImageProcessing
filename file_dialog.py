#!/usr/bin/env python

from gi.repository import Gtk

class FileDialog:
    def __init__(self, parent_window):
        self.parent_window = parent_window

    def choose_file(self):
        file_path = None
        dialog = Gtk.FileChooserDialog("Please choose a file", self.parent_window,
                Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
        dialog.destroy()

        return file_path

    def add_filters(self, dialog):
        filter_image = Gtk.FileFilter()
        filter_image.set_name("Image files")
        filter_image.add_mime_type("image/*")
        dialog.add_filter(filter_image)
