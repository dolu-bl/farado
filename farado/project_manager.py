#!/usr/bin/python
# -*- coding: utf-8 -*-

from farado.logger import dlog
from farado.items.project import Project
from farado.items.issue import Issue
from farado.items.user import User
from farado.general_manager_holder import gm_holder



class ProjectManager:
    def __init__(self):
        self.users = []

    def read_permanent_items(self):
        self.users = gm_holder.meta_item_manager.items(User)

    def projects(self):
        return gm_holder.meta_item_manager.items(Project)

    def project(self, project_id):
        return gm_holder.meta_item_manager.item_by_id(Project, project_id)

    def project_issues(self, project_id):
        return gm_holder.meta_item_manager.items_by_value(Issue, "project_id", project_id)

    def user_by_id(self, id):
        id = int(id)
        for user in self.users:
            if id == user.id:
                return user
        return None

    def user_by_login(self, login):
        for user in self.users:
            if login == user.login:
                return user
        return None

    def save_item(self, item):
        if item.id in gm_holder.meta_item_manager.items_ids(type(item)):
            gm_holder.meta_item_manager.expunge_item(item)
        else:
            gm_holder.meta_item_manager.add(item)