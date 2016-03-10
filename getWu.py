#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib
import re
import time
import socket
import getTodayUrl
import sendCloud
import handleData
from models import Push
from log import LogError
from log import LogGet
from log import LogSended
from log import LogGetSended

socket.setdefaulttimeout(5)

def getMesg(url) :
  html = ''
  lst = list()
  try :
    page = urllib.urlopen(url)
    html = page.read()
  except IOError,e :
    errno,errstr = sys.exc_info()[:2]
    curtime = time.strftime('%H:%M:%S',time.localtime(time.time()))
    LogError('\n\n-------------\nstart\n' + curtime)
    if errno == socket.timeout:
      LogError('There was a timeout')
    else :
      LogError('Some other socket error')

  if html == '':
    return lst
  lines = html.split('\n')
  start = 0
  end = 0
  findStart = False
  findEnd = False
  count = 0
  divCount = 0
  for line in lines :
    if findStart == False and '<!-- 正文开始 -->' in line :
      findStart = True
      start = count
    if '最新消息与数据' in line :
      start = count
    if findEnd == False and ('<!-- 正文结束 -->' in line ) : 
      findEnd = True
      end = count
      break
    count += 1
  for i in range(start,end+1) :
    lines[i] = lines[i].replace('&nbsp;',' ')
    #lines[i] = lines[i].replace('---&gt;','')  ##根据这个考虑分隔小时
    if "HREF" not in lines[i] :
      lines[i], num = re.subn(ur"<((?!>).)*>", "", lines[i])
    else :
      lines[i] = lines[i].replace('<div>','')
      lines[i] = lines[i].replace('</DIV>','')
      lines[i] = lines[i].replace('<span>','')
      lines[i] = lines[i].replace('</SPAN>','')
      lines[i] = lines[i].replace('<wbr>','')
      lines[i] = lines[i].replace('<p>','')
      lines[i] = lines[i].replace('</P>','')
      
    lines[i] = lines[i].strip() 
    #lines[i] = lines[i].replace('&lt;&lt;','<<')
    #lines[i] = lines[i].replace('&gt;&gt;','>>')
    #lines[i] = lines[i].replace('&#9733;','')
    #lines[i] = lines[i].replace('&amp;','&')
    ##if time and the content are placed seperately in two lines, then put time
    ## in the content's line
    if re.match(ur"^\d{1,2}:\d{2}$", lines[i]):
      lines[i+1] = lines[i] + '  ' + lines[i+1]
      lines[i] = ''
    if re.match(ur"^&lt;&lt;", lines[i]) and i > 0:
      lines[i-1] = lines[i-1] + '  ' + lines[i]
      lines[i] = ''
    #if (not re.match(ur"^\d{1,2}:\d{2}", lines[i]))  and ( not re.match(r"^\d{1}\.", lines[i])) :
    #  lines[i] = ''
  for i in range(start,end+1) :
    if lines[i] != '' :
      lst.append(lines[i])
      #print lines[i]
    #if lines[i].strip() != '':
      #print lines[i] + '\n'
  return lst

def isDeal(line) :
  if (re.match(r"^.*买进\d{1,2}%", line) or
      re.match(r"^.*再买\d{1,2}%", line) or
      re.match(r"^.*兑现\d{1,2}%", line) or
      re.match(r"^.*T出\d{1,2}%", line)  or
      re.match(r"^.*砍掉\d{1,2}%", line) or
      re.match(r"^.*出掉\d{1,2}%", line) or
      re.match(r"^.*减掉\d{1,2}%", line) or
      re.match(r"^.*减出\d{1,2}%", line) or
      re.match(r"^.*挂中\d{1,2}%", line) or
      re.match(r"^.*成交\d{1,2}%", line) or
      re.match(r"^.*减仓\d{1,2}%", line) or
      re.match(r"^.*加仓\d{1,2}%", line) or
      re.match(r"^.*接回\d{1,2}%", line) or
      re.match(r"^.*回补\d{1,2}%", line) ):
    return True
  return False

def init() :
  #需要考虑程序崩溃，重新启动能继续正常运行,邮件不重发
  lines = LogGetSended()
  length = len(lines)
  wuSendedLst = list()
  for i in range(length) :
    wuSendedLst.append(lines[i].strip('\n'))
  return wuSendedLst

def runEnd(url, sendedLst):
  if url == '' :
    return
  newLst = getMesg(url)
  date = time.strftime('%m月%d日',time.localtime(time.time()))
  h = time.localtime().tm_hour
  deals = listToStr(sendedLst)
  content = listToStr(newLst)
  title = ''
  if h == 11 :
    title = date + 'wu2198股市直播(上午篇)'
  else :
    title = date + 'wu2198股市直播'
  subject = title
  pushId = handleData.storePush(title, '', deals, content, url)
  push = Push(1, pushId, title, '', deals, content, url, subject) 
  sendCloud.send(push)
  #sendCloud.send(1, pushId, title, '', deals, content, url, subject) 
    
def listToStr(lst):
  ss = ''
  length = len(lst)
  for i in range(length):
    ss += lst[i] + '<br>'
  return ss

def runOnce(url, wuSendedLst, oldLst ) :
  if url == '':
    return
  newLst = getMesg(url)
  newLen = len(newLst)
  oldLen = len(oldLst)
  LogGet('oldLen:' + str(oldLen) + ' newLen:' + str(newLen))
  if newLen == 0 :
    return
  subject = ''
  LogGet('before if1')
  if newLen < oldLen :
    #中午是博客内容会改变，上午的没有直播
    del oldLst[:]
    oldLen = 0
  if newLen > oldLen :
    LogGet('\n\n---------------\nNew message:')
    for pos in range(oldLen, newLen):
      oldLst.append(newLst[pos])
    getNew = False
    for i in range(oldLen-3, newLen) :
      if i < 0:
        continue
      latestDeal = ''
      LogGet(newLst[i])
      if '中短线帐户' in newLst[i] :
        #if several deals occur at the same time, set the subject be the last deal
        for j in range(i-3,i) :
          if j < 0 :
            continue
          if re.match(r"^.*\d{1,2}%", newLst[j]) and newLst[j] not in wuSendedLst:
            if '中短线帐户' in newLst[j] :
              continue
            LogGet('New deal:' + newLst[j])
            getNew = True
            wuSendedLst.append(newLst[j])
            latestDeal += newLst[j] + '\n'
            ops = newLst[j].split(' ')
            if len(ops) > 1 :
              subject += ops[1] + ' '
            LogSended(newLst[j])
        if getNew :
          news = ''
          for hh in range(oldLen, newLen):
            news += newLst[hh] + '<br>'
          deals = listToStr(wuSendedLst)
          content = listToStr(newLst)
          date = time.strftime('%m月%d日', time.localtime(time.time()))
          title = date + 'wu2198股市直播更新'
          pushId = handleData.storePush(title, news, deals, content, url)
          push = Push(0, pushId, title, news, deals, content, url, subject) 
          sendCloud.send(push)
          #sendCloud.send(0, pushId, title, news, deals, content, url, subject)
    LogGet('after for 111')
    if getNew is False: #仓位暂时没更新，只更新交易内容，也要能判断出
      for i in range(oldLen, newLen):
        if isDeal(newLst[i]) and newLst[i] not in wuSendedLst :
          LogGet('########\n New Deal:' + newLst[i])
          getNew = True
          wuSendedLst.append(newLst[i])
          latestDeal = latestDeal + newLst[i] + '<br>'
          ops = newLst[i].split(' ')
          if len(ops) > 1 :
            subject = subject + ops[1] + ' '
          LogSended(newLst[i])
      if getNew :
        news = ''
        for hh in range(oldLen, newLen):
          news += newLst[hh] + '<br>'
        deals = listToStr(wuSendedLst)
        content = listToStr(newLst)
        date = time.strftime('%m月%d日', time.localtime(time.time()))
        title = date + 'wu2198股市直播更新'
        pushId = handleData.storePush(title, news, deals, content, url, subject)
        push = Push(0, pushId, title, news, deals, content, url, subject) 
        sendCloud.send(push)

  refreshTime =  "\n更新时间: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
  LogGet(refreshTime + '')
  LogGet('-----------------\n')

def run():
  #url = getTodayUrl.getUrl()  #url of wu's blog
  url = 'http://blog.sina.com.cn/s/blog_48874cec0102vx4s.html'
  if url == '' :
    return
  latestDeal = '暂无'
  oldLst = list()
  date = time.strftime('%Y%m%d', time.localtime(time.time()))
  wuSendedLst = init(date) # deaLst
  while True :
    runOnce(url, date, wuSendedLst, latestDeal, oldLst)
    time.sleep(10)

#run()

#lst = list()
#runEnd('http://blog.sina.com.cn/s/blog_48874cec0102w7nv.html',lst)
