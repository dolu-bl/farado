#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy

from farado.logger import dlog
from farado.ui.renderer import view_renderer
from farado.ui.cookie_helper import current_session_id
from farado.general_manager_holder import gm_holder
from farado.items.user import User
from farado.items.user_role import UserRole
from farado.ui.operation_result import OperationResult


class UsersView:
    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        return view_renderer["users"].render(
            user=user,
            project_manager=gm_holder.project_manager)

    @cherrypy.expose
    def user(
            self,
            target_user_id,
            target_user_login=None,
            target_user_email='',
            target_user_first_name='',
            target_user_middle_name='',
            target_user_last_name='',
            target_user_password='',
            target_user_need_change_password='',
            target_user_is_blocked='',
            ):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        target_user = gm_holder.project_manager.user_by_id(target_user_id)

        operation_result = None
        if target_user_login:
            if not target_user:
                target_user = User()
            target_user.login = target_user_login
            target_user.email = target_user_email
            target_user.first_name = target_user_first_name
            target_user.middle_name = target_user_middle_name
            target_user.last_name = target_user_last_name
            target_user.need_change_password = bool(target_user_need_change_password == 'on')
            target_user.is_blocked = bool(target_user_is_blocked == 'on')
            if 0 < len(target_user_password):
                target_user.set_password(target_user_password)
            gm_holder.project_manager.save_item(target_user)
            operation_result = OperationResult(caption="User saved", kind="success")

        return view_renderer["user"].render(
            user=user,
            target_user=target_user,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result)

    @cherrypy.expose
    def add_user(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        return view_renderer["user"].render(
            user=user,
            target_user=None,
            save_result=None)

    @cherrypy.expose
    def remove_user(self, target_user_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        gm_holder.project_manager.remove_item(User, target_user_id)
        operation_result = OperationResult(caption="User removed", kind="success")

        return view_renderer["users"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result)

    @cherrypy.expose
    def add_user_role(self, target_role_id, target_user_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        target_user = gm_holder.project_manager.user_by_id(target_user_id)
        user_role = UserRole()
        user_role.role_id = int(target_role_id)
        user_role.user_id = int(target_user_id)
        gm_holder.project_manager.save_item(user_role)
        operation_result = OperationResult(caption="Role added to user", kind="success")

        return view_renderer["user"].render(
            user=user,
            target_user=target_user,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result)

    @cherrypy.expose
    def remove_user_role(self, target_user_id, target_user_role_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        target_user = gm_holder.project_manager.user_by_id(target_user_id)
        gm_holder.project_manager.remove_item(UserRole, target_user_role_id)
        operation_result = OperationResult(caption="Role removed form user", kind="success")

        return view_renderer["user"].render(
            user=user,
            target_user=target_user,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result)
