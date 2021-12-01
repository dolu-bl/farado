#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import logging.config


logging.config.fileConfig('resources/logger.cfg')

## Get default logger
def DLog():
    '''
    Usage example:
        DLog().debug('debug message')
        DLog().info('info message')
        DLog().warn('warn message')
        DLog().error('error message')
        DLog().critical('critical message')
    '''
    # TODO: Control default logger from config file
    return FLog

## Logging to file
FLog = logging.getLogger('FileLogger')

## logging to console
CLog = logging.getLogger('ConsoleLogger')

