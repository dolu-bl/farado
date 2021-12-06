#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

from farado.logger import DLog



class AuthView:
    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        return "12321"
