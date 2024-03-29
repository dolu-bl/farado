#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

global_config = {
    'global': {
        # 'server.environment': 'production', # enable for production
        # 'server.socket_host': '0.0.0.0', # allow any hosts
        'server.socket_port': 8080,
    },
}

application_config = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd()),
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './resources/public',
    }
}

farado_config = {
    'database': {
        'connection_string' : 'sqlite:///resources/database.sqlite',
    },
    'uploads': {
        'path' : './resources/uploads'
    },
}
