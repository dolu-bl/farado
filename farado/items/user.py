#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import threading

from sqlalchemy import orm

from farado.logger import DLog



class User():
    def __init__( self
                , login
                , first_name
                , middle_name
                , last_name
                , email
                , password_hash = None
                , password = None
                , need_change_password = False
                , more_info = ""
                , is_blocked = False
                ):
        self.id = None
        self.login = login
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.need_change_password = need_change_password
        self.more_info = more_info
        self.is_blocked = is_blocked
        self.online_state = False
        self.mutex = threading.RLock()

        if password_hash:
            self.password_hash = password_hash
        elif password:
            self.set_password(password)
        else:
            raise ValueError('A password_hash or a password must be set for the user.')

    @orm.reconstructor
    def init_on_load(self):
        self.online_state = False
        self.mutex = threading.RLock()

    def __repr__(self):
        with self.mutex:
            return str(
                f'''<User(id='{ self.id
                    }',\n login='{ self.login
                    }',\n first_name='{ self.first_name
                    }',\n middle_name='{ self.middle_name
                    }',\n last_name='{ self.last_name
                    }',\n email='{ self.email
                    }',\n password_hash='{ self.password_hash
                    }',\n need_change_password='{ self.need_change_password
                    }',\n more_info='{ self.more_info
                    }',\n is_blocked='{ self.is_blocked
                    }',\n online_state='{ self.online_state
                    }')>'''
                )

    def set_password(self, password):
        with self.mutex:
            self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            DLog.info(f"User password changed: {self.login}")

    def check_password(self, password):
        with self.mutex:
            return bool(self.password_hash == hashlib.sha256(password.encode('utf-8')).hexdigest())
