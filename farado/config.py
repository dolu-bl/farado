#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

global_config = {
    'global': {
        # 'server.socket_host': '0.0.0.0', # allow any hosts 
        'server.socket_port': 8080,
    },
}

application_config = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './public'
    }
}
