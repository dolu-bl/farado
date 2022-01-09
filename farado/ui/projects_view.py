#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy
import json

from farado.logger import dlog
from farado.ui.renderer import view_renderer
from farado.ui.cookie_helper import current_session_id
from farado.general_manager_holder import gm_holder
from farado.items.project import Project
from farado.ui.operation_result import OperationResult
from farado.permission_manager import PermissionFlag
from farado.ui.base_view import BaseView, UiUserRestrictions, DataTableArgs



class ProjectsView(BaseView):

    @cherrypy.expose
    def index(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        rights = self.project_rights(user.id)

        return view_renderer["projects"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                is_create_enabled=bool(PermissionFlag.creator <= rights),
                is_delete_enabled=bool(PermissionFlag.deleter <= rights),
                )
            )

    @cherrypy.expose
    def projects_data(self, **args):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        rights = self.project_rights(user.id)
        table_args = DataTableArgs(args)

        projects_count = gm_holder.meta_item_manager.items_count(Project)
        projects = gm_holder.meta_item_manager.ordered_items(
            item_type = Project,
            order_by = "caption" if 1 == table_args.order_column else "id",
            is_order_ascending = table_args.is_order_ascending,
            slice_start = table_args.start,
            slice_stop = table_args.start + table_args.length,
            search_value = table_args.search_value,
            search_fields = ['caption', 'id'])
        data = []
        for project in projects:
            data.append({
                'id': project.id,
                'caption': project.caption,
                'management': bool(PermissionFlag.deleter <= rights)
                })

        result = {
            "draw": table_args.draw,
            "recordsTotal": projects_count,
            "recordsFiltered": projects_count,
            "data": data,
        }
        return json.dumps(result, indent=2)



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

        rights = self.project_rights(user.id, target_project_id)
        if PermissionFlag.watcher > rights:
            return view_renderer["403"].render()

        target_project = gm_holder.project_manager.project(target_project_id)
        if not target_project and not target_project_caption:
            return view_renderer["404"].render()

        operation_result = None
        if target_project_caption:
            if PermissionFlag.editor > rights:
                return view_renderer["403"].render()

            if not target_project:
                if PermissionFlag.creator > rights:
                    return view_renderer["403"].render()
                target_project = Project()

            target_project.caption = target_project_caption
            target_project.content = target_project_content
            gm_holder.project_manager.save_item(target_project)
            operation_result = OperationResult(caption="Project saved", kind="success")

        return view_renderer["project"].render(
            user=user,
            target_project=target_project,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                is_save_enabled=bool(PermissionFlag.editor <= rights),
                )
            )



    @cherrypy.expose
    def add_project(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        rights = self.project_rights(user.id)
        if PermissionFlag.creator > rights:
            return view_renderer["403"].render()

        return view_renderer["project"].render(
            user=user,
            target_project=None,
            save_result=None,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                is_save_enabled=bool(PermissionFlag.editor <= rights),
                )
            )



    @cherrypy.expose
    def remove_project(self, target_project_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        rights = self.project_rights(user.id, target_project_id)
        if PermissionFlag.deleter > rights:
            return view_renderer["403"].render()

        gm_holder.project_manager.remove_item(Project, target_project_id)
        operation_result = OperationResult(caption="Project removed", kind="success")

        return view_renderer["projects"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                is_create_enabled=bool(PermissionFlag.creator <= rights),
                is_delete_enabled=bool(PermissionFlag.deleter <= rights),
                )
            )
