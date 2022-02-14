#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib

from farado.logger import logger
from farado.config import farado_config



class FileManager:
    def __init__(self) -> None:
        self.uploads_path = farado_config['uploads']['path']

    def save_uploaded_file(self, path, filename, data):
        # make path
        target_path = os.path.join(self.uploads_path, path)
        pathlib.Path(target_path).mkdir(parents=True, exist_ok=True)

        # save file
        target_file_name = os.path.join(target_path, filename)
        with open(target_file_name, "wb") as file:
            file.write(data)
            logger.info(F'Uploaded file {target_file_name} saved')

    def remove_uploaded_file(self, path, filename):
        abs_file_name = os.path.abspath(
            os.path.join(
                self.uploads_path,
                path,
                filename))
        if abs_file_name and os.path.isfile(abs_file_name):
            os.remove(abs_file_name)
            logger.info(F'Uploaded file {abs_file_name} removed')

    def file_path(self, file):
        return os.path.abspath(
            os.path.join(
                self.uploads_path,
                file.path,
                file.name))

    def file_size(self, file):
        return os.path.getsize(
            self.file_path(file))

    def file_type(self, filename):
        '''
        Returns
        -------
        String
            file type by it name, values can be:
            * 'image'
            * 'html'
            * 'text'
            * 'video'
            * 'audio'
            * 'flash'
            * 'pdf'
            * 'object'
        '''
        file_extension = filename.split(".")[-1]
        if ('tiff' in file_extension or
            'wmf' in file_extension or
            'gif' in file_extension or
            'png' in file_extension or
            'jpeg' in file_extension or
            'jpg' in file_extension):
            return 'image'

        if ('html' in file_extension or
            'htm' in file_extension):
            return 'html'

        if ('txt' in file_extension or
            'md' in file_extension or
            'nfo' in file_extension or
            'php' in file_extension or
            'ini' in file_extension):
            return 'text'

        if ('ogg' in file_extension or
            'mp4' in file_extension or
            'webm' in file_extension):
            return 'video'

        if ('mp3' in file_extension or
            'wav' in file_extension):
            return 'audio'

        if ('swf' in file_extension):
            return 'flash'

        if ('pdf' in file_extension):
            return 'pdf'

        return 'object'
