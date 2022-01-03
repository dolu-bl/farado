#!/usr/bin/env python
# -*- coding: utf-8 -*-

import enum

class ValueTypes(enum.IntEnum):
    string = 0
    markdown_text = 1
    integer = 2
    float = 3
    bool = 4
    date_time = 5
    uri = 6
    # reserved
    issue_id = 100
    user_id = 101
    project_id = 102
    workflow_id = 103

class FieldKind():
    def __init__(
            self,
            caption='',
            value_type=ValueTypes.string,
            description='',
            issue_kind_id=None,
            is_system=False,
            ):
        self.id = None
        self.caption = caption
        self.value_type = value_type
        self.description = description
        self.issue_kind_id = issue_kind_id
        self.is_system = is_system

    def __repr__(self):
        return str(
            f'''<FieldKind(id='{ self.id
                }',\n caption='{ self.caption
                }',\n value_type='{ self.value_type
                }',\n description='{ self.description
                }',\n issue_kind_id='{ self.issue_kind_id
                }',\n is_system='{ self.is_system
                }')>'''
            )
