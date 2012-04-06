# coding:utf-8

from __future__ import unicode_literals
import tornado.web
import uuid

from record import users
from session import Session
from chat import sysmsg

class login(tornado.web.RequestHandler):
    # 获取信息，检查是否存有 session 等等
    def get(self):
        _uuid = self.get_secure_cookie('alice')
        if _uuid:
            session = Session(_uuid)
            self.finish({'user':session['user'],'room':session['room']})

    def post(self):
        self.set_header('Content-Type','text/plain')
        user = self.get_argument('user')

        # TODO:用户名检查

        # 建立 session
        _uuid = self.get_secure_cookie('alice')
        if not _uuid:
            _uuid = str(uuid.uuid4())
            self.set_secure_cookie('alice',_uuid)

        # 储存信息
        session = Session(_uuid)
        oldusr = session['user']
        session['user'] = user

        # 善后
        room = session['room']
        if room and oldusr:
            users[room][user] = users[room][oldusr]
            del users[room][oldusr]
            sysmsg(room,'注意： '+oldusr+' 更名为 '+user)
        self.write('+OK 100')

