#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy
from cherrypy.lib.static import serve_file

import json
import uuid

from farado.logger import logger
from farado.ui.renderer import view_renderer
from farado.ui.cookie_helper import current_session_id
from farado.general_manager_holder import gm_holder
from farado.items.issue import Issue
from farado.items.file import File
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

        # TODO : order by parent, project and kind
        issues_count = gm_holder.meta_item_manager.items_count(Issue)
        issues = gm_holder.meta_item_manager.ordered_items(
            item_type = Issue,
            order_by = "caption" if 3 == table_args.order_column else "id",
            is_order_ascending = table_args.is_order_ascending,
            slice_start = table_args.start,
            slice_stop = table_args.start + table_args.length,
            search_value = table_args.search_value,
            search_fields = ['caption', 'id'])
        data = []
        for issue in issues:
            issue_kind = gm_holder.project_manager.issue_kind(issue.issue_kind_id)
            state = gm_holder.project_manager.state(issue.state_id)
            parent_issue = gm_holder.project_manager.issue(issue.parent_id)
            project = gm_holder.project_manager.project(issue.project_id)
            data.append({
                'id': issue.id,
                'kind': [issue.issue_kind_id, issue_kind.caption if issue_kind else '—'],
                'state': [issue.state_id, state.caption if state else '—'],
                'caption': issue.caption,
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
    def issue(self, target_issue_id=None, **args):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_reading = bool(len(args) == 0)

        # TODO: issue_kind_rights
        rights = self.project_rights(user.id)
        if PermissionFlag.watcher > rights:
            return view_renderer["403"].render()

        target_issue = gm_holder.project_manager.issue(target_issue_id)
        if not target_issue and is_reading:
            return view_renderer["404"].render()

        operation_result = None
        if not is_reading:
            if PermissionFlag.editor > rights:
                return view_renderer["403"].render()

            if not target_issue:
                if PermissionFlag.creator > rights:
                    return view_renderer["403"].render()
                issue_kind_id = args['issue_kind_id'] if 'issue_kind_id' in args else None
                target_issue = gm_holder.project_manager.create_issue(issue_kind_id)
                # TODO : say issue_kind not found to user
                if not target_issue and is_reading:
                    return view_renderer["404"].render()
                
                if 'issue_files_editor' in args:
                    gm_holder.project_manager.save_item(target_issue)
                    for file_data in args['issue_files_editor']:
                        file_id = str(uuid.uuid4())
                        file_path = f'issue_{target_issue.id}'
                        gm_holder.project_manager.file_manager.save_uploaded_file(
                            file_path,
                            file_id,
                            file_data.file.read())

                        target_issue.files.append(File(
                            file_data.filename,
                            file_id,
                            file_path
                        ))

            if 'issue_caption' in args:
                target_issue.caption = args['issue_caption']
            if 'issue_content' in args:
                target_issue.content = args['issue_content']

            if 'issue_project_id' in args:
                issue_project_id = args['issue_project_id']
                if issue_project_id.isdigit() and bool(int(issue_project_id)):
                    target_issue.project_id = int(issue_project_id)

            if 'issue_parent_id' in args:
                issue_parent_id = args['issue_parent_id']
                if issue_parent_id.isdigit() and bool(int(issue_parent_id)):
                    target_issue.parent_id = int(issue_parent_id)

            if 'issue_state_id' in args:
                issue_state_id = args['issue_state_id']
                if issue_state_id.isdigit() and bool(int(issue_state_id)):
                    target_issue.state_id = int(issue_state_id)

            # Clearing fields values
            for field in target_issue.fields:
                field.value = None
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

    @cherrypy.expose
    def upload(self, target_issue_id, **args):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        # TODO: issue_kind_rights
        rights = self.project_rights(user.id)

        target_issue = gm_holder.project_manager.issue(target_issue_id)
        if not target_issue:
            return view_renderer["404"].render()

        file_data = args['issue_files_editor']
        file_id = str(uuid.uuid4())
        file_path = f'issue_{target_issue_id}'
        gm_holder.project_manager.file_manager.save_uploaded_file(
            file_path,
            file_id,
            file_data.file.read())

        target_issue.files.append(File(
            file_data.filename,
            file_id,
            file_path
        ))
        gm_holder.project_manager.save_item(target_issue)

        return "{}"

    @cherrypy.expose
    def file(self, target_issue_id, file_id=None, key=None):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        # TODO: issue_kind_rights
        rights = self.project_rights(user.id)

        target_issue = gm_holder.project_manager.issue(target_issue_id)
        if not target_issue:
            return view_renderer["404"].render()

        if not file_id:
            file_id = key

        file = target_issue.file(file_id)
        if not file:
            return view_renderer["404"].render()

        file_path = gm_holder.project_manager.file_manager.file_path(file)
        return serve_file(
            file_path,
            "application/x-download",
            "attachment",
            file.caption)

    @cherrypy.expose
    def remove_file(self, target_issue_id, file_id=None, key=None):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        # TODO: issue_kind_rights
        rights = self.project_rights(user.id)

        target_issue = gm_holder.project_manager.issue(target_issue_id)
        if not target_issue:
            return view_renderer["404"].render()

        if not file_id:
            file_id = key

        file = target_issue.file(file_id)
        if not file:
            return view_renderer["404"].render()

        gm_holder.project_manager.file_manager.remove_uploaded_file(file.path, file.name)
        gm_holder.project_manager.remove_item(File, file_id)
        return "{}"
