#coding=utf-8
import sys
import time
import datetime


#This module contains many functions that can log,
#which could be used by other modules

def LogRun(mesg) :
  date = time.strftime('%Y%m%d',time.localtime(time.time()))
  logFile = open('./log/run_' + date + '.log','a')
  logFile.write(mesg + '\n')
  logFile.close()

def LogError(mesg) :
  date = time.strftime('%Y%m%d',time.localtime(time.time()))
  logFile = open('./log/error_' + date + '.log', 'a')
  logFile.write(mesg + '\n')
  logFile.close()

def LogGet(mesg) :
  #reload(sys)
  #sys.setdefaultencoding('utf8') 
  date = time.strftime('%Y%m%d',time.localtime(time.time()))
  logFile = open('./log/get_' + date + '.log', 'a')
  logFile.write(mesg + '\n')
  logFile.close()

def LogSended(mesg) :
  #reload(sys)
  #sys.setdefaultencoding('utf8') 
  date = time.strftime('%Y%m%d',time.localtime(time.time()))
  logFile = open('./log/sended_' + date + '.log','a')
  logFile.write(mesg + '\n')
  logFile.close()

def LogGetSended() :
  #reload(sys)
  #sys.setdefaultencoding('utf8') 
  date = time.strftime('%Y%m%d',time.localtime(time.time()))
  sendedFile = open('./log/sended_' + date + '.log','a')
  sendedFile.close()
  sendedFile = open('./log/sended_' + date + '.log','r')
  lines = sendedFile.readlines()
  sendedFile.close()
  return lines

def LogEmail(mesg) :
  date = time.strftime('%Y%m%d',time.localtime(time.time()))
  logFile = open('./log/email_' + date + '.log','a')
  logFile.write(mesg + '\n')
  logFile.close()

def LogUpdateAddrLst(mesg) :
  dt = datetime.datetime.now()
  date = dt.strftime('%Y%m%d')
  logFile = open('./log/update_addrlst_' + date + '.log','a')
  ctime = dt.strftime('%m-%d %H:%M:%S  ')
  logFile.write(ctime + mesg + '\n')
  logFile.close()
