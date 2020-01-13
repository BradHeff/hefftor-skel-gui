#!/usr/bin/env python3

from os.path import expanduser
import shutil
import signal
from gi.repository import Gtk, GdkPixbuf
import gi
import os
gi.require_version('Gtk', '3.0')

home = expanduser("~")
base_dir = os.path.dirname(os.path.realpath(__file__))
MENU_CATS = ["polybar", "herbstluftwm", "bspwm", "bashrc-latest"]


class HSApp(Gtk.Window):
    def __init__(self):
        super(HSApp, self).__init__()
        Gtk.Window.__init__(self, title="Hefftors Skel App")
        self.set_resizable(False)
        self.set_border_width(10)
        self.set_icon_from_file(os.path.join(base_dir, 'hefftorlinux.svg'))
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.connect("check_resize", self.on_check_resize)

        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = "Hefftors Skel App"
        hb.props.subtitle = "Safely skel what needs to be skeled"
        self.set_titlebar(hb)

        self.vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.vbox)

        # ===========================================
        #				HEADER Section
        # ===========================================
        self.listviewHDR = Gtk.ListBox()
        self.listviewHDR.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listviewHDR, True, True, 0)

        # ListRow 1
        self.listRowHDR = Gtk.ListBoxRow()
        self.hboxHDR = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRowHDR.add(self.hboxHDR)

        self.pixbuf = GdkPixbuf.Pixbuf().new_from_file(
            os.path.join(base_dir, 'logo.png'))
        self.image = Gtk.Image().new_from_pixbuf(self.pixbuf)
        self.image_area = Gtk.Box()
        self.image_area.add(self.image)
        self.image_area.show_all()

        self.hboxHDR.pack_start(self.image_area, True, True, 0)
        self.listviewHDR.add(self.listRowHDR)

        # ===========================================
        #				First Section
        # ===========================================
        self.listview1 = Gtk.ListBox()
        self.listview1.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview1, True, True, 0)

        # ListRow 1
        self.listRow1 = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow1.add(self.hbox1)

        # ListRow 1 Elements
        self.label1 = Gtk.Label(xalign=0)
        self.label1.set_text("Category")
        self.cat = Gtk.ComboBoxText()
        for CATS in MENU_CATS:
            self.cat.append_text(CATS)
        self.cat.set_active(0)
        self.cat.set_size_request(170, 0)

        self.hbox1.pack_start(self.label1, True, True, 0)
        self.hbox1.pack_end(self.cat, False, True, 0)
        self.listview1.add(self.listRow1)

        # ===========================================
        #				Second Section
        # ===========================================
        self.listview2 = Gtk.ListBox()
        self.listview2.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview2, True, True, 0)

        # ListRow 1
        self.listRow2 = Gtk.ListBoxRow()
        self.hbox2 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow2.add(self.hbox2)

        # ListRow 1 Elements
        self.label2 = Gtk.Label(xalign=0)
        self.label2.set_text("Created By Brad Heffernan")
        self.btn2 = Gtk.Button(label="Run")
        self.btn2.connect("clicked", self.on_button_fetch_clicked)

        self.hbox2.pack_start(self.label2, True, True, 0)
        self.hbox2.pack_end(self.btn2, False, False, 0)
        self.listview2.add(self.listRow2)

    def resizeImage(self, x, y):
        pixbuf = self.pixbuf.scale_simple(x, y,
                                          GdkPixbuf.InterpType.BILINEAR)
        self.image.set_from_pixbuf(pixbuf)

    def on_check_resize(self, window):
        boxAllocation = self.hboxHDR.get_allocation()
        self.image_area.set_allocation(boxAllocation)
        self.resizeImage(boxAllocation.width,
                         boxAllocation.height)

    def on_button_fetch_clicked(self, widget):
        if self.cat.get_active_text() == "polybar":
            copytree('/etc/skel/.config/polybar/',
                     home + '/.config/polybar/')
            print("Path copied")
            ecode = 0
        elif self.cat.get_active_text() == "herbstluftwm":
            copytree('/etc/skel/.config/herbstluftwm/',
                     home + '/.config/herbstluftwm/')
            print("Path copied")
            ecode = 0
        elif self.cat.get_active_text() == "bspwm":
            copytree('/etc/skel/.config/bspwm/', home + '/.config/bspwm/')
            print("Path copied")
            ecode = 0
        elif self.cat.get_active_text() == "bashrc-latest":
            newPath = shutil.copy(
                '/etc/skel/.bashrc-latest', home + "/.bashrc-latest")
            print("Path of copied file : ", newPath)
            ecode = 0

        if(ecode == 1):
            self.callBox(1)
        else:
            self.callBox(0)

    def callBox(self, errorCode):
        if errorCode == 0:
            message = "Skel executed successfully."
            title = "Success!!"
        else:
            title = "Error!!"
            message = "Seems the terminal selected is incorrect or the command input is not properly coded for your terminals excecution option."

        md = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO,
                               buttons=Gtk.ButtonsType.OK, text=title)
        md.format_secondary_text(message)
        md.run()
        md.destroy()
        # self.set_sensitive(True)


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
            except Exception as e:
                print(e)
                ecode = 1
                os.unlink(d)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!\nFreechoice Menu GUI is Closing.')
    Gtk.main_quit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    window = HSApp()
    window.show_all()
    Gtk.main()
