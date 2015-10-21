#coding: utf-8
#获取wu2918每天分析文章的url，通过博客目录获取
# from http://blog.sina.com.cn/s/articlelist_1216826604_0_1.html

# <div class="articleCell SG_j_linedot1"> 之后的第四行是
# 文章名，从中找符合今天日期的文章，并提取URl
# 思路是：先找到从符合条件的<div ..>所在行，记录行号，找到开始的10个即可；
#         然后即可找匹配日期的

import urllib
import re
import time
import socket
from log import LogError

listUrl = "http://blog.sina.com.cn/s/articlelist_1216826604_0_1.html"

socket.setdefaulttimeout(5)

def getUrl() :
#if True :
  try :
    page = urllib.urlopen(listUrl)
    html = page.read()
  except IOError,e :
    errno,errstr = sys.exc_info()[:2]
    curtime = time.strftime('%H:%M:%S',time.localtime(time.time()))
    LogError('\n\n-------------\ngetTodayUrl error\n' + curtime)
    if errno == socket.timeout:
      LogError('There was a timeout')
    else :
      LogError('Some other socket error')
    return 'error'
  lines= html.split('\n')
  numlst = list()
  i = 0
  for line in lines :
    if '''<div class="articleCell SG_j_linedot1">''' in line :
      numlst.append(i)
      if len(numlst) == 20 :
        break
    i += 1
  #have found 10 articles
  month = time.localtime().tm_mon
  day = time.localtime().tm_mday
  title = str(month) +'月' + str(day) + '日' 
  #print title
  goodline = ''
  flag = False
  for k in range(0, 20) :
    num = numlst[k] + 4
    if title in lines[num] :
      goodline = lines[num]
      flag = True
      break
  url = ''
  if flag :
    pos = goodline.find('''href="''')
    goodline = goodline[pos+6:]
    url = goodline.split('''">''')[0]
    #print 'Today\'s url :' + url
  return url

#print getUrl()
