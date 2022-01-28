#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Rule():
    def __init__(
            self,
            caption='',
            is_admin=False,
            role_id=None,
            project_id=None,
            project_rights=None,
            issue_kind_id=None,
            workflow_id=None,
            issue_rights=None,
            ):
        self.id = None
        self.caption = caption
        self.role_id = role_id
        self.is_admin = is_admin
        self.project_id = project_id
        self.project_rights = project_rights
        self.issue_kind_id = issue_kind_id
        self.workflow_id = workflow_id
        self.issue_rights = issue_rights

    def __repr__(self):
        return str(
            f'''<Rule(id='{ self.id
                }',\n caption='{ self.caption
                }',\n role_id='{ self.role_id
                }',\n is_admin='{ self.is_admin
                }',\n project_id='{ self.project_id
                }',\n project_rights='{ self.project_rights
                }',\n issue_kind_id='{ self.issue_kind_id
                }',\n workflow_id='{ self.workflow_id
                }',\n issue_rights='{ self.issue_rights
                }')>'''
            )

    def reset_properties(self, properties):
        '''
        properties example:
        {'caption': 'asdf', 'project_id': '2', 'is_admin': 'on'}
        '''
        self.is_admin = False
        self.project_rights = 0
        self.issue_rights = 0
        for key, value in properties.items():
            if key in 'caption':
                self.caption = value
            elif key in 'role_id':
                self.role_id = to_int_or_none(value)
            elif key in 'is_admin':
                self.is_admin = bool(value == "on")
            elif key in 'project_id':
                self.project_id = to_int_or_none(value)
            elif key in 'project_rights':
                self.project_rights = to_int_or_none(value)
            elif key in 'issue_kind_id':
                self.issue_kind_id = to_int_or_none(value)
            elif key in 'workflow_id':
                self.workflow_id = to_int_or_none(value)
            elif key in 'issue_rights':
                self.issue_rights = to_int_or_none(value)

def to_int_or_none(value):
    try:
        return int(value)
    except:
        return None
