#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

dbPath = "wuPushes.sqlite"

def initDB():
  con = lite.connect(dbPath)
  with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Pushes")
    cur.execute("CREATE TABLE Pushes(Id INTEGER PRIMARY KEY, Title Text, News Text, Deals Text, Content TEXT);")

def store(title, news, deals, content):
  pushes =(title, news, deals, content)
  con = lite.connect(dbPath)
  con.text_factory = str
  with con:
    cur = con.cursor()
    #cur.execute("INSERT INTO Pushes(Title, News, Deals,Content) VALUES(" + title + "," +  news "," +  deals + "," +  content + ");")
    cur.execute('''INSERT INTO Pushes(Title, News, Deals, Content) VALUES(?,?,?,?)''', pushes)
    con.commit()
    lid = cur.lastrowid #The last Id of the inserted row
    print lid
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

def update(uId, uTitle):
  con = lite.connect(dbPath)
  con.text_factory = str
  with con:
    cur = con.cursor()
    cur.execute("UPDATE Pushes SET Title=? WHERE Id=?", (uTitle, uId)) 
    con.commit()
    print "Number of rows updated: %d" % cur.rowcount

#initDB()
#update(1,'11月06日wu2198股市直播')
#queryId(1)
