#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import time
import datetime

dbPath = "wublogpush.sqlite"

def initDB():
  con = lite.connect(dbPath)
  with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS pushes")
    cur.execute("CREATE TABLE pushes(id INTEGER PRIMARY KEY, title Text, \
            time Text, news Text, deals Text, content TEXT, url Text);")
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY,email Text,token Text,\
            subscribed_on DateTime, confirmed Boolean, confirmed_on DateTime, \
            unsubscribed Boolean, unsubscribed_on DateTime);")

def store(title, news, deals, content, url):
  curtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
  pushes =(title, curtime, news, deals, content, url)
  con = lite.connect(dbPath)
  con.text_factory = str
  with con:
    cur = con.cursor()
    cur.execute('''INSERT INTO pushes(title, time, news, deals, content, url) \
            VALUES(?,?,?,?,?,?)''', pushes)
    con.commit()
    lid = cur.lastrowid #The last Id of the inserted row
    #print lid
    return lid

def storeUser(email, token):
  curtime = datetime.datetime.now()
  pushes =(email, token, curtime, False, curtime, False, None)
  con = lite.connect(dbPath)
  con.text_factory = str
  with con:
    cur = con.cursor()
    cur.execute('''INSERT INTO users(email,token,subscribed_on, \
            confirmed,confirmed_on,unsubscribed,unsubscribed_on) \
            VALUES(?,?,?,?,?,?,?)''', pushes)
    con.commit()
    lid = cur.lastrowid #The last Id of the inserted row
    #print lid
    return lid

def queryId(uId):
  con = lite.connect(dbPath)
  with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM pushes WHERE Id=:Id", {"Id": uId})
    con.commit()
    row = cur.fetchone()
    for i in range(len(row)):
      print row[i]

def queryUserId(uId):
  con = lite.connect(dbPath)
  with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE Id=:Id", {"Id": uId})
    con.commit()
    row = cur.fetchone()
    for i in range(len(row)):
      print row[i]
def updateTitle(uId, uTitle):
  con = lite.connect(dbPath)
  con.text_factory = str
  with con:
    cur = con.cursor()
    cur.execute("UPDATE Pushes SET Title=? WHERE Id=?", (uTitle, uId)) 
    con.commit()
    print "Number of rows updated: %d" % cur.rowcount

def updateTime(uId, uTime):
  con = lite.connect(dbPath)
  con.text_factory = str
  with con:
    cur = con.cursor()
    cur.execute("UPDATE Pushes SET Time=? WHERE Id=?", (uTime, uId)) 
    con.commit()
    print "Number of rows updated: %d" % cur.rowcount

#initDB()
#store('csava', 'fefew', 'fesaf', 'fwfweg','http://sf')
#updateTitle(1,'11月06日wu2198股市直播')
#updateTime(1,'2015-11-06 15:10:00')
#queryId(1)
#print storeUser('yinfs@fs.com')
#queryUserId(2)
#queryUserId(3)
#queryUserId(5)
