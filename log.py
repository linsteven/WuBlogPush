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
    log_file = open('./log/run_' + date + '.log', 'a')
    log_file.write(mesg + '\n')
    log_file.close()

def log_error(mesg):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_file = open('./log/error_' + date + '.log', 'a')
    log_file.write(mesg + '\n')
    log_file.close()

def log_get(mesg):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_file = open('./log/get_' + date + '.log', 'a')
    log_file.write(mesg + '\n')
    log_file.close()

def log_sended(mesg):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_file = open('./log/sended_' + date + '.log', 'a')
    log_file.write(mesg + '\n')
    log_file.close()

def log_get_sended():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    sended_file = open('./log/sended_' + date + '.log', 'a')
    sended_file.close()
    sended_file = open('./log/sended_' + date + '.log', 'r')
    lines = sended_file.readlines()
    sended_file.close()
    return lines

def log_email(mesg):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_file = open('./log/email_' + date + '.log', 'a')
    log_file.write(mesg + '\n')
    log_file.close()

def log_update_addrlst(mesg):
    dtime = datetime.datetime.now()
    date = dtime.strftime('%Y%m%d')
    log_file = open('./log/update_addrlst_' + date + '.log', 'a')
    ctime = dtime.strftime('%m-%d %H:%M:%S  ')
    log_file.write(ctime + mesg + '\n')
    log_file.close()
