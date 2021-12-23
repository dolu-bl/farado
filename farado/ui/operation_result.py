#!/usr/bin/env python
# -*- coding: utf-8 -*-

class OperationResult:
    '''Stores a description of the result of the operation

    Attributes
    ----------
    caption : str
        Caption text of the result
    text : str
        Description of the result
    kind : str
        Kind of the result, possible values:
        * primary
        * secondary
        * success
        * danger
        * warning
        * info
        * light
        * dark
    '''
    def __init__(self, caption="", text="", kind="info"):
        self.caption = caption
        self.text = text
        self.kind = kind
