#!/usr/bin/python
# -*- coding: utf-8 -*-

class Role():
    def __init__(
            self,
            caption='',
            ):
        self.id = None
        self.caption = caption
        # creates by sqlalchemy.orm.mapper:
        # self.rules = []

    def __repr__(self):
        return str(
            f'''<Role(id='{ self.id
                }',\n caption='{ self.caption
                }')>'''
            )
