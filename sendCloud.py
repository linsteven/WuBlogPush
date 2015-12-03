#coding=utf-8
import requests, json
import time
import os
from handleData import getUsers
from log import LogEmail
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

mailUrl = "http://api.sendcloud.net/apiv2/mail/sendtemplate"

API_USER = "linsteven_test"
API_KEY = os.environ.get("API_KEY")

def send(templateId, pushId, title, news, deals, content, url, subject='') :
  if subject == '':
    subject = title
  LogEmail('\n' + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()) )
  LogEmail('pushId:' + str(pushId) + '\n' + title+ '\nnews:\n' + news + '\ndeals:\n' 
    + deals + '\ncontent:' + content)
  usersLst = getUsers()
  toLst = list()
  unsubscribeUrlLst = list()
  pushIdLst = list()
  titleLst = list()
  newsLst = list()
  dealsLst = list()
  contentLst = list()
  urlLst = list()

  toNum = len(usersLst)
  for i in range(toNum):
    toLst.append(usersLst[i][0])
    unsubscribeUrlLst.append("http://wublogpush.com/unsubscribe/" + usersLst[i][1])
    pushIdLst.append(str(pushId))
    titleLst.append(title)
    newsLst.append(news)
    dealsLst.append(deals)
    contentLst.append(content)
    urlLst.append(url)
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
  if templateId == 0:
    templateName = 'template_wu'
  else :
    templateName = 'template_wu_all'
  params = {
    "apiUser": API_USER,
    "apiKey" : API_KEY,
    "templateInvokeName" : templateName,
    "xsmtpapi" : json.dumps(sub_vars), 
    "from" : "wu@batch.wublogpush.com",
    "fromName" : "吴姐推送",
    "subject" : subject,
    }
  
  r = requests.post(mailUrl, files={}, data=params)
  LogEmail(r.text)

#send('0', '1', 'wu2198股市直播', '', '', '', '')
