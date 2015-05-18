# coding:utf-8

from view import route, url_for, View


@route('/about', name='about')
class About(View):
    def get(self):
        self.render()

@route('/login', name='login')
class Login(View):
    def get(self):
        self.render()

@route('/chat', name='chat')
class Chat(View):
    def get(self):
        self.render()
