# coding:utf-8

import time
from easydb import EasyDB

users = {}

db = EasyDB('chat',{'chat':['id integer primary key','room text','user text','msg text','time integer']})

def getchatrecord(room,count):
    t = int(time.time()) - 1800
    return db.query('select user,msg,time from chat where room="%s" and time>%d limit -%d' % (room,t,count))

