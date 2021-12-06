#!/usr/bin/python
# -*- coding: utf-8 -*-

from farado.logger import DLog
from farado.ui.web_service import WebService
from farado.session_manager import SessionManager
from farado.permission_manager import PermissionManager
from farado.items.meta_item_manager import MetaItemManager


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
        self.meta_item_manager = MetaItemManager()
        self.web_service = WebService(self)
        self.session_manager = SessionManager()
        self.permission_manager = PermissionManager(
            self.session_manager,
            self.meta_item_manager)

    def run(self):
        self.web_service.run()
        DLog.info('Farado finished')
