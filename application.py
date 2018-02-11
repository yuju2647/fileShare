#!usr/bin/env python
#coding=utf-8
import os
import json
import tornado.web
import web_config
import logging

from utils import path
from utils import router
from tornado.ioloop import PeriodicCallback

class Application(tornado.web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self,handlers=router.Route.get_routes(),**web_config.settings)


if __name__ == '__main__':
    Application()


