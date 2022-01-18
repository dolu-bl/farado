#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy
import json

from farado.logger import dlog
from farado.ui.renderer import view_renderer
from farado.ui.cookie_helper import current_session_id
from farado.general_manager_holder import gm_holder
from farado.items.issue import Issue
from farado.ui.operation_result import OperationResult
from farado.permission_manager import PermissionFlag
from farado.ui.base_view import BaseView, UiUserRestrictions, DataTableArgs



class IssuesView(BaseView):

    @cherrypy.expose
    def index(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        # TODO: issue_kind_rights
        rights = self.project_rights(user.id)

        return view_renderer["issues"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                is_create_enabled=bool(PermissionFlag.creator <= rights),
                is_delete_enabled=bool(PermissionFlag.deleter <= rights),
                )
            )

    @cherrypy.expose
    def issues_data(self, **args):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        # TODO: issue_kind_rights
        rights = self.project_rights(user.id)
        table_args = DataTableArgs(args)

        issues_count = gm_holder.meta_item_manager.items_count(Issue)
        issues = gm_holder.meta_item_manager.ordered_items(
            item_type = Issue,
            order_by = "caption" if 1 == table_args.order_column else "id",
            is_order_ascending = table_args.is_order_ascending,
            slice_start = table_args.start,
            slice_stop = table_args.start + table_args.length,
            search_value = table_args.search_value,
            search_fields = ['caption', 'id'])
        data = []
        for issue in issues:
            issue_kind = gm_holder.project_manager.issue_kind(issue.issue_kind_id)
            parent_issue = gm_holder.project_manager.issue(issue.parent_id)
            project = gm_holder.project_manager.project(issue.project_id)
            data.append({
                'id': issue.id,
                'caption': issue.caption,
                'kind': [issue.issue_kind_id, issue_kind.caption if issue_kind else '—'],
                'parent': [issue.parent_id, parent_issue.caption if parent_issue else '—'],
                'project': [issue.project_id, project.caption if project else "—"],
                'management': bool(PermissionFlag.deleter <= rights)
                })

        result = {
            "draw": table_args.draw,
            "recordsTotal": issues_count,
            "recordsFiltered": issues_count,
            "data": data,
        }
        return json.dumps(result, indent=2)

    @cherrypy.expose
    def issue(
            self,
            target_issue_id=None,
            target_issue_caption='',
            target_issue_content='',
            target_issue_project_id='',
            target_issue_parent_id='',
            issue_kind_id=None,
            **args
            ):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        # TODO: issue_kind_rights
        rights = self.project_rights(user.id)
        if PermissionFlag.watcher > rights:
            return view_renderer["403"].render()

        target_issue = gm_holder.project_manager.issue(target_issue_id)
        if not target_issue and not target_issue_caption:
            return view_renderer["404"].render()

        operation_result = None
        if target_issue_caption:
            if PermissionFlag.editor > rights:
                return view_renderer["403"].render()

            if not target_issue:
                if PermissionFlag.creator > rights:
                    return view_renderer["403"].render()
                target_issue = gm_holder.project_manager.create_issue(issue_kind_id)

            target_issue.caption = target_issue_caption
            target_issue.content = target_issue_content
            if target_issue_project_id.isdigit() and bool(int(target_issue_project_id)):
                target_issue.project_id = int(target_issue_project_id)
            if target_issue_parent_id.isdigit() and bool(int(target_issue_parent_id)):
                target_issue.parent_id = int(target_issue_parent_id)

            # Appling fields values
            for field in target_issue.fields:
                field_kind_argument = f'field_kind_{field.field_kind_id}'
                if field_kind_argument in args:
                    field.value = args[field_kind_argument]

            gm_holder.project_manager.save_item(target_issue)
            operation_result = OperationResult(caption="Issue saved", kind="success")

        return view_renderer["issue"].render(
            user=user,
            target_issue=target_issue,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                is_save_enabled=bool(PermissionFlag.editor <= rights),
                is_create_enabled=bool(PermissionFlag.creator <= rights),
                is_delete_enabled=bool(PermissionFlag.deleter <= rights),
                )
            )

    @cherrypy.expose
    def add_issue(self, issue_kind_id, parent_id=None, project_id=None):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        # TODO: issue_kind_rights
        rights = self.project_rights(user.id)
        temporary_issue = gm_holder.project_manager.create_issue(issue_kind_id)
        if parent_id:
            temporary_issue.parent_id = int(parent_id)
        if project_id:
            temporary_issue.project_id = int(project_id)

        return view_renderer["new_issue"].render(
            user=user,
            new_issue=temporary_issue,
            save_result=None,
            project_manager=gm_holder.project_manager,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id)
                )
            )

    @cherrypy.expose
    def remove_issue(self, target_issue_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        # TODO: issue_kind_rights
        rights = self.project_rights(user.id)

        gm_holder.project_manager.remove_item(Issue, target_issue_id)
        operation_result = OperationResult(caption="Issue removed", kind="success")

        return view_renderer["issues"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                is_create_enabled=bool(PermissionFlag.creator <= rights),
                is_delete_enabled=bool(PermissionFlag.deleter <= rights),
                )
            )
