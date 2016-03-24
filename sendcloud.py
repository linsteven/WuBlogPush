#coding=utf-8
import json
import time
import requests
from handle_data import get_users
from models import Push
from log import log_email

mail_url = "http://sendcloud.sohu.com/webapi/mail.send_template.json"

api_file = open('api_info.txt', 'r')
api_info = api_file.readlines()
API_USER = api_info[0].strip()
API_KEY = api_info[1].strip()

def send(push):
    log_email('\n' + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()))
    log_email('push_id:' + str(push.push_id) + '\n' + push.title+ '\nnews:\n'\
            + push.news + '\ndeals:\n' + push.deals + '\nchanges:\n' +\
            push.changes + '\ncontent:' + push.content + '\nsubject:' + push.subject)
    users_lst = get_users()
    #users_lst = list()
    #users_lst.append(('example@qq.com', 'sgsgerhbrt'))
    num = len(users_lst)
    once_num = 100
    times = num/once_num
    for i in range(times):
        send_once(push, users_lst, i*once_num, (i+1)*once_num)
    send_once(push, users_lst, times*once_num, num) #send the remainders

def get_sub_vars(push, users_lst, start, end):
    to_lst = list()
    unsubscribe_url_lst = list()
    push_id_lst = list()
    title_lst = list()
    news_lst = list()
    deals_lst = list()
    changes_lst = list()
    content_lst = list()
    url_lst = list()
    for i in range(start, end):
        to_lst.append(users_lst[i][0])
        unsubscribe_url_lst.append("http://wublogpush.com/unsubscribe/" + users_lst[i][1])
        push_id_lst.append(str(push.push_id))
        title_lst.append(push.title)
        news_lst.append(push.news)
        deals_lst.append(push.deals)
        changes_lst.append(push.changes)
        content_lst.append(push.content)
        url_lst.append(push.original_url)
    sub_vars = {
        'to': to_lst,
        'sub':{
            '%id%': push_id_lst,
            '%title%': title_lst,
            '%news%':  news_lst,
            '%deals%': deals_lst,
            '%changes%': changes_lst,
            '%content%': content_lst,
            '%url%': url_lst,
            '%%user_defined_unsubscribe_link%%' : unsubscribe_url_lst,
            }
        }
    return sub_vars


def send_once(push, users_lst, start, end):
    if start >= end:
        return
    sub_vars = get_sub_vars(push, users_lst, start, end)
    template_name = ''
    if push.template_id == 0:
        template_name = 'template_wu_new'
    else:
        template_name = 'template_wu_all_new'
    params = {
        "api_user": API_USER,
        "api_key" : API_KEY,
        "from" : "wu@batch.wublogpush.com",
        "substitution_vars" : json.dumps(sub_vars),
        "subject" : push.subject,
        "template_invoke_name" : template_name,
        "fromname" : "小王子推送",
        }
    req = requests.post(mail_url, files={}, data=params)
    log_email(req.text)

#push = Push('1', '1', 'wu2198股市直播', '', '', '', '', '')
#send(push)
