#!/usr/bin/python
# -*- coding: utf-8 -*-

import jinja2



template_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader('resources/views') ,
    extensions = ['jinja2.ext.loopcontrols', 'jinja2.ext.with_']
)
view_renderer = {}
view_renderer["login"] = template_environment.get_template("login.html")
view_renderer["index"] = template_environment.get_template("index.html")
view_renderer["users"] = template_environment.get_template("users.html")
view_renderer["user"] = template_environment.get_template("user.html")
view_renderer["projects"] = template_environment.get_template("projects.html")
view_renderer["project"] = template_environment.get_template("project.html")
view_renderer["roles"] = template_environment.get_template("roles.html")
view_renderer["role"] = template_environment.get_template("role.html")
