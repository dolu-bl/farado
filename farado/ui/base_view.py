#!/usr/bin/env python
# -*- coding: utf-8 -*-

from farado.general_manager_holder import gm_holder


class UiUserRestrictions:
    def __init__(
            self,
            is_admin=False,
            primary_action_enabled=False,
            secondary_action_enabled=False,
            third_action_enabled=False,
            ) -> None:
        self.is_admin = is_admin
        self.primary_action_enabled = primary_action_enabled
        self.secondary_action_enabled = secondary_action_enabled
        self.third_action_enabled = third_action_enabled

class BaseView:
    def __init__(self):
        # aliases
        self.check_project_rights = gm_holder.permission_manager.check_project_rights
        self.project_rights = gm_holder.permission_manager.project_rights
        self.is_admin = gm_holder.permission_manager.check_is_admin
