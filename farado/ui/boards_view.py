#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy
import json

from farado.logger import logger
from farado.ui.renderer import view_renderer
from farado.ui.cookie_helper import current_session_id
from farado.general_manager_holder import gm_holder
from farado.items.board import Board
from farado.items.board_column import BoardColumn
from farado.ui.operation_result import OperationResult
from farado.permission_manager import PermissionFlag
from farado.ui.base_view import BaseView, UiUserRestrictions



class BoardsView(BaseView):

    @cherrypy.expose
    def index(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        return view_renderer["boards"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                )
            )

    @cherrypy.expose
    def board(self, target_board_id=None, function=None, **args):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        if function:
            self.process_function(user, function)

        is_reading = bool(len(args) == 0)

        # TODO : rights

        target_board = gm_holder.project_manager.board(target_board_id)
        if not target_board and is_reading:
            return view_renderer["404"].render()

        operation_result = None
        if not is_reading:
            if not target_board:
                if not self.is_admin(user.id):
                    return view_renderer["403"].render()
                target_board = Board()

            if 'target_board_caption' in args:
                target_board.caption = args['target_board_caption']

            if 'target_board_description' in args:
                target_board.description = args['target_board_description']

            if 'target_board_workflow_id' in args:
                target_board_workflow_id = args['target_board_workflow_id']
                if target_board_workflow_id.isdigit() and bool(int(target_board_workflow_id)):
                    target_board.workflow_id = int(target_board_workflow_id)

            # To get target_board_id we must save the new item
            if not target_board_id:
                gm_holder.project_manager.save_item(target_board)
            self.save_board_columns(target_board.id, args)

            gm_holder.project_manager.save_item(target_board)
            operation_result = OperationResult(caption="Board saved", kind="success")

        return view_renderer["board"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            target_board=target_board,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                )
            )

    def save_board_columns(self, target_board_id, args):
        # Prepare board column property values
        board_column_properties = {}
        for key, value in args.items():
            if not key.startswith("board_column"):
                continue
            key_data = key.split("_")
            board_column_id = key_data[-1]
            board_column_field = "_".join(key_data[2:-1])
            if not board_column_id in board_column_properties:
                board_column_properties[board_column_id] = {}
            board_column_properties[board_column_id][board_column_field] = value

        # Apply rules property changes
        for board_column_id, properties in board_column_properties.items():
            board_column = gm_holder.project_manager.board_column(board_column_id)
            board_column.reset_properties(properties)
            board_column.board_id = target_board_id
            gm_holder.project_manager.save_item(board_column)

        # Remove deleted rules
        for board_column in gm_holder.project_manager.board_columns_by_board(target_board_id):
            if str(board_column.id) in board_column_properties:
                continue
            gm_holder.project_manager.remove_item(BoardColumn, board_column.id)


    @cherrypy.expose
    def add_board(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        if not self.is_admin(user.id):
            return view_renderer["403"].render()

        return view_renderer["board"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            target_board=None,
            save_result=None,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                )
            )

    @cherrypy.expose
    def remove_board(self, target_board_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        if not self.is_admin(user.id):
            return view_renderer["403"].render()

        gm_holder.project_manager.remove_item(Board, target_board_id)
        operation_result = OperationResult(caption="Board removed", kind="success")

        return view_renderer["boards"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                )
            )

    @cherrypy.expose
    def add_board_column(self, target_board_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        if not gm_holder.project_manager.board(target_board_id):
            return view_renderer["404"].render()

        board_column = BoardColumn()
        board_column.board_id = target_board_id
        gm_holder.project_manager.save_item(board_column)

        return view_renderer["board"].render(
            user=user,
            target_board=gm_holder.project_manager.board(target_board_id),
            project_manager=gm_holder.project_manager,
            operation_result=OperationResult(caption="Column added", kind="success"),
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )
