#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
import time
import threading

from farado.logger import DLog
from farado.items.user import User



class PermissionManager:

    def __init__(self, session_manager, meta_item_manager):
        self.session_manager = session_manager
        self.meta_item_manager = meta_item_manager
        # self.sessions_mutex = threading.RLock()

    def login(self, username, password):
        if not username or not password:
            return False

        user = self.meta_item_manager.item_by_value(User, 'login', username)
        if not user:
            return False

        return self.session_manager.create_session(user)
