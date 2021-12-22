#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

from farado.logger import dlog
from farado.ui.renderer import view_renderer
from farado.ui.cookie_helper import current_session_id
from farado.general_manager_holder import gm_holder
from farado.items.role import Role
from farado.items.rule import Rule
from farado.ui.operation_result import OperationResult


class RolesView:
    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        return view_renderer["roles"].render(
            user=user,
            project_manager=gm_holder.project_manager)

    @cherrypy.expose
    def role(
            self,
            target_role_id,
            target_role_caption='',
            ):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        target_role=gm_holder.project_manager.role(target_role_id)

        operation_result = None
        if target_role_caption:
            if not target_role:
                target_role = Role()
            target_role.caption = target_role_caption
            gm_holder.project_manager.save_item(target_role)
            operation_result = OperationResult(caption="Role saved", kind="success")

        return view_renderer["role"].render(
            user=user,
            target_role=target_role,
            operation_result=operation_result)

    @cherrypy.expose
    def add_role(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        return view_renderer["role"].render(
            user=user,
            target_role=None,
            save_result=None)

    @cherrypy.expose
    def remove_role(self, target_role_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        gm_holder.project_manager.remove_item(Role, target_role_id)
        operation_result = OperationResult(caption="Role removed", kind="success")

        return view_renderer["roles"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result)
