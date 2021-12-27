#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy

from farado.logger import dlog
from farado.ui.renderer import view_renderer
from farado.ui.cookie_helper import current_session_id
from farado.general_manager_holder import gm_holder
from farado.items.role import Role
from farado.items.rule import Rule
from farado.ui.operation_result import OperationResult
from farado.ui.base_view import BaseView, UiUserRestrictions


class RolesView(BaseView):

    @cherrypy.expose
    def index(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        if not self.is_admin(user.id):
            return view_renderer["403"].render()

        return view_renderer["roles"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                )
            )



    @cherrypy.expose
    def role(
            self,
            target_role_id,
            target_role_caption='',
            **args,
            ):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        if not self.is_admin(user.id):
            return view_renderer["403"].render()

        target_role = gm_holder.project_manager.role(target_role_id)

        operation_result = None
        if target_role_caption:
            if not target_role:
                target_role = Role()

            # Prepare rules property values
            rules_properties = {}
            for key, value in args.items():
                key_data = key.split("_")
                rule_id = key_data[-1]
                rule_field = "_".join(key_data[1:-1])
                if not rule_id in rules_properties:
                    rules_properties[rule_id] = {}
                rules_properties[rule_id][rule_field] = value

            # Apply rules property changes
            for rule_id, properties in rules_properties.items():
                rule = gm_holder.project_manager.rule(rule_id)
                rule.reset_properties(properties)
                rule.role_id = target_role_id
                gm_holder.project_manager.save_item(rule)

            # Remove deleted rules
            for rule in gm_holder.project_manager.rules_by_role(target_role_id):
                if str(rule.id) in rules_properties:
                    continue
                gm_holder.project_manager.remove_item(Rule, rule.id)

            target_role.caption = target_role_caption
            gm_holder.project_manager.save_item(target_role)
            operation_result = OperationResult(caption="Role saved", kind="success")

        return view_renderer["role"].render(
            user=user,
            target_role=target_role,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                )
            )



    @cherrypy.expose
    def add_role(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        if not self.is_admin(user.id):
            return view_renderer["403"].render()

        return view_renderer["role"].render(
            user=user,
            target_role=None,
            project_manager=gm_holder.project_manager,
            save_result=None,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                )
            )



    @cherrypy.expose
    def remove_role(self, target_role_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        if not self.is_admin(user.id):
            return view_renderer["403"].render()

        gm_holder.project_manager.remove_item(Role, target_role_id)
        operation_result = OperationResult(caption="Role removed", kind="success")

        return view_renderer["roles"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                )
            )



    @cherrypy.expose
    def add_rule(self, target_role_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        if not self.is_admin(user.id):
            return view_renderer["403"].render()

        if not gm_holder.project_manager.role(target_role_id):
            return view_renderer["404"].render()

        rule = Rule()
        rule.role_id = target_role_id
        gm_holder.project_manager.save_item(rule)

        return view_renderer["role"].render(
            user=user,
            target_role=gm_holder.project_manager.role(target_role_id),
            project_manager=gm_holder.project_manager,
            operation_result=OperationResult(caption="Rule added", kind="success"),
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                )
            )
