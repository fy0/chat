# coding:utf-8

import tornado.web

from controllers import form,chat,user

application = tornado.web.Application([
    # 访问模板
    (r"/",                 form.index),
    (r"/form/chat",        form.chat),
    (r"/form/reg",         form.reg),
    (r"/form/login",       form.login),
    (r"/form/about",       form.about),
    # 提交/返回聊天数据
    ('/chat/room/?(.*)',   chat.room),
    ('/chat/msg',          chat.msg),
    # 帐号相关操作
    ('/login',             user.login),
    ],

    template_path='templates',
    static_path='static',
    debug=True,
    cookie_secret="6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"
)

