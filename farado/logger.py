#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import logging.config


logging.config.fileConfig('resources/logger.cfg')

## Default logger
DLog = logging.getLogger('root')

## Logging to file
FLog = logging.getLogger('FileLogger')

## Logging to console
CLog = logging.getLogger('ConsoleLogger')
