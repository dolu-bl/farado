#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from time import sleep

from farado.session_manager import *



class SessionTest(unittest.TestCase):
    def test_check_duration(self):
        session = SessionManager.Session(duration=1)
        self.assertTrue(session.check_duration())
        sleep(2)
        self.assertFalse(session.check_duration())

class SessionManagerTest(unittest.TestCase):
    def test_a(self):
        # TODO : continue this
        self.assertTrue(True)
