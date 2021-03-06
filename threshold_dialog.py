#!/usr/bin/env python

from gi.repository import Gtk

class ThresholdDialog:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.threshold_value = None
        self.is_adaptive = None

    def open_dialog(self, no_check_button=False):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('threshold_gui.glade')
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog')
        self.dialog.set_transient_for(self.parent_window)
        if no_check_button:
            check_button = self.builder.get_object('checkbutton')
            check_button.set_visible(False)
        self.threshold_scale = self.builder.get_object('scale')
        self.automatic_ceck_button = self.builder.get_object('checkbutton')
        self.dialog.run()
        return self.threshold_value, self.is_adaptive

    def on_cancel_button(self, widget):
        self.dialog.destroy()

    def on_ok_button(self, widget):
        self.threshold_value = int(self.threshold_scale.get_value())
        self.is_adaptive = self.automatic_ceck_button.get_active()
        self.dialog.destroy()
