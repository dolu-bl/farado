#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BoardColumn():
    def __init__(
            self,
            board_id=None,
            state_id=None,
            caption='',
            order=0):
        self.id = None
        self.board_id = board_id
        self.state_id = state_id
        self.caption = caption
        self.order = order

    def __repr__(self):
        return str(
            f'''<BoardColumn(id='{ self.id
                }',\n board_id='{ self.board_id
                }',\n state_id='{ self.state_id
                }',\n caption='{ self.caption
                }',\n order='{ self.order
                }')>'''
            )

    def reset_properties(self, properties):
        '''
        properties example:
        {'state_id': '2', 'caption': 'asdf', 'order': '3'}
        '''
        for key, value in properties.items():
            if key in 'caption':
                self.caption = value
            elif key in 'state_id':
                self.state_id = to_int_or_none(value)
            elif key in 'order':
                self.order = to_int_or_none(value)

def to_int_or_none(value):
    try:
        return int(value)
    except:
        return None
