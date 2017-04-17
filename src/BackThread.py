#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import time
import json
import logging
import threading

import requests
import HandNetwork


class BackThread(threading.Thread):
    '''
    Hand network back group thread
    '''
    def __init__(self, username, password):
        threading.Thread.__init__(self)
        self.runing = True
        self.username = username
        self.password = password
        self.network = HandNetwork.Network(self.username, self.password)
        self.cyc = 0
        self.beat_count = sys.maxint
        self.fetch_count = sys.maxint
    def __check(self):
        if self.fetch_count >= 10000:
            self.fetch_count = 0
            response = requests.get('http://ip.taobao.com/service/getIpInfo.php', timeout=3)
            if json.loads(response.text).get('code') != 1:
                raise BaseException(response.text)
    def __join_login(self):
        while self.runing:
            try:
                self.cyc = self.network.login() * 0.8
                return
            except:
                logging.exception('retry login fail')
    def run(self):
        while self.runing:
            time.sleep(1)
            self.fetch_count += 1000
            self.beat_count += 1000
            if self.fetch_count >= 10000:
                self.fetch_count = 0
                try:
                    self.__check()
                except:
                    logging.exception('fetch fail')
                    logging.info('retry login.')
                    self.__join_login()
            if self.beat_count >= self.cyc:
                self.beat_count = 0
                try:
                    self.network.beat()
                except:
                    logging.exception('beat fail')
                    logging.info('retry login.')
                    self.__join_login()
        logging.warn('thread exit')
