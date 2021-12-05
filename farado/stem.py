#!/usr/bin/python
# -*- coding: utf-8 -*-

from farado.logger import DLog
from farado.ui import Ui



class Stem:
    def __init__(self):
        DLog.info('Now starting Farado...')
        self.ui = Ui()

    def run(self):
        self.ui.run()
        DLog.info('Farado finished')
