#coding=utf-8
'''This module contains many functions that can log,
which could be used by other modules'''

#import sys
import time
import datetime

#reload(sys)
#sys.setdefaultencoding('utf-8')

def log_run(mesg):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_file = open('./log/' + date + '_run.log', 'a')
    log_file.write(mesg + '\n')
    log_file.close()

def log_error(mesg):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_file = open('./log/' + date + '_error.log', 'a')
    log_file.write(mesg + '\n')
    log_file.close()

def log_get(mesg):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_file = open('./log/' + date + '_get.log', 'a')
    log_file.write(mesg + '\n')
    log_file.close()

def log_sended(mesg):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_file = open('./log/' + date + '_sended.log', 'a')
    log_file.write(mesg + '\n')
    log_file.close()

def log_get_sended():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    sended_file = open('./log/' + date + '_sended.log', 'a')
    sended_file.close()
    sended_file = open('./log/' + date + '_sended.log', 'r')
    lines = sended_file.readlines()
    sended_file.close()
    return lines

def log_email(mesg):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_file = open('./log/' + date + '_email.log', 'a')
    log_file.write(mesg + '\n')
    log_file.close()

def log_update_addrlst(mesg):
    dtime = datetime.datetime.now()
    date = dtime.strftime('%Y%m%d')
    log_file = open('./log/' + date + '_update_addrlst.log', 'a')
    ctime = dtime.strftime('%m-%d %H:%M:%S  ')
    log_file.write(ctime + mesg + '\n')
    log_file.close()

def log_proxy(proxy):
    dtime = datetime.datetime.now()
    date = dtime.strftime('%Y%m%d')
    log_file = open('./log/' + date + '_proxy.log', 'a')
    log_file.write(proxy + '\n')
    log_file.close()
