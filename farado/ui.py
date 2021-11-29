#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from farado.config import global_config, application_config



class Ui:
    def __init__(self) -> None:
        cherrypy.quickstart(self, '/', application_config)
