#!usr/bin/env python
# coding=utf-8

__author__ = 'yujun huang'

from utils import time_transfer
from utils import request_data
from utils import path

import sys
import logging
import datetime


def tran_stamp_to_time(user, *args):
    for arg in args:
        try:
            value = user[arg]
            if value:
                value = float(value) / 1000
                user[arg] = time_transfer.timestamp_to_time(value)
        except Exception, e:
            logging.warning('Error :{}'.format(e))

def tran_datetime_to_str(user, *args):
    for arg in args:
        date = user[arg]
        if date and isinstance(date, datetime.datetime):
            date_str = date.strftime('%Y-%m-%d %H:%M:%S')
            user[arg] = date_str

def tran_to_float(user, *args):
    for arg in args:
        value = user[arg]
        user[arg] = float(value)


def get_rate(exchanges, currency):
    if currency == 'CNH':
        currency = 'CNY'
    if currency in exchanges:
        return exchanges[currency]
    else:
        raise ValueError("invalid currency")


def tran_currencys(users, currency_key, amount_key):
    request_data.get_exchanges()
    exchanges = request_data.get_exchanges()
    for user in users:
        currency = user[currency_key]
        rate = get_rate(exchanges, currency)
        user[amount_key] = float(user[amount_key]) * rate
        user[currency_key] = 'USD'

def tran_currency(user, currency_key, amount_key):
    request_data.get_exchanges()
    exchanges = request_data.get_exchanges()
    currency = user[currency_key]
    rate = get_rate(exchanges, currency)
    user[amount_key] = float(user[amount_key]) * rate
    user[currency_key] = 'USD'


def check_cache(user_id, cache):
    if cache :
        if cache["pid"] and not cache.has_key('p_type'):
            return None
        if cache.has_key('p_pid') and cache['p_pid'] and not cache.has_key('pp_type'):
            return None
        if cache.has_key('pp_pid') and cache['pp_pid'] and not cache.has_key('ppp_type'):
            return None
    return cache

def is_between(value, tup):
    if value >= tup[0] and value <= tup[1]:
        return True
    return False

def get_asset_start(amount):
    amount = float(amount)
    if is_between(amount, (0, 10000)):
        return 1.0
    elif is_between(amount, (10001, 50000)):
        return 1.5
    elif is_between(amount, (50001, 100000)):
        return 2.0
    elif is_between(amount, (100001, 500000)):
        return 2.5
    elif is_between(amount, (500001, 1000000)):
        return 3.0
    elif is_between(amount, (1000001, 5000000)):
        return 3.5
    elif is_between(amount, (5000001, 999999999)):
        return 4.0

def set_scripts_logging(_file_):
    log_filename = path.get_log_path(_file_)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_filename)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('[line:%(lineno)d] %(levelname)s %(message)s'))
    logging.getLogger().addHandler(console_handler)
    logging.info('\nlog_filename: {}'.format(log_filename))
    return log_filename

def pick_near_one(values, value):
    values = sorted(values)
    mid_index = len(values) / 2

    if len(values) == 2:
        return values[1]
    if len(values) == 1:
        return values[0]

    if value < values[mid_index]:
        near_one = pick_near_one(values[0:mid_index + 1] , value)
    else:
        near_one = pick_near_one(values[mid_index:], value)

    return near_one

if __name__ == '__main__':
    values = [5,3,7,9,2,0,4,5,6]
    value = 5
    near_one = pick_near_one(values, value)
    print 'debug'


