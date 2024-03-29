#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy

from farado.logger import logger
from farado.ui.renderer import view_renderer
from farado.ui.cookie_helper import current_session_id
from farado.general_manager_holder import gm_holder
from farado.items.issue_kind import IssueKind
from farado.items.field_kind import FieldKind
from farado.ui.operation_result import OperationResult
from farado.ui.base_view import BaseView, UiUserRestrictions


class IssueKindsView(BaseView):

    @cherrypy.expose
    def index(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        return view_renderer["issue_kinds"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def issue_kind(
            self,
            target_issue_kind_id,
            target_issue_kind_caption=None,
            target_issue_kind_workflow_id=None,
            target_issue_kind_default_state_id=None
            ):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        target_issue_kind = gm_holder.project_manager.issue_kind(target_issue_kind_id)

        operation_result = None
        if target_issue_kind_caption:
            if not target_issue_kind:
                target_issue_kind = IssueKind()

            target_issue_kind.caption = target_issue_kind_caption
            target_issue_kind.workflow_id = int(target_issue_kind_workflow_id)
            target_issue_kind.default_state_id = int(target_issue_kind_default_state_id)
            gm_holder.project_manager.save_item(target_issue_kind)
            operation_result = OperationResult(caption="Issue kind saved", kind="success")

        return view_renderer["issue_kind"].render(
            user=user,
            target_issue_kind=target_issue_kind,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def add_issue_kind(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        return view_renderer["issue_kind"].render(
            user=user,
            target_issue_kind=None,
            save_result=None,
            project_manager=gm_holder.project_manager,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def remove_issue_kind(self, target_issue_kind_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        gm_holder.project_manager.remove_item(IssueKind, target_issue_kind_id)
        operation_result = OperationResult(caption="Issue kind removed", kind="success")

        return view_renderer["issue_kinds"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def add_field_kind(self, target_issue_kind_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        field_kind = FieldKind()
        field_kind.issue_kind_id = int(target_issue_kind_id)
        field_kind.caption = "New field kind"
        gm_holder.project_manager.save_item(field_kind)
        target_issue_kind = gm_holder.project_manager.issue_kind(target_issue_kind_id)
        operation_result = OperationResult(caption="Field kind added to issue kind", kind="success")

        return view_renderer["issue_kind"].render(
            user=user,
            target_issue_kind=target_issue_kind,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def save_field_kind(
            self,
            target_issue_kind_id,
            target_field_kind_id,
            target_field_kind_caption,
            target_field_kind_description,
            target_field_kind_value_type=0,
            target_field_kind_is_system=None,
            ):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        target_field_kind = gm_holder.project_manager.field_kind(target_field_kind_id)
        target_field_kind.caption = target_field_kind_caption
        target_field_kind.description = target_field_kind_description
        target_field_kind.value_type = int(target_field_kind_value_type)
        target_field_kind.is_system = bool(target_field_kind_is_system == 'on')
        gm_holder.project_manager.save_item(target_field_kind)
        target_issue_kind = gm_holder.project_manager.issue_kind(target_issue_kind_id)
        operation_result = OperationResult(caption="Field kind saved", kind="success")

        return view_renderer["issue_kind"].render(
            user=user,
            target_issue_kind=target_issue_kind,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def remove_field_kind(self, target_issue_kind_id, target_field_kind_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        gm_holder.project_manager.remove_item(FieldKind, target_field_kind_id)
        target_issue_kind = gm_holder.project_manager.issue_kind(target_issue_kind_id)
        operation_result = OperationResult(caption="Field kind removed form issue kind", kind="success")

        return view_renderer["issue_kind"].render(
            user=user,
            target_issue_kind=target_issue_kind,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )
