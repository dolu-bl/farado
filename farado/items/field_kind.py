#!/usr/bin/python
# -*- coding: utf-8 -*-

class FieldKind():
    def __init__(
            self,
            caption,
            value_type,
            description,
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
