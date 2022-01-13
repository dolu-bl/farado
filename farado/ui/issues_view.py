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

