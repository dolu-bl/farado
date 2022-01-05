#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

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
        self.project_rights = gm_holder.permission_manager.project_rights
        self.is_admin = gm_holder.permission_manager.check_is_admin

class DataTableArgs:
    def __init__(self, args) -> None:
        self._args = args

        self.draw = 1
        if 'draw' in args:
            self.draw = int(args['draw'])

        self.start = 0
        if 'start' in args:
            self.start = int(args['start'])

        self.length = 10
        if 'length' in args:
            self.length = int(args['length'])

        self.search_value = ''
        if 'search[value]' in args:
            self.search_value = str(args['search[value]'])

    def __repr__(self):
        return json.dumps(self._args, indent=2)
