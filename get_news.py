#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import sys
import urllib
import urllib2
import re
import time
import socket
import sendcloud
import handle_data
from models import Push
from log import log_error
from log import log_get
from log import log_sended
from log import log_get_sended

socket.setdefaulttimeout(5)
POSITION_TAG = '中短线帐户'
proxy_lst = list()
with open("proxy.txt") as proxy_file:
    for proxy_line in proxy_file:
        proxy_lst.append(proxy_line.strip())

def get_true_str(line):
    '''remove html tags'''
    line = line.replace('&nbsp;', ' ')
    #line = line.replace('---&gt;', '')  ##根据这个考虑分隔小时
    if "HREF" not in line:
        line, num = re.subn(ur"<((?!>).)*>", "", line)
    else:
        line = line.replace('<div>', '')
        line = line.replace('</DIV>', '')
        line = line.replace('<span>', '')
        line = line.replace('</SPAN>', '')
        line = line.replace('<wbr>', '')
        line = line.replace('<p>', '')
        line = line.replace('</P>', '')
    line = line.strip()
    return line

def find_start_end(lines):
    start = 0
    end = 0
    find_start = False
    find_end = False
    count = 0
    for line in lines:
        if not find_start and '<!-- 正文开始 -->' in line:
            find_start = True
            start = count
        if '最新消息与数据' in line:
            start = count
        if not find_end and '<!-- 正文结束 -->' in line:
            find_end = True
            end = count
            break
        count += 1
    return start, end

def get_content_lst(lines, start, end):
    lst = list()
    for i in range(start, end + 1):
        ##if time and the content are placed seperately in two lines, then put time
        ## in the content's line
        lines[i] = get_true_str(lines[i])
        if re.match(ur"^\d{1,2}:\d{2}$", lines[i]):
            lines[i+1] = lines[i] + '  ' + lines[i+1]
            lines[i] = ''
        if re.match(ur"^&lt;&lt;", lines[i]) and i > 0:
            lines[i-1] = lines[i-1] + '  ' + lines[i]
            lines[i] = ''
    for i in range(start, end+1):
        if not lines[i]:
            lst.append(lines[i])
    return lst

def get_html(url, proxy_index, is_timeout):
    html = ''
    if is_timeout:
        proxy_index = (proxy_index + 1)%(len(proxy_lst) + 1)
    try:
        if proxy_index == 0:
            page = urllib.urlopen(url)
        else:
            proxy = urllib2.ProxyHandler({'http': proxy_lst[proxy_index - 1]})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            page = urllib2.urlopen(url)
        html = page.read()
    except IOError:
        errno = sys.exc_info()[:1]
        curtime = time.strftime('%H:%M:%S', time.localtime(time.time()))
        log_error('\n\n-------------\nstart\n' + curtime)
        if errno == socket.timeout:
            log_error('There was a timeout')
        else:
            log_error('Some other socket error')
    return html, proxy_index

def get_mesg(url, proxy_index, is_timeout=False):
    html, proxy_index = get_html(url, proxy_index, is_timeout)
    if html == '':
        return []
    lines = html.split('\n')
    start, end = find_start_end(lines)
    return get_content_lst(lines, start, end), proxy_index

def is_deal(line):
    if (re.match(r"^.*买进\d{1,2}%", line) or
            re.match(r"^.*加仓\d{1,2}%", line) or
            re.match(r"^.*增仓\d{1,2}%", line) or
            re.match(r"^.*接回\d{1,2}%", line) or
            re.match(r"^.*回补\d{1,2}%", line) or
            re.match(r"^.*再买\d{1,2}%", line) or
            re.match(r"^.*再接\d{1,2}%", line) or
            re.match(r"^.*挂中\d{1,2}%", line) or
            re.match(r"^.*成交\d{1,2}%", line) or
            re.match(r"^.*兑现\d{1,2}%", line) or
            re.match(r"^.*T出\d{1,2}%", line)  or
            re.match(r"^.*砍掉\d{1,2}%", line) or
            re.match(r"^.*出\d{1,2}%", line) or
            re.match(r"^.*出掉\d{1,2}%", line) or
            re.match(r"^.*走掉\d{1,2}%", line) or
            re.match(r"^.*割掉\d{1,2}%", line) or
            re.match(r"^.*减掉\d{1,2}%", line) or
            re.match(r"^.*再减\d{1,2}%", line) or
            re.match(r"^.*减持\d{1,2}%", line) or
            re.match(r"^.*减出\d{1,2}%", line) or
            re.match(r"^.*减仓\d{1,2}%", line)):
        return True
    return False

def init():
    #需要考虑程序崩溃，重新启动能继续正常运行,邮件不重发
    lines = log_get_sended()
    length = len(lines)
    sended_lst = list()
    for i in range(length):
        sended_lst.append(lines[i].strip('\n'))
    return sended_lst

def save_position(position):
    pos_file = open('./position.txt', 'w+')
    pos_file.write(position)
    pos_file.close()

def get_position():
    pos_file = open('./position.txt', 'r')
    position_str = pos_file.read()
    pos_file.close()
    return position_str

def get_final_position(new_lst):
    length = len(new_lst)
    position = ''
    for i in range(length-1, -1, -1):
        if POSITION_TAG in new_lst[i] and re.match(r"^.*[^0-9.]\d{1,2}%", new_lst[i]):
            position = new_lst[i].strip().split(' ')[-1]
            break
    return position

def run_end(url, proxy_index):
    if url == '':
        return
    new_lst, proxy_index = get_mesg(url, proxy_index)
    old_position = get_position()
    new_position = get_final_position(new_lst)
    if new_position == '':
        new_position = old_position
    changes = '昨日： ' + old_position + '<br>'
    date = time.strftime('%m月%d日', time.localtime(time.time()))
    hour = time.localtime().tm_hour
    deals_lst = get_all_deals(new_lst)
    deals = list_to_str(deals_lst)
    content = list_to_str(new_lst)
    title = ''
    if hour == 11:
        title = date + 'wu2198股市直播(上午篇)'
        changes += '上午： ' + new_position
    else:
        title = date + 'wu2198股市直播'
        changes += '今日： ' + new_position
        save_position(new_position)
    subject = title
    push_id = handle_data.store_push(title, '', deals, changes, content, url)
    push = Push(1, push_id, title, '', deals, changes, content, url, subject)
    sendcloud.send(push)

def is_position(line):
    if POSITION_TAG in line and re.match(r"^.*[^0-9.]\d{1,3}%", line):
        return True
    return False

def find_deals(deals_lst, new_lst, start, end):
    if start < 0:
        start = 0
    new_start = start
    for i in range(start, end):
        if POSITION_TAG in new_lst[i]:
            new_start = i
    for i in range(new_start, end):
        if (POSITION_TAG not in new_lst[i] and
                re.match(r"^.*[^0-9.]\d{1,2}%", new_lst[i])):
            deals_lst.append(new_lst[i])
    #return deals_lst

def get_all_deals(new_lst):
    '''deals must be in front of position or at the end,
    position means 仓位'''

    deals_lst = list()
    length = len(new_lst)
    for i in range(length):
        if is_position(new_lst[i]):
            find_deals(deals_lst, new_lst, i-5, i)
    for item in new_lst[-3:]:
        if is_deal(item) and item not in deals_lst:
            deals_lst.append(item)
    return deals_lst

def list_to_str(lst):
    newstr = ''
    for item in lst:
        newstr += item + '<br>'
    return newstr

def judge_is_timeout(update_time):
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    is_noon = False
    if (hour == 11 and minute > 30) or hour == 12 or (hour == 1 and minute < 10):
        is_noon = True
    now_time = datetime.datetime.now()
    diff_secs = (now_time - update_time).seconds
    if not is_noon and diff_secs > 30 * 60:
        return True
    return False

def update_sended(item):
    '''update sended file'''
    log_get('New deal:' + item)
    log_sended(item)

def get_added_lst(old_lst, new_lst): #should be tested
    added_lst = list()
    for item in new_lst:
        if item not in old_lst:
            added_lst.append(item)
            log_get(item)
    return added_lst

def get_deal_lst(added_lst):
    deal_lst = list()
    length = len(added_lst)
    pos = 0
    for i in range(length):
        if is_position(added_lst[i]):
            pos = i
    if pos == 0:
        for item in added_lst:
            if is_deal(item):
                deal_lst.append(item)
                update_sended(item)
    else:
        for i in range(pos):
            if (re.match(r"^.*[^0-9.]\d{1,2}%", added_lst[i]) and
                    not is_position(added_lst[i])):
                deal_lst.append(added_lst[i])
                update_sended(item)
    return deal_lst

def split_deal_lst(deal_lst):
    lst = list()
    for item in deal_lst:
        lst.append(item.split(' ')[-1])
    return lst

def log_refresh_time():
    refresh_time = "\n更新时间: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    log_get(refresh_time + '')
    log_get('-----------------\n')

def save_and_send(url, new_deal_lst, added_lst, new_lst):
    subject = "， ".join(split_deal_lst(new_deal_lst))
    news = list_to_str(added_lst)
    deals = list_to_str(get_all_deals(new_lst))
    content = list_to_str(new_lst)
    date = time.strftime('%m月%d日', time.localtime(time.time()))
    title = date + 'wu2198股市直播更新'
    changes = ''
    push_id = handle_data.store_push(title, news, deals, changes, content, url)
    push = Push(0, push_id, title, news, deals, changes, content, url, subject)
    sendcloud.send(push)

def run_once(url, sended_lst, old_lst, proxy_index, update_time):
    if url == '':
        return
    is_timeout = judge_is_timeout(update_time)
    new_lst, proxy_index = get_mesg(url, proxy_index, is_timeout)
    new_len = len(new_lst)
    if new_len == 0:
        return
    added_lst = get_added_lst(old_lst, new_lst)
    if not added_lst:
        return
    old_lst.extend(added_lst)
    update_time = datetime.datetime.now()
    new_deal_lst = get_deal_lst(added_lst)
    if not new_deal_lst:
        log_refresh_time()
        return proxy_index, update_time
    sended_lst.extend(new_deal_lst) #update_sended_lst
    save_and_send(url, new_deal_lst, added_lst, new_lst)
    log_refresh_time()

#lst = list()
#run_end('http://blog.sina.com.cn/s/blog_48874cec0102wfkk.html',lst)
