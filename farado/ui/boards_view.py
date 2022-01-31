#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy
import json

from farado.logger import dlog
from farado.ui.renderer import view_renderer
from farado.ui.cookie_helper import current_session_id
from farado.general_manager_holder import gm_holder
from farado.items.board import Board
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
    def board(
            self,
            target_board_id=None,
            target_board_caption='',
            target_board_description='',
            ):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        # TODO : rights

        target_board = gm_holder.project_manager.board(target_board_id)
        if not target_board and not target_board_caption:
            return view_renderer["404"].render()

        operation_result = None
        if target_board_caption:
            if not target_board:
                if not self.is_admin(user.id):
                    return view_renderer["403"].render()
                target_board = Board()

            target_board.caption = target_board_caption
            target_board.description = target_board_description
            gm_holder.project_manager.save_item(target_board)
            operation_result = OperationResult(caption="Board saved", kind="success")

        return view_renderer["board"].render(
            user=user,
            target_board=target_board,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=self.is_admin(user.id),
                )
            )

    @cherrypy.expose
    def add_board(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        if not self.is_admin(user.id):
            return view_renderer["403"].render()

        return view_renderer["board"].render(
            user=user,
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
