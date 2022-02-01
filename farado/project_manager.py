#!/usr/bin/env python
# -*- coding: utf-8 -*-

from farado.items.board_column import BoardColumn
from farado.logger import dlog
from farado.items.project import Project
from farado.items.board import Board
from farado.items.issue import Issue
from farado.items.field import Field
from farado.items.user import User
from farado.items.role import Role
from farado.items.rule import Rule
from farado.items.workflow import Workflow
from farado.items.state import State
from farado.items.edge import Edge
from farado.items.issue_kind import IssueKind
from farado.items.field_kind import FieldKind, ValueTypes
from farado.items.user_role import UserRole
from farado.general_manager_holder import gm_holder
from farado.file_manager import FileManager



class ProjectManager:
    def __init__(self):
        self.users = []
        self.file_manager = FileManager()

    def read_permanent_items(self):
        self.users = gm_holder.meta_item_manager.items(User)

    def projects(self):
        return gm_holder.meta_item_manager.items(Project)

    def project(self, project_id):
        if project_id:
            return gm_holder.meta_item_manager.item_by_id(Project, project_id)
        return None

    def project_issues(self, project_id):
        if project_id:
            return gm_holder.meta_item_manager.items_by_value(Issue, "project_id", project_id)
        return None

    def boards(self):
        return gm_holder.meta_item_manager.items(Board)

    def board(self, board_id):
        if board_id:
            return gm_holder.meta_item_manager.item_by_id(Board, board_id)
        return None

    def board_columns_by_board(self, board_id):
        if board_id:
            return gm_holder.meta_item_manager.items_by_value(BoardColumn, "board_id", board_id)
        return None

    def board_columns(self):
        return gm_holder.meta_item_manager.items(BoardColumn)

    def board_column(self, board_column_id):
        if board_column_id:
            return gm_holder.meta_item_manager.item_by_id(BoardColumn, board_column_id)
        return None

    def roles(self):
        return gm_holder.meta_item_manager.items(Role)

    def role(self, role_id):
        if role_id:
            return gm_holder.meta_item_manager.item_by_id(Role, role_id)
        return None

    def rules_by_role(self, role_id):
        if role_id:
            return gm_holder.meta_item_manager.items_by_value(Rule, "role_id", role_id)
        return None

    def rule(self, rule_id):
        if rule_id:
            return gm_holder.meta_item_manager.item_by_id(Rule, rule_id)
        return None

    def user_roles_by_user(self, user_id):
        if user_id:
            return gm_holder.meta_item_manager.items_by_value(UserRole, "user_id", user_id)
        return None

    def roles_by_user(self, user_id):
        if user_id:
            return gm_holder.meta_item_manager.roles_by_user(user_id)
        return None

    def workflows(self):
        return gm_holder.meta_item_manager.items(Workflow)

    def workflow(self, workflow_id):
        if workflow_id:
            return gm_holder.meta_item_manager.item_by_id(Workflow, workflow_id)
        return None

    def states(self):
        return gm_holder.meta_item_manager.items(State)

    def state(self, state_id):
        if state_id:
            return gm_holder.meta_item_manager.item_by_id(State, state_id)
        return None

    def new_states_for_issue(self, issue_id):
        if not issue_id:
            return []
        issue = self.issue(issue_id)
        if not issue:
            return []
        issue_kind = self.issue_kind(issue.issue_kind_id)
        if not issue_kind:
            return []
        workflow = self.workflow(issue_kind.workflow_id)
        if not workflow:
            return []
        states_ids = [edge.to_state_id for edge in workflow.edges if issue.state_id == edge.from_state_id]
        return [state for state in workflow.states if state.id in states_ids]

    def edges(self):
        return gm_holder.meta_item_manager.items(Edge)

    def edge(self, edge_id):
        if edge_id:
            return gm_holder.meta_item_manager.item_by_id(Edge, edge_id)
        return None

    def issue_kinds(self):
        return gm_holder.meta_item_manager.items(IssueKind)

    def issue_kind(self, issue_kind_id):
        if issue_kind_id:
            return gm_holder.meta_item_manager.item_by_id(IssueKind, issue_kind_id)
        return None

    def field_kinds(self):
        return gm_holder.meta_item_manager.items(FieldKind)

    def field_kind(self, field_kind_id):
        if field_kind_id:
            return gm_holder.meta_item_manager.item_by_id(FieldKind, field_kind_id)
        return None

    def value_types(self):
        return ValueTypes

    def issues(self):
        return gm_holder.meta_item_manager.items(Issue)

    def issue(self, issue_id):
        if issue_id:
            return gm_holder.meta_item_manager.item_by_id(Issue, issue_id)
        return None

    def sub_issues(self, issue_id):
        if issue_id:
            return gm_holder.meta_item_manager.items_by_value(Issue, 'parent_id', issue_id)
        return []

    def parent_issues(self, parent_issue_id):
        if parent_issue_id:
            issue = gm_holder.meta_item_manager.item_by_id(Issue, parent_issue_id)
            if issue:
                return [issue] + self.parent_issues(issue.parent_id)
        return []

    def user_by_id(self, id):
        if not id:
            return None
        id = int(id)
        for user in self.users:
            if id == user.id:
                return user
        return None

    def user_by_login(self, login):
        if not login:
            return None
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

    def create_issue(self, issue_kind_id):
        issue_kind = self.issue_kind(issue_kind_id)
        if not issue_kind:
            return None

        issue = Issue()
        issue.issue_kind_id = issue_kind.id
        issue.state_id = issue_kind.default_state_id
        for field_kind in issue_kind.field_kinds:
            issue.fields.append(Field(field_kind_id=field_kind.id))
        return issue
