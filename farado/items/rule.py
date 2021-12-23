#!/usr/bin/python
# -*- coding: utf-8 -*-

class Rule():
    def __init__(
            self,
            caption='',
            ):
        self.id = None
        self.caption = caption
        self.role_id = None
        self.project_id = None
        self.is_project_watcher = False
        self.is_project_editor = False
        self.is_project_creator = False
        self.is_project_deleter = False
        self.issue_kind_id = None
        self.workflow_id = None
        self.is_issue_watcher = False
        self.is_issue_editor = False
        self.is_issue_creator = False
        self.is_issue_deleter = False

    def __repr__(self):
        return str(
            f'''<Rule(id='{ self.id
                }',\n caption='{ self.caption
                }',\n role_id='{ self.role_id
                }',\n project_id='{ self.project_id
                }',\n is_project_watcher ='{ self.is_project_watcher 
                }',\n is_project_editor ='{ self.is_project_editor 
                }',\n is_project_creator ='{ self.is_project_creator 
                }',\n is_project_deleter ='{ self.is_project_deleter 
                }',\n issue_kind_id='{ self.issue_kind_id
                }',\n workflow_id='{ self.workflow_id
                }',\n is_issue_watcher ='{ self.is_issue_watcher 
                }',\n is_issue_editor ='{ self.is_issue_editor 
                }',\n is_issue_creator ='{ self.is_issue_creator 
                }',\n is_issue_deleter ='{ self.is_issue_deleter 
                }')>'''
            )

    def reset_properties(self, properties):
        '''
        properties example:
        {'caption': 'asdf', 'project_id': '2', 'project_watcher': 'on', 'issue_editor': 'on'}
        '''
        self.is_project_watcher = False
        self.is_project_editor = False
        self.is_project_creator = False
        self.is_project_deleter = False
        self.is_issue_watcher = False
        self.is_issue_editor = False
        self.is_issue_creator = False
        self.is_issue_deleter = False
        for key, value in properties.items():
            if key in 'caption':
                self.caption = value
            elif key in 'role_id':
                self.role_id = int(value)
            elif key in 'project_id':
                try:
                    self.project_id = int(value)
                except:
                    self.project_id = None
            elif key in 'is_project_watcher':
                self.is_project_watcher = bool('on' == value)
            elif key in 'is_project_editor':
                self.is_project_editor = bool('on' == value)
            elif key in 'is_project_creator':
                self.is_project_creator = bool('on' == value)
            elif key in 'is_project_deleter':
                self.is_project_deleter = bool('on' == value)
            elif key in 'issue_kind_id':
                try:
                    self.issue_kind_id = int(value)
                except:
                    self.project_id = None
            elif key in 'workflow_id':
                try:
                    self.workflow_id = int(value)
                except:
                    self.project_id = None
            elif key in 'is_issue_watcher':
                self.is_issue_watcher = bool('on' == value)
            elif key in 'is_issue_editor':
                self.is_issue_editor = bool('on' == value)
            elif key in 'is_issue_creator':
                self.is_issue_creator = bool('on' == value)
            elif key in 'is_issue_deleter':
                self.is_issue_deleter = bool('on' == value)
