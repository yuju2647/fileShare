#!usr/bin/env python
# coding=utf-8

__author__ = 'yujun huang'

import requests
import json
import time

exchanges = None
last_update_time = 0


def get_exchanges():
    global exchanges
    global last_update_time
    now = time.time()
    if now - last_update_time >= 60 * 60 or last_update_time == 0:
        url = "https://api.itiger.com/stock_info/exchangeRate?access_token=q5EeYLVSlEDaxhEUUWjN4AQTq69W2M"
        req = requests.get(url, timeout=10)
        data = json.loads(req.text)
        exchanges = {}
        for item in data['items']:
            exchanges[item[0]] = item[1]
        last_update_time = time.time()
    return exchanges


def test():
    global last_check_time
    last_check_time = time.time()


if __name__ == '__main__':
    t = get_exchanges()
    test()
    time.sleep(3)
    test()
