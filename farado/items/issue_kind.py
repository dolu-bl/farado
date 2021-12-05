#!/usr/bin/python
# -*- coding: utf-8 -*-

class IssueKind():
    def __init__( self
                , caption
                , workflow_id = None
                ):
        self.id = None
        self.caption = caption
        self.workflow_id = workflow_id

    def __repr__(self):
        return str(
            f'''<IssueKind(id='{ self.id
                }',\n caption='{ self.caption
                }',\n workflow_id='{ self.workflow_id
                }')>'''
            )
