# coding:utf-8

from __future__ import unicode_literals
import time
from easydb import EasyDB

# users 结构 : users -> room -> 房间内用户
users = {}

class Rooms:
    data = {}
    #def __init__(self):
    #    pass
    def addroom(self,_id,title="无标题"):
        self.data[_id] = {'title':title,'num':0,'lastmsg':{}}
    def delroom(self,_id):
        if _id in self.data:
            del self.data[_id]
            return True
    def __setitem__(self,key,value):
        self.data[key]['lastmsg'] = value
    def __getitem__(self,key):
        self.data[key]['num'] = len(users[key])
        return self.data[key]
    def getinfo(self):
        for i in self.data:
            self.data[i]['num'] = len(users[i])
        return self.data

# 房间内的一些信息: 标题、人数、最后一条消息
rooms = Rooms()

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

