#!/usr/bin/env python

from gi.repository import Gtk

class MaskDialog:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.mask_value = None
        self.builder = Gtk.Builder()
        self.builder.add_from_file('mask_size_gui.glade')
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog')
        self.dialog.set_transient_for(self.parent_window)
        self.mask_spin = self.builder.get_object('spinbutton')

    def open_dialog(self):
        self.dialog.run()
        return self.mask_value

    def on_cancel_button(self, widget):
        self.dialog.destroy()

    def on_ok_button(self, widget):
        self.mask_spin.update()
        self.mask_value = int(self.mask_spin.get_value())
        self.dialog.destroy()
