#coding=utf-8
import requests, json
import time
from log import LogEmail

mailUrl = "http://sendcloud.sohu.com/webapi/mail.send_template.json"

apiFile = open('apiInfo.txt','r')
apiInfo = apiFile.readlines()
API_USER = apiInfo[0].strip()
API_KEY = apiInfo[1].strip()

def send(templateId, pushId, title, news, deals, content, url) :
  LogEmail('\n' + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()) )
  LogEmail('pushId:' + str(pushId) + '\n' + title+ '\nnews:\n' + news + '\ndeals:\n' 
    + deals + '\ncontent:' + content)
  userFile = open('users_wu.txt','r')
  toLst = userFile.readlines()
  toNum = len(toLst)
  for i in range(toNum):
    toLst[i] = toLst[i].strip()

  pushIdLst = list()
  titleLst = list()
  newsLst = list()
  dealsLst = list()
  contentLst = list()
  urlLst = list()

  for i in range(toNum) :
    pushIdLst.append(str(pushId))
    titleLst.append(title)
    newsLst.append(news)
    dealsLst.append(deals)
    contentLst.append(content)
    urlLst.append(url)

  templateName = ''
  sub_vars = ''
  if templateId == 0:
    templateName = 'template_wu'
    sub_vars = {
      'to': toLst,
      'sub':{
        '%id%': pushIdLst,
        '%title%': titleLst,
        '%news%':  newsLst,
        '%deals%': dealsLst,
        '%content%': contentLst,
        '%url%': urlLst,
        }
      }
  else :
    templateName = 'template_wu_all'
    sub_vars = {
      'to' : toLst,
      'sub':{
        '%id%': pushIdLst,
        '%title%' : titleLst,
        '%deals%' : dealsLst,
        '%content%': contentLst,
        '%url%': urlLst,
        }
      }

  params = {
    "api_user": API_USER,
    "api_key" : API_KEY,
    "template_invoke_name" : templateName,
    "substitution_vars" : json.dumps(sub_vars), 
    "from" : "wu@batch.wublogpush.com",
    "fromname" : "吴姐推送",
    "subject" : title,
    "resp_email_id": "true",
    }
  
  r = requests.post(mailUrl, files={}, data=params)
  LogEmail(r.text)

#send('大刘微博内容','http://www.imaibo.net/space/1954702')

