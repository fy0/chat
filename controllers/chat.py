# coding=utf-8

from __future__ import unicode_literals
import tornado.web
import time,json,re

import record
from record import db
from record import users
from session import Session

def sysmsg(room,text):
    msg.send_msg(room,'系统消息',text,int(time.time()))

class room(tornado.web.RequestHandler):
    # 获取房间信息
    def get(self,room):
        if not room:
            # 返回所有信息
            pass
        pass
    # 进入/离开房间
    def post(self,room):
        _cmd  = self.get_argument('cmd')
        if _cmd == 'ENTER':
            uuid = self.get_secure_cookie('alice')
            if not uuid:return
            session = Session(uuid)
            room = session['room'] = self.get_argument('room')
            # 返回前20条聊天记录，时间限制在30分钟内。
            self.write(json.dumps(record.getchatrecord(room,20)))
        elif _cmd == 'LEAVE':
            uuid = self.get_secure_cookie('alice')
            if not uuid:return
            session = Session(uuid)
            room = session['room']
            user = session['user']
            del users[room][user]
            sysmsg(room,'用户 '+user+' 离开房间')
            session['room'] = None

# 收发消息
class msg(tornado.web.RequestHandler):
    callbacks = {}

    @tornado.web.asynchronous
    def get(self):
        # 初始化 session
        uuid = self.get_secure_cookie('alice')
        if not uuid:return
        session = Session(uuid)

        # 检查房间是否存在
        room = session['room']
        if not room: return
        if not room in self.callbacks:
            self.callbacks[room] = set()
            users[room] = dict()
        user = session['user']
        # 添加至回调列表
        self.callbacks[room].add(self.on_new_msg)
        # 新用户
        if not user in users[room]:
            users[room][user] = []
            sysmsg(room,'用户 '+user+' 进入房间')

    def post(self):
        # 初始化 session
        uuid = self.get_secure_cookie('alice')
        if not uuid:return
        session = Session(uuid)

        # 发送消息
        _room = session['room']
        _user = session['user']
        _msg  = self.get_argument('msg')
        _time = int(time.time())
        self.send_msg(_room,_user,_msg,_time)

    @staticmethod
    def send_msg(room,usr,msgtext,time):
        db.query('insert into chat(room,user,time,msg) values(?,?,?,?)',(room,usr,time,msgtext))
        db.commit()
        for callback in msg.callbacks[room]:
            callback(usr,msgtext,time)
        msg.callbacks[room] = set()

    def on_new_msg(self,usr,msg,time):
        if self.request.connection.stream.closed():
            return
        self.write('{"user":"%s","msg":"%s","time":%d}' % (usr,msg,time))
        self.finish()

