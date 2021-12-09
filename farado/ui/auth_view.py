#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

from farado.logger import dlog
from farado.ui.renderer import view_renderer



class AuthView:
    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        return view_renderer["login"].render()
