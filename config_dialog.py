#!/usr/bin/env python

from gi.repository import Gtk

class ConfigDialog:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.amount_value = None

    def open_dialog(self, title, max):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('config_dialog.glade')
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog')
        self.dialog.set_transient_for(self.parent_window)
        self.label = self.builder.get_object('label')
        self.label.set_text(title)
        self.amount_scale = self.builder.get_object('amount_scale')
        self.amount_scale.set_range(1, max)

        self.dialog.run()
        return self.amount_value

    def on_cancel_button(self, widget):
        self.dialog.destroy()

    def on_ok_button(self, widget):
        self.amount_value = int(self.amount_scale.get_value())
        self.dialog.destroy()
