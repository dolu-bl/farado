#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
import time
import threading

from farado.logger import DLog



class SessionManager:
    '''Stores and manages user sessions

    Attributes
    ----------
    sessions : list
        List of active user sessions
    sessions_mutex : threading.RLock
        Mutex for sessions container
    '''

    class Session:
        '''User session info

        Attributes
        ----------
        id : uuid.UUID
            Session identifier
        user : User
            Reference to user instance
        duration : int
            Session duration in seconds
        last_action_time : float
            Timestamp of last user action
        '''

        def __init__(self, user = None, id = uuid.uuid1(), duration = 3600):
            self.id = id
            self.user = user
            self.duration = duration
            self.last_action_time = time.time()

        def check_duration(self):
            '''Checks if the session has timed out

            Returns
            -------
            bool
                flag whether session has expired
            '''
            result = bool((time.time() - self.last_action_time) <= self.duration)
            if not result and self.user:
                DLog.info(f'User session has expired: {self.user.login}')
            return result

        def keep_alive(self):
            '''Updates the last action time for this session
            '''
            self.last_action_time = time.time()

    def __init__(self):
        self.sessions = []
        self.sessions_mutex = threading.RLock()

    def kill_expired_session(self):
        '''Delete all sessions that have expired
        '''
        with self.sessions_mutex:
            self.sessions = [session for session in self.sessions if session.check_duration()]

    def user_by_session_id(self, id):
        '''Checks if there is a session with given id and returns user instance

        Method calls deleter for all sessions that have expired
        and calls keep alive for checked session

        Parameters
        ----------
        id : uuid.UUID
            Session id

        Returns
        -------
        User
            user instance, if there is a session with the given id
        '''
        if not id:
            return None

        try:
            if not isinstance(id, uuid.UUID):
                id = uuid.UUID(id)
        except ValueError:
            return None

        with self.sessions_mutex:

            self.kill_expired_session()

            for session in self.sessions:
                if not id == session.id:
                    continue

                session.keep_alive()
                return session.user
        return None

    def check_user_id(self, id):
        '''Checks if there is a session for a user with given id

        Method calls deleter for all sessions that have expired

        Parameters
        ----------
        id : int
            User id

        Returns
        -------
        bool
            flag whether there is a session for the user
        '''
        if not id:
            return False

        with self.sessions_mutex:

            self.kill_expired_session()

            for session in self.sessions:
                if not session.user:
                    continue

                if not id == session.user.id:
                    continue

                return True
        return False

    def create_session(self, user):
        '''Creates a new user session if there is none

        Parameters
        ----------
        user : User
            Instance of the user

        Returns
        -------
        uuid.UUID
            session id
        None
            if a user session was not created due to the fact that one already exists
        '''
        with self.sessions_mutex:
            if self.check_user_id(user.id):
                return None

            # TODO: get duration form config
            session = self.Session(user)
            self.sessions.append(session)
            return session.id

    def remove_session(self, id):
        '''Removes user session

        Parameters
        ----------
        id : uuid.UUID
            Session id

        Returns
        -------
        bool
            if the session was removed
        '''
        with self.sessions_mutex:
            session_to_remove = [session for session in self.sessions if session.id == id]
            for session in session_to_remove:
                self.sessions.remove(session)

            return bool(session_to_remove)
