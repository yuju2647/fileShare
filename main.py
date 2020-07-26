#!usr/bin/env python
#coding=utf-8
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filemode='w')

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import other_config
import sys
from handlers import *
from application import Application
from tornado.options import define, options


def main():
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    logging.info('''
                ************                          ****************
                ****************server {} is running********************
                ************                          ****************
            '''.format(options._options['port'].default))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    define("port", default=8809, type=int)
    main()