#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

from farado.config import global_config, application_config
from farado.logger import dlog
from farado.ui.auth_view import AuthView
from farado.ui.renderer import view_renderer
from farado.ui.cookie_helper import current_session_id, set_current_session_id
from farado.general_manager_holder import gm_holder
from farado.items.user import User



class WebService:
    def __init__(self):
        self.auth_view = AuthView()

    @cherrypy.expose
    def index(self, login=None, password=None):
        if login:
            session_id = gm_holder.permission_manager.login(login, password)
        else:
            session_id = current_session_id()

        user = gm_holder.permission_manager.user_by_session_id(session_id)
        if not user:
            return view_renderer["login"].render()

        set_current_session_id(session_id)
        return view_renderer["index"].render(user=user, project_manager=gm_holder.project_manager)

    @cherrypy.expose
    def logout(self):
        gm_holder.permission_manager.logout(current_session_id())
        set_current_session_id(None)
        return view_renderer["login"].render()

    @cherrypy.expose
    def users(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        return view_renderer["users"].render(user=user, project_manager=gm_holder.project_manager)

    @cherrypy.expose
    def user(
            self,
            target_user_id,
            target_user_login=None,
            target_user_email=None,
            target_user_first_name=None,
            target_user_middle_name=None,
            target_user_last_name=None,
            target_user_password=None,
            target_user_need_change_password=None,
            target_user_is_blocked=None,
            ):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        target_user=gm_holder.project_manager.user_by_id(target_user_id)

        save_result = None
        if target_user_login:
            if not target_user:
                target_user = User()
            target_user.login = target_user_login
            target_user.email = target_user_email
            target_user.first_name = target_user_first_name
            target_user.middle_name = target_user_middle_name
            target_user.last_name = target_user_last_name
            target_user.need_change_password = bool(target_user_need_change_password == 'on')
            target_user.is_blocked = bool(target_user_is_blocked == 'on')
            if target_user_password and 0 < len(target_user_password):
                target_user.set_password(target_user_password)
            gm_holder.project_manager.save_item(target_user)
            save_result = True

        return view_renderer["user"].render(
            user=user,
            target_user=target_user,
            save_result=save_result)

    @cherrypy.expose
    def new_user(self):
        user = gm_holder.permission_manager.user_by_session_id(current_session_id())
        if not user:
            return view_renderer["login"].render()

        return view_renderer["user"].render(
            user=user,
            target_user=None,
            save_result=None)

    def run(self):
        # HACK: switching off date time output for cherrypy log
        cherrypy._cplogging.LogManager.time = lambda self : "cherrypy"
        cherrypy.config.update(global_config)
        cherrypy.log.screen = False
        cherrypy.tree.mount(self.auth_view, '/login', application_config)
        cherrypy.quickstart(self, '/', application_config)
