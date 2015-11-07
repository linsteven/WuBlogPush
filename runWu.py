#coding=utf-8
import getWu
import time
import sendWu
import getTodayUrl
from log import LogRun

startHour = 9
midHour = 11
midMinute = 40
stopHour = 15
stopWuMinute = 10

LogRun('程序启动')

while True :
  hour = time.localtime().tm_hour
  minute = time.localtime().tm_min
  LogRun(str(hour) + ':' + str(minute))
  isEnter = False
  if hour >= startHour and hour < stopHour :
    isEnter = True
    LogRun('开始wu2198')
    url = ''
    while(True) :
      url = getTodayUrl.getUrl()
      if url != 'error' :
        break
    LogRun('url=' + url)
    sendedLst = getWu.init()
    oldLst = list()
    isEnd = False
    isMid = False
    while(isEnter) :
      getWu.runOnce(url, sendedLst, oldLst)
      time.sleep(2)
      h = time.localtime().tm_hour
      m = time.localtime().tm_min
      s = time.localtime().tm_sec
      LogRun(str(h) + ':' + str(m) + ':' + str(s) )
      if not isMid and h == midHour and m == midMinute :
        getWu.runEnd(url, sendedLst)
        isMid = True
      if not isEnd and h == stopHour and m == stopWuMinute :
        isEnter = False
        getWu.runEnd(url, sendedLst)
        isEnd = True
        LogRun('结束wu2198')
    
  time.sleep(300)

