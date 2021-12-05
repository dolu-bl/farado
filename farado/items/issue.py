#!/usr/bin/python
# -*- coding: utf-8 -*-

class Issue():
    def __init__( self
                , caption
                , content
                , issuekind_id = None
                , parent_id = None
                , project_id = None
                ):
        self.id = None
        self.caption = caption
        self.content = content
        self.issuekind_id = issuekind_id
        self.parent_id = parent_id
        self.project_id = project_id

    def __repr__(self):
        return str(
            f'''<Issue(id='{ self.id
                }',\n caption='{ self.caption
                }',\n content='{ self.content
                }',\n issuekind_id='{ self.issuekind_id
                }',\n parent_id='{ self.parent_id
                }',\n project_id='{ self.project_id
                }')>'''
            )
