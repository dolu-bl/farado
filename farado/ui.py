#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from farado.config import global_config, application_config



class Ui:
    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        return "123"

    def run(self):
        cherrypy.config.update(global_config)
        cherrypy.quickstart(self, '/', application_config)
