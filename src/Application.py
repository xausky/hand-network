#!/usr/bin/python3
#-*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

import os
import json
import shutil
import logging

import BackThread

class AboutDialog(Gtk.AboutDialog):
    def __init__(self):
        Gtk.AboutDialog.__init__(self)
        self.set_logo(Application.LOGO_PIXBUF)
        self.set_program_name('Hand Network Login')
        self.set_version('1.0')
        self.set_authors(['YangNan.Shi'])
        self.set_comments('The application can auto login hand-china company network.')
class Application:
    HOME = os.getenv('HOME')
    PREFIX = os.getenv('HAND_NETWORK_PREFIX','share')
    CONFIG_DIR = HOME + '/.config/hand-network'
    CONFIG_FILE_NAME = CONFIG_DIR + '/config.json'
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if not os.path.exists(CONFIG_FILE_NAME):
        shutil.copy(PREFIX + '/config.json', CONFIG_FILE_NAME)
    ICON_PIXBUF = GdkPixbuf.Pixbuf.new_from_file(PREFIX + '/icon.png')
    LOGO_PIXBUF = GdkPixbuf.Pixbuf.new_from_file(PREFIX + '/logo.png')
    def __init__(self):
        self.icon = Gtk.StatusIcon()
        self.icon.set_from_pixbuf(Application.ICON_PIXBUF)
        self.icon.connect("popup-menu", self.right_click_event)
        self.icon.connect("activate", self.show_about_dialog)

        self.menu = Gtk.Menu()
        about = Gtk.MenuItem()
        about.set_label("About")
        about.connect("activate", self.show_about_dialog)
        self.menu.append(about)
        quit = Gtk.MenuItem()
        quit.set_label("Quit")
        quit.connect("activate", self.quit)
        self.menu.append(quit)
        self.menu.show_all()
        config_file = open(Application.CONFIG_FILE_NAME)
        config = json.loads(config_file.read())
        config_file.close()
        self.thread = BackThread.BackThread(config['username'], config['password'])
        self.thread.start()

    def right_click_event(self, icon, button, time):
        self.menu.popup(None, None, None, icon, button, time)

    def quit(self, widget):
        Gtk.main_quit()
        self.thread.runing = False

    def show_about_dialog(self, widget):
        about = AboutDialog()
        about.run()
        about.destroy()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='/tmp/hand-network.log',
                filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)
    app = Application()
    Gtk.main()
