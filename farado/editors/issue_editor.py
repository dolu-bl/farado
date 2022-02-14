#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from farado.logger import logger
from farado.general_manager_holder import gm_holder
from farado.items.issue import Issue
from farado.items.file import File
from farado.permission_manager import PermissionFlag



class IssueEditor():

    def change(self, rights, target_issue_id=None, **args):
        if PermissionFlag.editor > rights:
            logger.warning('No issue editor rights')
            return (False, 'No issue editor rights')

        target_issue = gm_holder.project_manager.issue(target_issue_id)
        need_create_new = bool(not target_issue)

        if need_create_new:
            if PermissionFlag.creator > rights:
                logger.warning('No issue creator rights')
                return (False, 'No issue creator rights')

            issue_kind_id = args['issue_kind_id'] if 'issue_kind_id' in args else None
            target_issue = gm_holder.project_manager.create_issue(issue_kind_id)
            if not target_issue:
                logger.warning('Issue_kind not found')
                return (False, 'Issue_kind not found')

            if 'issue_files_editor' in args:
                gm_holder.project_manager.save_item(target_issue)
                for file_data in args['issue_files_editor']:
                    file_id = str(uuid.uuid4())
                    file_path = f'issue_{target_issue.id}'
                    gm_holder.project_manager.file_manager.save_uploaded_file(
                        file_path,
                        file_id,
                        file_data.file.read())

                    target_issue.files.append(File(
                        file_data.filename,
                        file_id,
                        file_path
                    ))

        if 'issue_caption' in args:
            target_issue.caption = args['issue_caption']
        if 'issue_content' in args:
            target_issue.content = args['issue_content']

        if 'issue_project_id' in args:
            issue_project_id = args['issue_project_id']
            if issue_project_id.isdigit() and bool(int(issue_project_id)):
                target_issue.project_id = int(issue_project_id)

        if 'issue_parent_id' in args:
            issue_parent_id = args['issue_parent_id']
            if issue_parent_id.isdigit() and bool(int(issue_parent_id)):
                target_issue.parent_id = int(issue_parent_id)

        if 'issue_state_id' in args:
            issue_state_id = args['issue_state_id']
            if issue_state_id.isdigit() and bool(int(issue_state_id)):
                target_issue.state_id = int(issue_state_id)

        # Clearing fields values
        for field in target_issue.fields:
            field.value = None
        # Appling fields values
        for field in target_issue.fields:
            field_kind_argument = f'field_kind_{field.field_kind_id}'
            if field_kind_argument in args:
                field.value = args[field_kind_argument]

        gm_holder.project_manager.save_item(target_issue)
        print(target_issue)
        logger.warning('New issue saved' if need_create_new else 'Issue saved')
        return (True, 'New issue saved' if need_create_new else 'Issue saved')



    def create_issue(self, rights, issue_kind_id, parent_id=None, project_id=None):
        # TODO: issue_kind_rights
        temporary_issue = gm_holder.project_manager.create_issue(issue_kind_id)
        if parent_id:
            temporary_issue.parent_id = int(parent_id)
        if project_id:
            temporary_issue.project_id = int(project_id)
        return (True, "Temporary issue created")



    def remove_issue(self, rights, target_issue_id):
        # TODO: issue_kind_rights
        gm_holder.project_manager.remove_item(Issue, target_issue_id)
        return (True, "Issue removed")
