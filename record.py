# coding:utf-8

import time
from easydb import EasyDB

users = {}

db = EasyDB('chat',
        {'chat':['id integer primary key','room text','user text','msg text','time integer'],
         'user':['name text primary key','pw text','nickname text','note text','icon text','settings text']
    })

def getchatrecord(room,count):
    t = int(time.time()) - 1800
    return db.query('select user,msg,time from chat where user!="系统消息" and room="%s" and time>%d limit -%d' % (room,t,count))

def newuser(name,pw,nickname,note,icon,settings):
    return db.query('insert into user values("%s","%s","%s","%s","%s","%s")' % (name,pw,nickname,note,icon,settings))

def userexist(user):
    if db.query('select name from user where name="%s"' % user):
        return True

def rename(old,new):
    pass

