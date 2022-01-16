#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.util.compat import u
from farado.items.user import User
from farado.items.role import Role
from farado.items.rule import Rule
from farado.items.user_role import UserRole

from farado.items.project import Project

from farado.items.issue import Issue
from farado.items.issue_kind import IssueKind

from farado.items.field import Field
from farado.items.field_kind import FieldKind, ValueTypes

from farado.items.meta_item_manager import MetaItemManager
from farado.project_manager import ProjectManager
from farado.general_manager_holder import gm_holder

from farado.config import farado_config


def main():
    data_creator = DefaultDataCreator()
    data_creator.create_users()
    data_creator.create_issues()

class DefaultDataCreator:
    def __init__(self) -> None:
        self.meta_item_manager = MetaItemManager(farado_config['database']['connection_string'])
        self.project_manager = ProjectManager()
        gm_holder.set_meta_item_manager(self.meta_item_manager)
        gm_holder.set_project_manager(self.project_manager)
        self.add_item = self.meta_item_manager.add_item

    def create_users(self):
        user = User(
            'admin',
            'John',
            'Ivanovich',
            'Smith',
            'john.smith@ivanovich.com',
            password="admin",
        )
        self.add_item(user)

        role = Role('Administrator')
        role.rules.append(Rule(
                caption='Admin rule',
                is_admin=True
        ))
        self.add_item(role)
        self.add_item(UserRole(user_id=user.id, role_id=role.id))

    def create_issues(self):
        issue_kind = IssueKind(
            "Задача",
        )
        issue_kind.field_kinds.append(
            FieldKind(
                "Developer",
                ValueTypes.user_id,
                "Issue developer"
            )
        )
        issue_kind.field_kinds.append(
            FieldKind(
                "Field2",
                ValueTypes.integer,
                "Some integer value"
            )
        )
        self.add_item(issue_kind)

        # ====================== #
        project = Project(
            "Project caption 1",
            "Project content 1"
        )
        issue1 = self.project_manager.create_issue(issue_kind.id)
        issue1.caption = "Issue 1"
        issue1.content = "Issue content 1"
        project.issues.append(issue1)
        self.add_item(project)

        issue2 = self.project_manager.create_issue(issue_kind.id)
        issue2.caption = "Issue 2"
        issue2.content = "Issue content 2"
        issue2.parent_id = issue1.id
        project.issues.append(issue2)
        self.add_item(project)

        # ====================== #
        project2 = Project(
            "Project caption 2",
            "Project content 2"
        )
        project2.issues.append(
            Issue(
                "Issue caption 21",
                "Issue content 21"
            )
        )
        project2.issues.append(
            Issue(
                "Issue caption 22",
                "Issue content 22"
            )
        )
        self.add_item(project2)

if __name__ == '__main__':
    main()
