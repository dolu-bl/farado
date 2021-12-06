#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

from farado.logger import DLog
from farado.ui.renderer import view_renderer



class AuthView:
    def __init__(self, web_service):
        self.web_service = web_service

    @cherrypy.expose
    def index(self, login=None, password=None):
        print("login =", login)
        print("password =", password)
        return view_renderer["in"].render()
