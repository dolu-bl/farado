#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Workflow():
    def __init__(
            self,
            caption,
            description,
            ):
        self.id = None
        self.caption = caption
        self.description = description

    def __repr__(self):
        return str(
            f'''<Workflow(id='{ self.id
                }',\n caption='{ self.caption
                }',\n description='{ self.description
                }')>'''
            )
