#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import time
import datetime

dbpath = "wublogpush.sqlite"

def init_db():
    con = lite.connect(dbpath)
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS pushes")
        #add changes
        cur.execute("CREATE TABLE pushes(id INTEGER PRIMARY KEY, title Text, \
                time Text, news Text, deals Text, content TEXT, url Text);")
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY,email Text,token Text,\
                subscribed_on DateTime, confirmed Boolean, confirmed_on DateTime, \
                unsubscribed Boolean, unsubscribed_on DateTime);")

def store_push(title, news, deals, changes, content, url):
    curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    pushes = (title, curtime, news, deals, changes, content, url)
    con = lite.connect(dbpath)
    con.text_factory = str
    with con:
        cur = con.cursor()
        cur.execute('''INSERT INTO pushes(title, time, news, deals, changes, content, url) \
                VALUES(?,?,?,?,?,?,?)''', pushes)
        con.commit()
        lid = cur.lastrowid #The last Id of the inserted row
        #print lid
        return lid

def store_user(email, token):
    curtime = datetime.datetime.now()
    pushes = (email, token, curtime, True, curtime, False, None)
    con = lite.connect(dbpath)
    con.text_factory = str
    with con:
        cur = con.cursor()
        cur.execute('''INSERT INTO users(email,token,subscribed_on, \
                confirmed,confirmed_on,unsubscribed,unsubscribed_on) \
                VALUES(?,?,?,?,?,?,?)''', pushes)
        con.commit()
        lid = cur.lastrowid #The last Id of the inserted row
        return lid

def print_users():
    con = lite.connect(dbpath)
    with con:
        cur = con.cursor()
        cur.execute("SELECT email,token FROM users WHERE confirmed='1' AND unsubscribed='0'")
        con.commit()
        rows = cur.fetchall()
        #userLst = getUsers()
        length = len(rows)
        for i in range(length):
            print rows[i][0]
        #return rows
    #return null

def get_users():
    con = lite.connect(dbpath)
    with con:
        cur = con.cursor()
        cur.execute("SELECT email,token FROM users WHERE confirmed='1' AND unsubscribed='0'")
        con.commit()
        rows = cur.fetchall()
        return rows
    return []

def query_id(uid):
    con = lite.connect(dbpath)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM pushes WHERE Id=:Id", {"Id": uid})
        con.commit()
        row_lst = cur.fetchone()
        for item in row_lst:
            print item
        print 'length of row:', len(row_lst)

def query_all_users():
    con = lite.connect(dbpath)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        con.commit()
        rows = cur.fetchall()
        for row in rows:
            for item in row:
                print item
            print ""

def query_all_pushes():
    con = lite.connect(dbpath)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM pushes")
        con.commit()
        rows = cur.fetchall()
        for row in rows:
            for item in row:
                print item
            print ""

def query_user_id(uid):
    con = lite.connect(dbpath)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE Id=:Id", {"Id": uid})
        con.commit()
        row = cur.fetchone()
        for item in row:
            print item

def update_title(uid, utitle):
    con = lite.connect(dbpath)
    con.text_factory = str
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Pushes SET Title=? WHERE Id=?", (utitle, uid))
        con.commit()
        print "Number of rows updated: %d" % cur.rowcount

def update_time(uid, utime):
    con = lite.connect(dbpath)
    con.text_factory = str
    with con:
        cur = con.cursor()
        cur.execute("UPDATE pushes SET Time=? WHERE Id=?", (utime, uid))
        con.commit()
        print "Number of rows updated: %d" % cur.rowcount

def add_column():
    con = lite.connect(dbpath)
    cur = con.cursor()
    cur.execute("alter table pushes add column `changes` Text")

#queryUserId(1)
#queryAllUsers()
#addColumn()
#queryAllPushes()
#printUsers()
