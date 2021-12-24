#!/usr/bin/env python
# -*- coding: utf-8 -*-

from farado.logger import dlog
from farado.items.project import Project
from farado.items.issue import Issue
from farado.items.user import User
from farado.items.role import Role
from farado.items.rule import Rule
from farado.items.user_role import UserRole
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

    def roles(self):
        return gm_holder.meta_item_manager.items(Role)

    def role(self, role_id):
        return gm_holder.meta_item_manager.item_by_id(Role, role_id)

    def rules_by_role(self, role_id):
        return gm_holder.meta_item_manager.items_by_value(Rule, "role_id", role_id)

    def rule(self, rule_id):
        return gm_holder.meta_item_manager.item_by_id(Rule, rule_id)

    def user_roles_by_user(self, user_id):
        return gm_holder.meta_item_manager.items_by_value(UserRole, "user_id", user_id)

    def roles_by_user(self, user_id):
        return gm_holder.meta_item_manager.roles_by_user(user_id)

    def user_by_id(self, id):
        if not id:
            return None
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
        is_new_item = bool(item.id == None)
        gm_holder.meta_item_manager.add_item(item)
        if is_new_item:
            if type(item) == User:
                self.users.append(item)

    def remove_item(self, item_type, item_id):
        item_id = int(item_id)
        gm_holder.meta_item_manager.delete_item_by_id(item_type, item_id)
        if item_type == User:
            self.users = [user for user in self.users if not(user.id == item_id)]
