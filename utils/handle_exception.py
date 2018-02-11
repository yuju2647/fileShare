#!usr/bin/env python
# coding=utf-8

import logging
import json
import traceback
import threading

import _mysql_exceptions
def getpost_wrapper(func):
    thread_local = threading.local()
    thread_local.failed_times=0

    def wrapper(self):
        result=handle_exception(self)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(json.dumps(result))

    def handle_exception(self):
        result = {"data": None, "error": None}
        try:
            result['data'] = func(self)
        except _mysql_exceptions.OperationalError,e:
            thread_local.failed_times+=1
            failed_times=thread_local.failed_times
            logging.warning("ERROR OperationalError ,failed times={} {}".format(failed_times,traceback.format_exc()))
            logging.info('try to reset connection')
            self.application.reset_conn_pool()
            if failed_times>=3:
                logging.warning("ERROR {} {} ".format(e, traceback.format_exc()))
                result['error'] = str(e)
            else:
                result=handle_exception(self)
        except Exception, e:
            logging.warning("ERROR {} {} ".format(e,traceback.format_exc()))
            result['error']=str(e)
        return result

    return wrapper

