#!/usr/bin/python
# -*- coding: utf-8 -*-

from farado.logger import DLog
from farado.ui.web_service import WebService



class Stem:
    def __init__(self):
        DLog.info('''                                         ''')
        DLog.info('''    _|                                   ''')
        DLog.info('''   |                           |         ''')
        DLog.info('''   __|   _` |   __|  _` |   _` |   _ \   ''')
        DLog.info('''   |    (   |  |    (   |  (   |  (   |  ''')
        DLog.info('''  _|   \__,_| _|   \__,_| \__,_| \___/   ''')
        DLog.info('''                                         ''')
        DLog.info('Now starting...')
        self.web_service = WebService()

    def run(self):
        self.web_service.run()
        DLog.info('Farado finished')
