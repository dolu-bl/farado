#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy

from farado.logger import dlog
from farado.ui.renderer import view_renderer
from farado.ui.cookie_helper import current_session_id
from farado.general_manager_holder import gm_holder
from farado.items.workflow import Workflow
from farado.items.state import State
from farado.items.edge import Edge
from farado.ui.operation_result import OperationResult
from farado.ui.base_view import BaseView, UiUserRestrictions


class WorkflowsView(BaseView):

    @cherrypy.expose
    def index(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        return view_renderer["workflows"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def workflow(
            self,
            target_workflow_id,
            target_workflow_caption=None,
            target_workflow_description='',
            ):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        target_workflow = gm_holder.project_manager.workflow(target_workflow_id)

        operation_result = None
        if target_workflow_caption:
            if not target_workflow:
                target_workflow = Workflow()

            target_workflow.caption = target_workflow_caption
            target_workflow.description = target_workflow_description
            gm_holder.project_manager.save_item(target_workflow)
            operation_result = OperationResult(caption="Workflow saved", kind="success")

        return view_renderer["workflow"].render(
            user=user,
            target_workflow=target_workflow,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def add_workflow(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        return view_renderer["workflow"].render(
            user=user,
            target_workflow=None,
            save_result=None,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def remove_workflow(self, target_workflow_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        gm_holder.project_manager.remove_item(Workflow, target_workflow_id)
        operation_result = OperationResult(caption="Workflow removed", kind="success")

        return view_renderer["workflows"].render(
            user=user,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def add_state(self, target_workflow_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        state = State()
        state.workflow_id = int(target_workflow_id)
        state.caption = "New state"
        gm_holder.project_manager.save_item(state)
        target_workflow = gm_holder.project_manager.workflow(target_workflow_id)
        operation_result = OperationResult(caption="State added to workflow", kind="success")

        return view_renderer["workflow"].render(
            user=user,
            target_workflow=target_workflow,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def save_state(
            self,
            target_workflow_id,
            target_state_id,
            target_state_caption,
            target_state_description,
            ):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        target_state = gm_holder.project_manager.state(target_state_id)
        target_state.caption = target_state_caption
        target_state.description = target_state_description
        gm_holder.project_manager.save_item(target_state)
        target_workflow = gm_holder.project_manager.workflow(target_workflow_id)
        operation_result = OperationResult(caption="State saved", kind="success")

        return view_renderer["workflow"].render(
            user=user,
            target_workflow=target_workflow,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def remove_state(self, target_workflow_id, target_state_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        gm_holder.project_manager.remove_item(State, target_state_id)
        target_workflow = gm_holder.project_manager.workflow(target_workflow_id)
        operation_result = OperationResult(caption="State removed form workflow", kind="success")

        return view_renderer["workflow"].render(
            user=user,
            target_workflow=target_workflow,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )




    @cherrypy.expose
    def add_edge(self, target_workflow_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        edge = Edge()
        edge.workflow_id = int(target_workflow_id)
        gm_holder.project_manager.save_item(edge)
        target_workflow = gm_holder.project_manager.workflow(target_workflow_id)
        operation_result = OperationResult(caption="Edge added to workflow", kind="success")

        return view_renderer["workflow"].render(
            user=user,
            target_workflow=target_workflow,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def save_edge(
            self,
            target_workflow_id,
            target_edge_id,
            target_edge_from_state_id,
            target_edge_to_state_id,
            ):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        target_edge = gm_holder.project_manager.edge(target_edge_id)
        target_edge.from_state_id = int(target_edge_from_state_id)
        target_edge.to_state_id = int(target_edge_to_state_id)
        gm_holder.project_manager.save_item(target_edge)
        target_workflow = gm_holder.project_manager.workflow(target_workflow_id)
        operation_result = OperationResult(caption="Edge saved", kind="success")

        return view_renderer["workflow"].render(
            user=user,
            target_workflow=target_workflow,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )



    @cherrypy.expose
    def remove_edge(self, target_workflow_id, target_edge_id):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        is_admin = self.is_admin(user.id)
        if not is_admin:
            return view_renderer["403"].render()

        gm_holder.project_manager.remove_item(Edge, target_edge_id)
        target_workflow = gm_holder.project_manager.workflow(target_workflow_id)
        operation_result = OperationResult(caption="Edge removed form workflow", kind="success")

        return view_renderer["workflow"].render(
            user=user,
            target_workflow=target_workflow,
            project_manager=gm_holder.project_manager,
            operation_result=operation_result,
            restriction=UiUserRestrictions(
                is_admin=is_admin,
                )
            )
