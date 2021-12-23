#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy

from farado.config import global_config, application_config
from farado.logger import dlog
from farado.ui.users_view import UsersView
from farado.ui.projects_view import ProjectsView
from farado.ui.roles_view import RolesView
from farado.ui.renderer import view_renderer
from farado.ui.cookie_helper import current_session_id, set_current_session_id
from farado.general_manager_holder import gm_holder



class WebService:
    def __init__(self):
        self.users_view = UsersView()
        self.projects_view = ProjectsView()
        self.roles_view = RolesView()

    @cherrypy.expose
    def index(self, login=None, password=None):
        if login:
            session_id = gm_holder.permission_manager.login(login, password)
        else:
            session_id = current_session_id()

        user = gm_holder.permission_manager.user_by_session_id(session_id)
        if not user:
            return view_renderer["login"].render()

        set_current_session_id(session_id)
        return view_renderer["index"].render(user=user, project_manager=gm_holder.project_manager)

    @cherrypy.expose
    def logout(self):
        gm_holder.permission_manager.logout(current_session_id())
        set_current_session_id(None)
        return view_renderer["login"].render()

    def run(self):
        # HACK: switching off date time output for cherrypy log
        cherrypy._cplogging.LogManager.time = lambda self : "cherrypy"
        cherrypy.config.update(global_config)
        cherrypy.log.screen = False
        cherrypy.tree.mount(self.users_view, '/users', application_config)
        cherrypy.tree.mount(self.projects_view, '/projects', application_config)
        cherrypy.tree.mount(self.roles_view, '/roles', application_config)
        cherrypy.quickstart(self, '/', application_config)
