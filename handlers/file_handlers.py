#!usr/bin/env python
# coding=utf-8

__author__ = 'yujun huang'

from utils import router

import os
import logging
import json
from utils import path
import base_handler

@router.Route("/console/file_upload")
class FileUploadHandler(base_handler.BaseHandler):

    def get(self):
        self.render('file_upload.html')

    def post(self):
        complect = int(self.get_argument('complect'))
        task_id = self.get_argument('task_id')
        chunk = self.get_argument('chunk', 0)
        temp_path = path.get_temp_path()
        if not complect:
            upload_file = self.request.files['file'][0]
            body = upload_file['body']
            temp_filename = "%s%s" % (task_id, chunk)
            with open(os.path.join(temp_path, temp_filename), 'wb') as fp:
                fp.write(body)
        else:
            logging.info('upload complect task_id: {}'.format(task_id))
            filename = self.get_argument('filename')
            filename_path = os.path.join(path.get_upload_path(), filename)
            filename_path = path.check_repeat_filename(filename_path)
            with open(filename_path, 'wb') as upload_file:
                wipe_temps = list()
                while True:
                    temp_filename = "%s%s" % (task_id, chunk)
                    temp_filename_path = os.path.join(temp_path, temp_filename)
                    if os.path.exists(temp_filename_path):
                        temp_file = open(temp_filename_path, 'rb')
                        upload_file.write(temp_file.read())
                        temp_file.flush()
                        temp_file.close()
                        logging.info('upload flushed temp file: {}'.format(temp_filename))
                        wipe_temps.append(temp_filename_path)
                    else:
                        logging.info('upload successfully file:{}'.format(filename))
                        logging.info('removing temp files')
                        for filename_path in wipe_temps:
                            os.remove(filename_path)
                        logging.info('remove complect')
                        break
                    chunk += 1


if __name__ == '__main__':
    pass