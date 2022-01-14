#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Issue():
    def __init__(
            self,
            caption=None,
            content=None,
            issue_kind_id=None,
            parent_id=None,
            project_id=None):
        self.id = None
        self.caption = caption
        self.content = content
        self.issue_kind_id = issue_kind_id
        self.parent_id = parent_id
        self.project_id = project_id
        # creates by sqlalchemy.orm.mapper:
        # self.fields = []
        # self.files = []

    def __repr__(self):
        return str(
            f'''<Issue(id='{ self.id
                }',\n caption='{ self.caption
                }',\n content='{ self.content
                }',\n issue_kind_id='{ self.issue_kind_id
                }',\n parent_id='{ self.parent_id
                }',\n project_id='{ self.project_id
                }')>'''
            )

    def field(self, field_kind_id):
        for field in self.fields:
            if field_kind_id == field.field_kind_id:
                return field
        return None
