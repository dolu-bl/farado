#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Edge():
    def __init__(
            self,
            from_state_id=None,
            to_state_id=None,
            workflow_id=None,
            ):
        self.id = None
        self.from_state_id = from_state_id
        self.to_state_id = to_state_id
        self.workflow_id = workflow_id

    def __repr__(self):
        return str(
            f'''<Edge(id='{ self.id
                }',\n from_state_id='{ self.from_state_id
                }',\n to_state_id='{ self.to_state_id
                }',\n workflow_id='{ self.workflow_id
                }')>'''
            )
