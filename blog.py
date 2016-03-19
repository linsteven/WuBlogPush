#coding: utf-8
"""获取wu2918每天分析文章的url，通过博客目录获取
from http://blog.sina.com.cn/s/articlelist_1216826604_0_1.html

<div class="articleCell SG_j_linedot1"> 之后的第四行是
文章名，从中找符合今天日期的文章，并提取URl
思路是：先找到从符合条件的<div ..>所在行，记录行号，找到开始的10个即可;
然后即可找匹配日期的"""

import urllib
import time
import socket
import sys
from log import log_error


socket.setdefaulttimeout(5)
GET_NUM = 20 # get 20 articles at first

def get_items():
    """get lines that contains titles and urls
       which according to the catalogue of wu2198's blog.
       numlst stores the index of the lines that selected"""

    list_url = "http://blog.sina.com.cn/s/articlelist_1216826604_0_1.html"
    try:
        page = urllib.urlopen(list_url)
        html = page.read()
    except IOError:
        errno = sys.exc_info()[:1]
        curtime = time.strftime('%H:%M:%S', time.localtime(time.time()))
        log_error('\n\n-------------\ngetTodayUrl error\n' + curtime)
        if errno == socket.timeout:
            log_error('There was a timeout')
        else:
            log_error('Some other socket error')
        return '', ''
    lines = html.split('\n')
    numlst = list()
    i = 0
    for line in lines:
        if '''<div class="articleCell SG_j_linedot1">''' in line:
            numlst.append(i)
            if len(numlst) == GET_NUM:
                break
        i += 1
    return lines, numlst

def get_url(lines, numlst, keywords):
    """get titles and urls from the chosen lines"""

    flag = False
    url = ''
    for k in range(0, GET_NUM):
        num = numlst[k] + 4
        if keywords in lines[num]:
            goodline = lines[num]
            flag = True
            break
    if flag:
        pos = goodline.find('''href="''')
        goodline = goodline[pos+6:]
        url = goodline.split('''">''')[0]
    return url

def get_today_url():
    """get the live urls"""

    lines, numlst = get_items()
    if not lines:
        return ''
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday
    date = str(month) +'月' + str(day) + '日'
    url = get_url(lines, numlst, date)
    return url
