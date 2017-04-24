#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib
import json
import base64
import requests
import logging
class Network():
    LOGIN_URL = 'http://192.168.211.101/portal/pws?t=li'
    BEAT_URL = 'http://192.168.211.101/portal/page/doHeartBeat.jsp'
    COMMON_HERADERS = {
    'Accept-Language': 'en-US',
    'Accept': 'text/html'
    }
    def __init__(self, username, password):
        b64Password = base64.b64encode(bytes(password,'utf8'))
        self.data = {'userName': username, 'userPwd': b64Password}

    def login(self):
        logging.info('login:%s'%(self.data))
        response = requests.post(Network.LOGIN_URL, data=self.data,
         headers=Network.COMMON_HERADERS, timeout=3)
        responseText = base64.b64decode(response.text + '==')
        responseJson = urllib.unquote(responseText.decode('utf8'))
        jsonDict = json.loads(responseJson)
        heartBeatCyc = jsonDict.get('heartBeatCyc')
        if heartBeatCyc == None:
            raise BaseException(responseJson)
        logging.info('login seccuss: %s'%(responseJson))
        self.heartBeatCyc = int(heartBeatCyc)
        self.serialNo = jsonDict.get('serialNo')
        return self.heartBeatCyc

    def beat(self):
        response = requests.post(Network.BEAT_URL, data={'serialNo': self.serialNo},
         headers=Network.COMMON_HERADERS, timeout=3)
        if response.text.find('v_failedTimes') is -1:
            raise BaseException(response.text)
