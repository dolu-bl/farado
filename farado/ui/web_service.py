#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

from farado.config import global_config, application_config
from farado.logger import DLog
from farado.ui.auth_view import AuthView



class WebService:
    def __init__(self):
        self.auth_view = AuthView()

    @cherrypy.expose
    def index(self):
        return "123"

    def run(self):
        # HACK: switching off date time output for cherrypy log
        cherrypy._cplogging.LogManager.time = lambda self : "cherrypy"
        cherrypy.config.update(global_config)
        cherrypy.log.screen = False
        cherrypy.tree.mount(self.auth_view, '/in', application_config)
        cherrypy.quickstart(self, '/', application_config)
