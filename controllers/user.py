# coding:utf-8

import tornado.web
import uuid

import logic
from logic import users
from session import Session

class login(tornado.web.RequestHandler):
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
        self.write('+OK 100')

