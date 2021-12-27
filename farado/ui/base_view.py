#!/usr/bin/env python
# -*- coding: utf-8 -*-

from farado.general_manager_holder import gm_holder



class BaseView:
    def __init__(self):
        # aliases
        self.check_project_rights = gm_holder.permission_manager.check_project_rights
