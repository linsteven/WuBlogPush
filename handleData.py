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

def storePush(title, news, deals, content, url):
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
  pushes =(email, token, curtime, True, curtime, False, None)
  con = lite.connect(dbPath)
  con.text_factory = str
  with con:
    cur = con.cursor()
    cur.execute('''INSERT INTO users(email,token,subscribed_on, \
            confirmed,confirmed_on,unsubscribed,unsubscribed_on) \
            VALUES(?,?,?,?,?,?,?)''', pushes)
    con.commit()
    lid = cur.lastrowid #The last Id of the inserted row
    return lid

def getUsers():
  con = lite.connect(dbPath)
  with con:
    cur = con.cursor()
    cur.execute("SELECT email,token FROM users WHERE confirmed='1' AND unsubscribed='0'")
    con.commit()
    rows = cur.fetchall()
    return rows
  return null

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
#queryId(1)
#queryUserId(2)
#getUsers()
