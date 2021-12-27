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
from farado.items.field_kind import FieldKind

from farado.items.meta_item_manager import MetaItemManager
from farado.config import farado_config



if __name__ == '__main__':
    manager = MetaItemManager(farado_config['database']['connection_string'])

    # ====================== #
    user = User(
        'admin',
        'John',
        'Ivanovich',
        'Smith',
        'john.smith@ivanovich.com',
        password="admin",
    )
    manager.add_item(user)

    role = Role('Administrator')
    role.rules.append(Rule(
            caption='Admin rule',
            is_admin=True
    ))
    manager.add_item(role)
    manager.add_item(UserRole(user_id=user.id, role_id=role.id))

    # ====================== #
    issue_kind = IssueKind(
        "Задача",
    )
    issue_kind.field_kinds.append(
        FieldKind(
            "Developer",
            "User",
            "Issue developer",
            issue_kind.id,
        )
    )
    manager.add_item(issue_kind)

    # ====================== #
    project = Project(
        "Project caption 1",
        "Project content 1"
    )
    project.issues.append(
        Issue(
            "Issue caption 1",
            "Issue content 1"
        )
    )
    manager.add_item(project)

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
    manager.add_item(project2)
