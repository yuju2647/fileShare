#!usr/bin/env python
# coding=utf-8

__author__ = 'yujun huang'

from utils import router

import os
import glob
import json
import logging
from handlers.base_handler import BaseHandler
from utils import path

@router.Route("/console/file_upload")
class FileUploadHandler(BaseHandler):

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


@router.Route("/console/view_files")
class FilesViewHandler(BaseHandler):

    def get(self):
        upload_path = path.get_upload_path()
        filenames = glob.glob(os.path.join(upload_path, '*'))
        file_names = sorted([ os.path.basename(filename) for filename in filenames])
        self.render("view_files.html", **{"file_names" : file_names})


@router.Route("/console/download_file")
class FileDownloadHandler(BaseHandler):

    def get(self):
        upload_path = path.get_upload_path()
        file_name = self.get_argument("file_name")
        filename = os.path.join(upload_path, file_name)
        self.set_header("Content-type", "application/octet-stream")
        self.set_header("Content-disposition", "attachment; filename={}".format(file_name))
        buf_size = 4069
        with open(filename, 'rb') as input:
            while True:
                by = input.read(buf_size)
                if not by:
                    break
                self.write(by)
        self.finish()

if __name__ == '__main__':
    pass