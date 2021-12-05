#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from farado.config import global_config, application_config

from farado.logger import DLog


class Ui:
    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        for i in range(10000):
            DLog.error("asdfasdf")
            DLog.info("asdfasdf")
            DLog.warning("asdfasdf")
            DLog.critical("asdfasdf324")
        return "123"

    def run(self):
        # HACK: switching off date time output for cherrypy log
        cherrypy._cplogging.LogManager.time = lambda self : "cherrypy"
        cherrypy.config.update(global_config)
        cherrypy.log.screen = False
        cherrypy.quickstart(self, '/', application_config)
