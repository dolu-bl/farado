#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jinja2



template_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader('resources/views') ,
    extensions = ['jinja2.ext.loopcontrols', 'jinja2.ext.with_']
)
view_renderer = {}
view_renderer["login"] = template_environment.get_template("login.html.j2")
view_renderer["index"] = template_environment.get_template("index.html.j2")
view_renderer["logs"] = template_environment.get_template("logs.html.j2")
view_renderer["users"] = template_environment.get_template("users.html.j2")
view_renderer["user"] = template_environment.get_template("user.html.j2")
view_renderer["projects"] = template_environment.get_template("projects.html.j2")
view_renderer["project"] = template_environment.get_template("project.html.j2")
view_renderer["roles"] = template_environment.get_template("roles.html.j2")
view_renderer["role"] = template_environment.get_template("role.html.j2")
view_renderer["workflows"] = template_environment.get_template("workflows.html.j2")
view_renderer["workflow"] = template_environment.get_template("workflow.html.j2")
view_renderer["issue_kinds"] = template_environment.get_template("issue_kinds.html.j2")
view_renderer["issue_kind"] = template_environment.get_template("issue_kind.html.j2")
view_renderer["issues"] = template_environment.get_template("issues.html.j2")
view_renderer["issue"] = template_environment.get_template("issue.html.j2")
view_renderer["new_issue"] = template_environment.get_template("new_issue.html.j2")
view_renderer["boards"] = template_environment.get_template("boards.html.j2")
view_renderer["board"] = template_environment.get_template("board.html.j2")
