# coding=utf-8

import tornado.web

class index(tornado.web.RequestHandler):
    def get(self):
        self.set_cookie('room','')
        self.render('main.html');

class about(tornado.web.RequestHandler):
    def get(self):
        self.render('about.html')
        #return render.about()

class login(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')
        #return render.login()

class chat(tornado.web.RequestHandler):
    def get(self):
        self.render('chat.html')
        #return render.chat()

class reg(tornado.web.RequestHandler):
    def get(self):
        self.render('reg.html')
        #return render.reg()

