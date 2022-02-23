#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Comment():
    def __init__(
            self,
            issue_id=None,
            user_id=None,
            creation_datetime=None,
            content=None):
        self.id = None
        self.issue_id = issue_id
        self.user_id = user_id
        self.creation_datetime = creation_datetime
        self.content = content

    def __repr__(self):
        return str(
            f'''<Comment(id='{ self.id
                }',\n issue_id='{ self.issue_id
                }',\n user_id='{ self.user_id
                }',\n creation_datetime='{ self.creation_datetime
                }',\n content='{ self.content
                }')>'''
            )

    def formated_creation_datetime(self):
        # TODO: add date format selection in config
        return f'{self.creation_datetime:%d.%m.%Y %H:%M:%S}'
