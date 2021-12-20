#!/usr/bin/python
# -*- coding: utf-8 -*-

class Project():
    def __init__(
            self,
            caption='',
            content='',
            ):
        self.id = None
        self.caption = caption
        self.content = content
        # creates by sqlalchemy.orm.mapper:
        # self.issues = []

    def __repr__(self):
        return str(
            f'''<Project(id='{ self.id
                }',\n caption='{ self.caption
                }',\n content='{ self.content
                }')>'''
            )
