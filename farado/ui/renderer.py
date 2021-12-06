#!/usr/bin/python
# -*- coding: utf-8 -*-

import jinja2



template_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader('resources/views') ,
    extensions = ['jinja2.ext.loopcontrols', 'jinja2.ext.with_']
)
view_renderer = {}
view_renderer["in"] = template_environment.get_template("in.html")
