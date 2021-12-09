#!/usr/bin/python
# -*- coding: utf-8 -*-



class GeneralManagerHolder:
    def set_meta_item_manager(self, meta_item_manager):
        self.meta_item_manager = meta_item_manager

    def set_project_manager(self, project_manager):
        self.project_manager = project_manager

    def set_permission_manager(self, permission_manager):
        self.permission_manager = permission_manager

gm_holder = GeneralManagerHolder()
