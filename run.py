#coding=utf-8
'''start the mail service'''

import datetime
import time
import blog
from log import log_run
from get_news import run_once
from get_news import run_end
from get_news import init

start_hour = 9
mid_hour = 11
mid_mintue = 40
stop_hour = 15
stop_minute = 10

def get_hour_minute():
    t_hour = time.localtime().tm_hour
    t_minute = time.localtime().tm_min
    log_run(str(t_hour) + ':' + str(t_minute))
    return t_hour, t_minute

while True:
    is_enter = False
    hour, minute = get_hour_minute()
    if hour >= start_hour and hour < stop_hour:
        url = blog.get_today_url()
        if url == '':
            time.sleep(30)
            continue
        log_run('start service, url = ' + url)
        sended_lst = init()
        old_lst = list()
        is_end = False
        is_mid = False
        is_enter = True
        proxy_index = 0
        update_time = datetime.datetime.now()
        while is_enter:
            proxy_index, update_time = run_once(url, sended_lst, old_lst,
                                                proxy_index, update_time)
            time.sleep(60)
            hour, minute = get_hour_minute()
            if not is_mid and hour == mid_hour and minute == mid_mintue:
                run_end(url, proxy_index)
                is_mid = True
            if not is_end and hour == stop_hour and minute == stop_minute:
                is_enter = False
                run_end(url, proxy_index)
                is_end = True
                log_run('the end')
    time.sleep(300)

