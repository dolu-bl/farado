#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy



def current_session_id():
    cookie = cherrypy.request.cookie
    if "farado_session_id" in cookie:
        return cookie["farado_session_id"].value
    return None

def set_current_session_id(session_id=None):
    cherrypy.response.cookie["farado_session_id"] = session_id
