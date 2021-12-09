#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import logging.config


logging.config.fileConfig('resources/logger.cfg')

## Default logger
dlog = logging.getLogger('root')

## Logging to file
flog = logging.getLogger('FileLogger')

## Logging to console
clog = logging.getLogger('ConsoleLogger')
