#!/usr/bin/env python
# -*- coding: utf-8 -*-

class State():
    def __init__(
            self,
            caption="",
            description="",
            workflow_id=None,
            ):
        self.id = None
        self.caption = caption
        self.description = description
        self.workflow_id = workflow_id

    def __repr__(self):
        return str(
            f'''<State(id='{ self.id
                }',\n caption='{ self.caption
                }',\n description='{ self.description
                }',\n workflow_id='{ self.workflow_id
                }')>'''
            )
