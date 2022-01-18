#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Field():
    def __init__(
            self,
            value=None,
            field_kind_id=None,
            issue_id=None
            ):
        self.id = None
        self.value = value
        self.field_kind_id = field_kind_id
        self.issue_id = issue_id

    def __repr__(self):
        return str(
            f'''<Field(id='{ self.id
                }',\n issue_id='{ self.issue_id
                }',\n field_kind_id='{ self.field_kind_id
                }',\n value='{ self.value
                }')>'''
            )
