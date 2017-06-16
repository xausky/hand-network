#!/usr/bin/python3
#-*- coding: utf-8 -*-

import gi
gi.require_version('Notify', '0.7')
from gi.repository import GLib, Notify, GdkPixbuf

import os
import json
import shutil
import logging

import BackThread

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
    def __init__(self):
        Notify.init('hand-network')
        self.notification = Notify.Notification.new('Hand Network', 'Running')
        self.notification.set_image_from_pixbuf(Application.ICON_PIXBUF)
        self.notification.connect('closed', self.notification_callback)
        self.notification.show()
        config_file = open(Application.CONFIG_FILE_NAME)
        config = json.loads(config_file.read())
        config_file.close()
        self.thread = BackThread.BackThread(config['username'], config['password'])
        self.thread.start()

    def notification_callback(self, notification):
        self.quit()

    def quit(self):
        self.thread.runing = False
        self.notification.close()
        loop.quit()

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
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt as e:
        app.quit()    
