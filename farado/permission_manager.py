#!/usr/bin/env python
# -*- coding: utf-8 -*-

import enum

from farado.logger import dlog
from farado.items.user import User
from farado.session_manager import SessionManager
from farado.general_manager_holder import gm_holder


class PermissionFlag(enum.IntEnum):
    none = 0
    watcher = 1
    editor = 2
    creator = 4
    deleter = 8

class PermissionManager:

    def __init__(self):
        self.session_manager = SessionManager()

    def login(self, username, password):
        if not username or not password:
            dlog.warning(f'Login failed — there are no username or password')
            return False

        user = gm_holder.project_manager.user_by_login(username)
        if not user:
            dlog.warning(f'Login failed — no such user: {username}')
            return False

        if not user.check_password(password):
            dlog.warning(f'Login failed — incorrect password for: {username}')
            return False

        session_id = self.session_manager.create_session(user)
        if session_id:
            dlog.info(f'Login success: {username} session_id: {session_id}')

        return session_id

    def logout(self, session_id):
        if not session_id:
            dlog.info(f'Logout failed — there is no session_id')
            return

        user = self.session_manager.user_by_session_id(session_id)
        if user:
            dlog.info(f'Logout user: {user.login} session_id: {session_id}')
        else:
            dlog.info(f'Logout session_id: {session_id}')

        self.session_manager.remove_session(session_id)

    def user_by_session_id(self, session_id):
        return self.session_manager.user_by_session_id(session_id)

    def project_rights(self, user_id, project_id=None):
        if project_id:
            project_id = int(project_id)
        result = 0
        for role in gm_holder.project_manager.roles_by_user(user_id):
            for rule in role.rules:
                if rule.project_id and not(rule.project_id == project_id):
                    continue
                result |= rule.project_rights
        return result

    def check_is_admin(self, user_id):
        for role in gm_holder.project_manager.roles_by_user(user_id):
            for rule in role.rules:
                if rule.is_admin:
                    return True
        return False
