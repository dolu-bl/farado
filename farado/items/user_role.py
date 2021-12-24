#!/usr/bin/env python
# -*- coding: utf-8 -*-

class UserRole():
    def __init__(self, user_id=None, role_id=None):
        self.id = None
        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return str(
            f'''<UserRole(id='{ self.id
                }',\n user_id='{ self.user_id
                }',\n role_id='{ self.role_id
                }')>'''
            )
