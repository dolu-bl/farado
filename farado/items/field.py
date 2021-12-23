#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Field():
    def __init__( self
                , value
                , fieldkind_id = None
                , issue_id = None
                ):
        self.id = None
        self.value = value
        self.fieldkind_id = fieldkind_id
        self.issue_id = issue_id

    def __repr__(self):
        return str(
            f'''<Field(id='{ self.id
                }',\n issue_id='{ self.issue_id
                }',\n fieldkind_id='{ self.fieldkind_id
                }',\n value='{ self.value
                }')>'''
            )
