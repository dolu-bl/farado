#!/usr/bin/env python
# -*- coding: utf-8 -*-

from farado.general_manager_holder import gm_holder


class UiUserRestrictions:
    def __init__(self, **args) -> None:
        for key, value in args.items():
            setattr(self, key, value)
    def __repr__(self):
        result = '<UiUserRestrictions(\n'
        for key, value in self.__dict__.items():
            result += f'''{key}='{value}'\n'''
        result += ')>'
        return result

class BaseView:
    def __init__(self):
        # aliases
        self.check_project_rights = gm_holder.permission_manager.check_project_rights
        self.project_rights = gm_holder.permission_manager.project_rights
        self.is_admin = gm_holder.permission_manager.check_is_admin
