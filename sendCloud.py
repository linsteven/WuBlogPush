#coding=utf-8
import requests, json
import time
#from log import LogEmail

mailUrl = "http://sendcloud.sohu.com/webapi/mail.send_template.json"

apiFile = open('apiInfo.txt','r')
apiInfo = apiFile.readlines()
API_USER = apiInfo[0].strip()
API_KEY = apiInfo[1].strip()

def send(newDeals, content, url) :
  LogEmail('\n' + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()) )
  LogEmail(content + '\n' + url)
  userFile = open('users_wu.txt','r')
  toLst = userFile.readlines()
  toNum = len(toLst)
  for i in range(toNum):
    toLst[i] = toLst[i].strip()
  
  weiboLst = list()
  urlLst = list()
  for i in range(toNum) :
    weiboLst.append(content)
    urlLst.append(url)

  sub_vars = {
    'to': toLst,
    'sub':{
      '%weibo%': weiboLst,
      '%url%': urlLst,
      }
    }

  params = {
    "api_user": API_USER,
    "api_key" : API_KEY,
    "template_invoke_name" : "template_wu",
    "substitution_vars" : json.dumps(sub_vars), 
    "from" : "wu@batch.wublogpush.com",
    "fromname" : "wu推送",
    "subject" : "wu直播更新",
    "resp_email_id": "true",
    }
  
  r = requests.post(mailUrl, files={}, data=params)
  LogEmail(r.text)

#send('大刘微博内容','http://www.imaibo.net/space/1954702')

