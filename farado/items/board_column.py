#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BoardColumn():
    def __init__(
            self,
            board_id=None,
            state_id=None,
            order=0):
        self.id = None
        self.board_id = board_id
        self.state_id = state_id
        self.order = order

    def __repr__(self):
        return str(
            f'''<BoardColumn(id='{ self.id
                }',\n board_id='{ self.board_id
                }',\n state_id='{ self.state_id
                }',\n order='{ self.order
                }')>'''
            )
