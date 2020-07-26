#!usr/bin/env python
#coding=utf-8
import os
import json
import tornado.web
import logging

from utils import path
from utils import router
from tornado.ioloop import PeriodicCallback

settings = {
    "debug": True,
    "template_path": "templates",
    "static_path": "statics",
    "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwsQt8S0R0kRvJ5/xJkjdkfsjld",
    "login_url": "/file/login"
}

class Application(tornado.web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self,handlers=router.Route.get_routes(), **settings)


if __name__ == '__main__':
    Application()


