#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy

from farado.logger import dlog
from farado.ui.renderer import view_renderer
from farado.ui.cookie_helper import current_session_id
from farado.general_manager_holder import gm_holder
from farado.items.project import Project
from farado.ui.operation_result import OperationResult
from farado.permission_manager import PermissionFlag
from farado.ui.base_view import BaseView



class ProjectsView(BaseView):
    @cherrypy.expose
    def index(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        return view_renderer["projects"].render(
            user=user,
            project_manager=gm_holder.project_manager)

    @cherrypy.expose
    def project(
            self,
            target_project_id,
            target_project_caption='',
            target_project_content='',
            ):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        if not self.check_project_rights(user.id, PermissionFlag.watcher, target_project_id):
            return view_renderer["403"].render()

        target_project=gm_holder.project_manager.project(target_project_id)

        operation_result = None
        if target_project_caption:
            if not self.check_project_rights(user.id, PermissionFlag.editor, target_project_id):
                return view_renderer["403"].render()
            if not target_project:
                if not self.check_project_rights(user.id, PermissionFlag.creator):
                    return view_renderer["403"].render()
                target_project = Project()
            target_project.caption = target_project_caption
            target_project.content = target_project_content
            gm_holder.project_manager.save_item(target_project)
            operation_result = OperationResult(caption="Project saved", kind="success")

        return view_renderer["project"].render(
            user=user,
            target_project=target_project,
            operation_result=operation_result)

    @cherrypy.expose
    def add_project(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        if not self.check_project_rights(user.id, PermissionFlag.creator):
            return view_renderer["403"].render()

        return view_renderer["project"].render(
            user=user,
            target_project=None,
            save_result=None)

    @cherrypy.expose
    def remove_project(self, target_project_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        if not self.check_project_rights(user.id, PermissionFlag.deleter):
            return view_renderer["403"].render()

        gm_holder.project_manager.remove_item(Project, target_project_id)
        operation_result = OperationResult(caption="Project removed", kind="success")

        return view_renderer["projects"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result)
