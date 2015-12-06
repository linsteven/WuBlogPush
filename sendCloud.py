#coding=utf-8
import requests, json
import time
import os
from handleData import getUsers
from models import Push
from log import LogEmail
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

mailUrl = "http://sendcloud.sohu.com/webapi/mail.send_template.json"

apiFile = open('apiInfo.txt','r')
apiInfo = apiFile.readlines()
API_USER = apiInfo[0].strip()
API_KEY = apiInfo[1].strip()

#def send(templateId, pushId, title, news, deals, content, url, subject='') :
def send(push):
  LogEmail('\n' + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()) )
  LogEmail('pushId:' + str(push.pushId) + '\n' + push.title+ '\nnews:\n'\
          + push.news + '\ndeals:\n' + push.deals + '\ncontent:' + push.content + '\nsubject:' + push.subject)
  apiKey = str(API_KEY)
  LogEmail(apiKey)
  LogEmail(API_USER)
  usersLst = getUsers()
  num = len(usersLst)
  onceNum = 100
  times = num/onceNum
  for i in range(times):
    sendOnce(push, usersLst, i*onceNum, (i+1)*onceNum)
  sendOnce(push, usersLst, times*onceNum, num) #send the remainders

def sendOnce(push, usersLst, start, end):
  if start >= end:
    return
  toLst = list()
  unsubscribeUrlLst = list()
  pushIdLst = list()
  titleLst = list()
  newsLst = list()
  dealsLst = list()
  contentLst = list()
  urlLst = list()

  for i in range(start, end):
    toLst.append(usersLst[i][0])
    unsubscribeUrlLst.append("http://wublogpush.com/unsubscribe/" + usersLst[i][1])
    pushIdLst.append(str(push.pushId))
    titleLst.append(push.title)
    newsLst.append(push.news)
    dealsLst.append(push.deals)
    contentLst.append(push.content)
    urlLst.append(push.originalUrl)
  sub_vars = {
    'to': toLst,
    'sub':{
      '%id%': pushIdLst,
      '%title%': titleLst,
      '%news%':  newsLst,
      '%deals%': dealsLst,
      '%content%': contentLst,
      '%url%': urlLst,
      '%%user_defined_unsubscribe_link%%' : unsubscribeUrlLst,
        }
      }

  templateName = ''
  if push.templateId == 0:
    templateName = 'template_wu'
  else :
    templateName = 'template_wu_all'
  params = {
    "api_user": API_USER,
    "api_key" : API_KEY,
    "from" : "wu@batch.wublogpush.com",
    "substitution_vars" : json.dumps(sub_vars), 
    "subject" : push.subject,
    "template_invoke_name" : templateName,
    "fromname" : "吴姐推送",
    }
  
  r = requests.post(mailUrl, files={}, data=params)
  LogEmail(r.text)

#push = Push('0', '1', 'wu2198股市直播', '', '', '', '')
#send(push)
