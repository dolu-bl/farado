#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

from farado.config import global_config, application_config
from farado.logger import DLog
from farado.ui.auth_view import AuthView



class WebService:
    def __init__(self, stem):
        self.auth_view = AuthView(self)
        self.stem = stem

    @cherrypy.expose
    def index(self, login=None, password=None):

        if login:
            session_id = self.stem.permission_manager.login(login, password)
        else:
            session_id = self.session_id()
            if not self.stem.session_manager.check_session_id(session_id):
                return self.auth_view.index()

        return "123" + str(session_id)


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
        cherrypy.tree.mount(self.auth_view, '/in', application_config)
        cherrypy.quickstart(self, '/', application_config)
