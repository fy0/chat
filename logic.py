# coding:utf-8

import easydb
import tornado.web

users = {}
rooms = {'1':{'title':'','users':[]},
         '2':{'title':'','users':[]},
         '3':{'title':'','users':[]},
         '4':{'title':'','users':[]},
         '5':{'title':'','users':[]},
         '6':{'title':'','users':[]}}

usercount = []

# 消息
def addmsg(usr,msg,time):
    if not usr in users:
        return False
    sysmsg_msg(usr,msg,time)

# 添加一个用户
def adduser(usr):
    if not usr in users:
        usercount.append(0)
        uc = len(usercount)
        users[usr] = {'id':uc,'room':0}
        return True
    return False

# 修改用户名
def changename(usr,newusr):
    if newusr in users or usr not in users:
        return False
    users[newusr] = users[usr]
    if users[usr]['room']:
        sysmsg_changename(usr,newusr,users[usr]['room'])
    del users[usr]
    return True

# 进入房间
def enterroom(usr,room):
    # 正确性检查,TODO:session检查
    if not usr in users or not room in rooms:
        return False
    if users[usr]['room']:
        return False
    # 进入新房间
    rooms[room]['users'].append(users[usr]['id'])
    users[usr]['room'] = room
    sysmsg_enter(usr,room)

# 离开房间
def leaveroom(usr):
    if not usr:return False
    rooms[users[usr]['room']]['users'].remove(users[usr]['id'])
    sysmsg_leave(usr,users[usr]['room'])
    users[usr]['room'] = ''
    return True

# 添加房间
def addroom(name,title):
    if name in rooms:
        return False
    rooms[name] = {'title':title,'users':[]}

# 系统消息：进入房间
def sysmsg_enter(usr,room):
    print u'通知：用户 '+usr+u' 进入房间 '+room+' !'
    pass

# 系统消息：离开房间
def sysmsg_leave(usr,room):
    print u'通知：用户 '+usr+u' 离开房间 '+room+' !'
    pass

# 系统消息：改名
def sysmsg_changename(old,new,room):
    print u'通知：用户 '+old+u' 改名为 '+new+' !'
    pass

# DEBUG 信息：消息发送
def sysmsg_msg(usr,msg,time):
    print u'['+repr(time)+u'] 消息：用户 '+usr+u' 说: '+msg
    pass

