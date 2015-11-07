#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import time

dbPath = "wuPushes.sqlite"

def initDB():
  con = lite.connect(dbPath)
  with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Pushes")
    cur.execute("CREATE TABLE Pushes(Id INTEGER PRIMARY KEY, Title Text, Time Text, News Text, Deals Text, Content TEXT);")

def store(title, news, deals, content):
  curtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
  pushes =(title, curtime, news, deals, content)
  con = lite.connect(dbPath)
  con.text_factory = str
  with con:
    cur = con.cursor()
    cur.execute('''INSERT INTO Pushes(Title, Time, News, Deals, Content) VALUES(?,?,?,?,?)''', pushes)
    con.commit()
    lid = cur.lastrowid #The last Id of the inserted row
    #print lid
    return lid

def queryId(uId):
  con = lite.connect(dbPath)
  with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Pushes WHERE Id=:Id", {"Id": uId})
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
#updateTitle(1,'11月06日wu2198股市直播')
#updateTime(1,'2015-11-06 15:10:00')
#queryId(1)
