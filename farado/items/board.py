#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Board():
    def __init__(
            self,
            caption=None,
            description=None,
            workflow_id=None):
        self.id = None
        self.caption = caption
        self.description = description
        self.workflow_id = workflow_id
        # creates by sqlalchemy.orm.mapper:
        # self.board_columns = []

    def __repr__(self):
        return str(
            f'''<Board(id='{ self.id
                }',\n caption='{ self.caption
                }',\n description='{ self.description
                }',\n workflow_id='{ self.workflow_id
                }')>'''
            )

    def board_column(self, board_column_id):
        if not board_column_id:
            return None
        board_column_id = int(board_column_id)
        for board_column in self.board_columns:
            if board_column_id == board_column.field_kind_id:
                return board_column
        return None

    def ordered_board_columns(self):
        return sorted(
            self.board_columns,
            key=lambda column: column.order)
