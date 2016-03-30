#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import time
import datetime
import re

dbpath = "wublogpush.sqlite"


def get_position(content):
    new_lst = content.split('<br>')
    length = len(new_lst)
    position = ''
    for i in range(length-1, -1, -1):
        if u"中短线帐户" in new_lst[i] and re.match(ur"^.*[^0-9.]\d{1,2}%", new_lst[i]):
            position = new_lst[i].strip().split(' ')[-1]
            break
    return position

def init_db():
    con = lite.connect(dbpath)
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS pushes")
        #add changes
        cur.execute("CREATE TABLE pushes(id INTEGER PRIMARY KEY, title Text, \
                time Text, news Text, deals Text, changes Text, content TEXT, url Text);")
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY,email Text,token Text,\
                subscribed_on DateTime, confirmed Boolean, confirmed_on DateTime, \
                unsubscribed Boolean, unsubscribed_on DateTime);")

def create_positions():
    con = lite.connect(dbpath)
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS positions")
        cur.execute("CREATE TABLE positions(id INTEGER PRIMARY KEY, date Text, \
                size Text, content Text, deals Text, push_id INTEGER);")

def store_position(date, size, content, deals, push_id):
    positions = (date, size, content, deals, push_id)
    con = lite.connect(dbpath)
    con.text_factory = str
    with con:
        cur = con.cursor()
        cur.execute('''INSERT INTO positions(date, size, content, deals, push_id) \
                VALUES(?,?,?,?,?)''', positions)
        con.commit()
        #lid = cur.lastrowid #The last Id of the inserted row
        #print lid
        #print type(lid)

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

def get_size_content(position):
    size = re.findall(r'\d{1,3}', position)[0]
    content = re.findall(r'\((.*)\)', position)[0]
    return size, content

def init_positions():
    con = lite.connect(dbpath)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM pushes")
        con.commit()
        rows = cur.fetchall()
        for row in rows:
            if not re.match(ur"^15:1", row[2].split(' ')[-1]):
                continue
            position = get_position(row[5])
            if not position:
                continue
            size, content = get_size_content(position)
            pos = (row[2].split(' ')[0], size, content, row[4], row[0])
            cur.execute('''INSERT INTO positions(date, size, content, deals, push_id) \
                    VALUES(?,?,?,?,?)''', pos)
            con.commit()
            lid = cur.lastrowid #The last Id of the inserted row
            print lid


def query_all_positions():
    con = lite.connect(dbpath)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM positions")
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

def query_user_by_email(mail):
    con = lite.connect(dbpath)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=:email", {"email": mail})
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

def update_changes(uid, uchanges):
    con = lite.connect(dbpath)
    con.text_factory = str
    with con:
        cur = con.cursor()
        cur.execute("UPDATE pushes SET changes=? WHERE Id=?", (uchanges, uid))
        con.commit()
        print "Number of rows updated: %d" % cur.rowcount

def update_deals(uid, udeals):
    con = lite.connect(dbpath)
    con.text_factory = str
    with con:
        cur = con.cursor()
        cur.execute("UPDATE pushes SET deals=? WHERE Id=?", (udeals, uid))
        con.commit()
        print "Number of rows updated: %d" % cur.rowcount

def update_pos_date(uid, utime):
    con = lite.connect(dbpath)
    con.text_factory = str
    with con:
        cur = con.cursor()
        cur.execute("UPDATE positions SET date=? WHERE Id=?", (utime, uid))
        con.commit()
        print "Number of rows updated: %d" % cur.rowcount

def update_pos_size(uid, usize):
    con = lite.connect(dbpath)
    con.text_factory = str
    with con:
        cur = con.cursor()
        cur.execute("UPDATE positions SET size=? WHERE Id=?", (usize, uid))
        con.commit()
        print "Number of rows updated: %d" % cur.rowcount

def update_pos_content(uid, ucontent):
    con = lite.connect(dbpath)
    con.text_factory = str
    with con:
        cur = con.cursor()
        cur.execute("UPDATE positions SET content=? WHERE Id=?", (ucontent, uid))
        con.commit()
        print "Number of rows updated: %d" % cur.rowcount
        
def update_pos_deals(uid, udeals):
    con = lite.connect(dbpath)
    con.text_factory = str
    with con:
        cur = con.cursor()
        cur.execute("UPDATE positions SET deals=? WHERE Id=?", (udeals, uid))
        con.commit()
        print "Number of rows updated: %d" % cur.rowcount

def update_position(date, size, content, deals, push_id):
    con = lite.connect(dbpath)
    con.text_factory = str
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM positions WHERE date=\'" + date + "\'")
        con.commit()
        rows = cur.fetchall()
        if not rows:
            cur.execute('''INSERT INTO positions(date, size, content, deals, push_id) \
                VALUES(?,?,?,?,?)''', positions)
        else:
            cur.execute("UPDATE positions SET size=?, content=?, deals=?, push_id=?  WHERE date=\'" + date + "\'", (size, content, deals, push_id))
        con.commit()
        #print "Number of rows updated: %d" % cur.rowcount

def add_column():
    con = lite.connect(dbpath)
    cur = con.cursor()
    cur.execute("alter table pushes add column `changes` Text")

#queryUserId(1)
#queryAllUsers()
#addColumn()
#queryAllPushes()
#printUsers()
#create_positions()
#create_positions() #1
#init_positions()   #2
#store_position('2016-03-23', '50', '10%新股.10%袖珍股.10%生物.20%移动支付', '', '428')
#query_user_by_email('150038817@qq.com')
#update_pos_date(88, '2016-03-24')
#utext = '''
#9:31 兑现30%互联网金融股(挂单全部成交),昨日它逆市涨了近7%(未能封停),我收短线肉走人.....短线不贪婪,不恋战<br>
#14:03 买进10%软件股,见它连续调整了几天,应该是机会<br>
#14:36 买进20%移动支付概念股<br>
#14:52 兑现10%券商股,T出10%网络安全股....收两块肉'''
#update_pos_deals(62, utext)
#update_pos_size(62, '100')
#update_pos_content(62, '10%猪肉.20%网络安全.30%高送转.10%券商.10%软件.20%移动支付')
#query_all_positions() #3
#size = '50'
#content = '10%猪肉.20%网络安全.20%电池'
#deals = '9:33 买进20%电池股(挂单成交)<br>11:27 兑现10%网络安全股,吃块大肉'
#push_id = '441'
#update_position('2016-03-28', size, content, deals, push_id)
