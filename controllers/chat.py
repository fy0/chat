# coding=utf-8

import tornado.web
import time,json,re

import logic

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
            _user = self.get_argument('user')
            _room = self.get_argument('room')
            logic.enterroom(_user,_room)
        elif _cmd == 'LEAVE':
            _user = self.get_argument('user')
            logic.leaveroom(_user)

# 收发消息
class msg(tornado.web.RequestHandler):
    callbacks = {}
    users = {}

    @tornado.web.asynchronous
    def get(self,room):
        # 检查房间是否存在
        if not room in self.callbacks:
            self.callbacks[room] = set()
        # 添加至回调列表
        self.callbacks[room].add(self.on_new_msg)
        # 检查用户是否在房间中
        self.user = self.get_cookie('user')
        if not self.user:
            _user = self.get_argument('user')
            self.set_cookie('user',_user)
            self.user = repr(_user)
            self.send_msg(room,'系统消息',u'用户'+_user+u'进入房间',int(time.time()))

    def post(self,room):
        if not room in self.callbacks:
            self.callbacks[room] = set()
        # 发送消息
        _user = self.get_argument('user')
        _msg  = self.get_argument('msg')
        _time = int(time.time())
        logic.addmsg(_user,_msg,_time)
        self.send_msg(room,_user,_msg,_time)

    def send_msg(self,room,usr,msg,time):
        print '准备将消息加入回调列表'
        for callback in self.callbacks[room]:
            callback(usr,msg,time)
        self.callbacks[room] = set()

    def on_new_msg(self,usr,msg,time):
        if self.request.connection.stream.closed():
            return
        self.write(u"{'user':'%s','msg':'%s','time':%s}" % (usr,msg,time))
        print '试图将消息发给用户'
        self.finish()

