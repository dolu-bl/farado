#!/usr/bin/env python
# -*- coding: utf-8 -*-

class IssueKind():
    def __init__(
            self,
            caption='',
            workflow_id=None,
            default_state_id=None,
            ):
        self.id = None
        self.caption = caption
        self.workflow_id = workflow_id
        self.default_state_id = default_state_id
        # creates by sqlalchemy.orm.mapper:
        # self.field_kinds = []

    def __repr__(self):
        return str(
            f'''<IssueKind(id='{ self.id
                }',\n caption='{ self.caption
                }',\n workflow_id='{ self.workflow_id
                }',\n default_state_id='{ self.default_state_id
                }')>'''
            )
