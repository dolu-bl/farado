#!/usr/bin/env python
# -*- coding: utf-8 -*-

from farado.logger import logger
from farado.config import farado_config
from farado.ui.web_service import WebService
from farado.project_manager import ProjectManager
from farado.permission_manager import PermissionManager
from farado.items.meta_item_manager import MetaItemManager
from farado.general_manager_holder import gm_holder



class Stem:
    def __init__(self):
        self.log_splash()
        logger.info('Now starting...')

        self.meta_item_manager = MetaItemManager(farado_config['database']['connection_string'])
        self.project_manager = ProjectManager()
        self.permission_manager = PermissionManager()

        gm_holder.set_meta_item_manager(self.meta_item_manager)
        gm_holder.set_project_manager(self.project_manager)
        gm_holder.set_permission_manager(self.permission_manager)

        self.web_service = WebService()
        self.project_manager.read_permanent_items()

    def run(self):
        self.web_service.run()
        logger.info('Farado finished')

    def log_splash(self):
        logger.info('''                                         ''')
        logger.info('''    _|                                   ''')
        logger.info('''   |                           |         ''')
        logger.info('''   __|   _` |   __|  _` |   _` |   _ \   ''')
        logger.info('''   |    (   |  |    (   |  (   |  (   |  ''')
        logger.info('''  _|   \__,_| _|   \__,_| \__,_| \___/   ''')
        logger.info('''                                         ''')
