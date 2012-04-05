# coding:utf-8

import tornado.web

import logic

class login(tornado.web.RequestHandler):
    def post(self):
        self.set_header('Content-Type','text/plain')
        oldusr = self.get_arguments('oldusr')
        user = self.get_argument('user')

        if oldusr:
            if logic.changename(oldusr[0],user):
                self.write('+OK 100')
            else:
                self.write('+ERR 101')
        else:
            if logic.adduser(user):
                self.write('+OK 100')
            else:
                self.write('+ERR 101') # 重名

