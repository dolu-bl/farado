#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

from farado.config import global_config, application_config
from farado.logger import DLog
from farado.ui.auth_view import AuthView
from farado.ui.renderer import view_renderer



class WebService:
    def __init__(self, stem):
        self.auth_view = AuthView(self)
        self.stem = stem

    @cherrypy.expose
    def index(self, login=None, password=None):
        if login:
            session_id = self.stem.permission_manager.login(login, password)
            DLog.info(f'Login attempt: {login} session_id: {session_id}')
        else:
            session_id = self.session_id()

        user = self.stem.session_manager.user_by_session_id(session_id)
        if not user:
            DLog.info(f"Providing login window")
            return view_renderer["login"].render()

        cherrypy.response.cookie["farado_session_id"] = session_id
        return view_renderer["index"].render(user=user)

    @cherrypy.expose
    def logout(self, login=None, password=None):
        session_id = self.session_id()
        user = self.stem.session_manager.user_by_session_id(session_id)
        if user:
            DLog.info(f'Logout user: {user.login} session_id: {session_id}')
        else:
            DLog.info(f'Logout session_id: {session_id}')
        cherrypy.response.cookie["farado_session_id"] = None
        self.stem.session_manager.remove_session(session_id)
        return view_renderer["login"].render()

    def session_id(self):
        cookie = cherrypy.request.cookie
        if "farado_session_id" in cookie:
            return cookie["farado_session_id"].value
        return None

    def run(self):
        # HACK: switching off date time output for cherrypy log
        cherrypy._cplogging.LogManager.time = lambda self : "cherrypy"
        cherrypy.config.update(global_config)
        cherrypy.log.screen = False
        cherrypy.tree.mount(self.auth_view, '/login', application_config)
        cherrypy.quickstart(self, '/', application_config)
