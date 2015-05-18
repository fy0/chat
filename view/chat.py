# coding:utf-8

import json
from view import route, url_for, View
from sockjs.tornado import SockJSRouter, SockJSConnection


class Room(object):
    def __init__(self):
        self.users = set()


class ChatConnection(SockJSConnection):
    visitors = set()
    rooms = {}
    uid_start = 1000

    def on_open(self, request):
        self.uid = self.uid_start
        self.uid_start += 1
        self.room_id = None
        self.username = None
        self.visitors.add(self)

    def on_close(self):
        self.leave_room()
        self.visitors.remove(self)

    def say(self, txt):
        if self.room_id:
            r = self.rooms[self.room_id]
            self.broadcast(r.users, json.dumps([
               ['say', [self.uid, self.username], txt],
            ]))

    def enter_room(self, room_id):
        self.leave_room()
        if not room_id in self.rooms:
            self.rooms[room_id] = Room()
        if not self.room_id in self.rooms:
            self.room_id = room_id
            r = self.rooms[room_id]
            r.users.add(self)
            #self.broadcast([self], json.dumps([['enter_room', self.uid]]))
            self.broadcast(r.users, json.dumps([['enter_room', room_id, [self.uid, self.username]]]))

    def leave_room(self):
        if self.room_id in self.rooms:
            r = self.rooms[self.room_id]
            r.users.remove(self)

            self.broadcast(r.users, json.dumps([['leave_room', self.room_id, [self.uid, self.username]]]))

            if len(r.users) == 0:
                del self.rooms[self.room_id]

            self.room_id = None

    def on_message(self, message):
        info = json.loads(message)

        for i in info:
            key = i[0]
            if key == 'set_username':
                self.username = i[1]
                self.broadcast([self], json.dumps([['user_info', [self.uid, self.username]]]))
            elif key == 'enter_room':
                if self.username:
                    self.enter_room(int(i[1]))
            elif key == 'leave_room':
                if self.username:
                    self.leave_room(int(i[1]))
            elif key == 'say':
                if self.username:
                    self.say(i[1])
            elif key == 'room_list':
                pass


chat_route = SockJSRouter(ChatConnection, '/ws/api')
