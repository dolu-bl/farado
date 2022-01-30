#!/usr/bin/env python
# -*- coding: utf-8 -*-

class File():
    def __init__(
            self,
            caption,
            name,
            path,
            description="",
            issue_id = None
            ):
        self.id = None
        self.caption = caption
        self.name = name
        self.path = path
        self.description = description
        self.issue_id = issue_id

    def __repr__(self):
        return str(
            f'''<File(id='{ self.id
                }',\n caption='{ self.caption
                }',\n name='{ self.name
                }',\n path='{ self.path
                }',\n description='{ self.description
                }',\n issue_id='{ self.issue_id
                }')>'''
            )
