#coding=utf-8
import getWu
import time
import sendWu
import getTodayUrl

startHour = 9
midHour = 11
midMinute = 40
stopHour = 15
stopWuMinute = 10

def out(str):
  print str + '\n'

sendWu.informMyself('程序启动')
while True :
  date = time.strftime('%Y%m%d',time.localtime(time.time()))
  logFile = open('./log/run_' + date + '.log','a')
  hour = time.localtime().tm_hour
  minute = time.localtime().tm_min
  logFile.write(str(hour) + ':' + str(minute) + '\n')
  logFile.close()
  isEnter = False
  if hour >= startHour and hour < stopHour :
    isEnter = True
    logFile = open('./log/run_' + date + '.log','a')
    logFile.write('\n\n\nEnterWu\n\n')
    sendWu.informMyself('开始wu2198')
    logFile.close()
    url = ''
    while(True) :
      url = getTodayUrl.getUrl()
      if url != 'error' :
        break
    sendedLst = getWu.init(date)
    oldLst = list()
    isEnd = False
    isMid = False
    while(isEnter) :
      #out('isEnter')
      getWu.runOnce(url, date, sendedLst, oldLst)
      #out('runonce ok')
      time.sleep(3)
      h = time.localtime().tm_hour
      m = time.localtime().tm_min
      s = time.localtime().tm_sec
      logFile = open('./log/run_' + date + '.log','a')
      logFile.write(str(h) + ':' + str(m) + ':' + str(s) + '\n')
      if not isMid and h == midHour and m == midMinute :
        getWu.runEnd(url)
        isMid = True
      if not isEnd and h == stopHour and m == stopWuMinute :
        isEnter = False
        getWu.runEnd(url)
        isEnd = True
        sendWu.informMyself('结束wu2198')
      logFile.close()
    
  time.sleep(300)

