# -*- coding=utf-8 -*-
import asynchat
import asyncore
import socket

PORT = 6666


class EndSession(Exception):
    pass


class ChatServer(asyncore.dispatcher):
    '''
        聊天程序
    '''

    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        # create socket
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        # set socket can be reused
        self.set_reuse_addr()
        self.bind(("", port))
        self.listen(5)
        self.users = {}
        self.main_room = ChatRoom(self)

    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self.connect())

class ChatSession(asyncore.dispatcher):

    def __init__(self, server, socket):
        asyncore.dispatcher.__init__(self, socket)
        self.server = server
        self.set_terminator(b'\n')
        self.data = []
        self.name = None
        self.enter(LoginRoom(server))

    def enter(self, room):
        try:
            cur = self.room
        except AttributeError:
            pass
        else:
            cur.remove
        self.room = room
        room.add(self)

    def collect_incoming_data(self, data):
        self.append(data)

    def find_termintor(self):
        line = ''.join(self.data)
        self.data = []
        try:
            self.room.handle(self, line)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        asynchat.async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))

class CommandHandler:
    '''
        command handle class
    '''
    def unknown(self, session, cmd):
        #相应未知命令
        session.push(('Unknow command {} \n'.format(cmd)).encode('utf-8'))

    def handle(self, session, line):
        if not line.strip():
            return
        parts = line.split(' ', 1)
        cmd = parts[0]
        try:
            line = parts[1].strip()
        except IndexError:
            line = ''
        method = getattr(self, 'do_'+ cmd, None)
        try:
            method(session, line)
        except TypeError:
            self.unknown(session, cmd)

class Room(CommandHandler):
    '''
        包含多个用户的环境，负责基本的命令处理和广播
    '''
    def __init__(self, server):
        self.server = server
        self.sessions = []

    def add(self, session):
        self.sessions.append(session)

    def remove(self, session):
        self.sessions.remove(session)

    def broadcast(self, line):
        #向所有用户发送指定信息

        for session in self.sessions:
            session.push(line)

    def do_logout(self, session, line):
        raise   EndSession

class LoginRoom(Room):

    def add(self, session):
        #用户连接成功的回应
        Room.add(self, session)
        #使用asynchat.asyn_chat.push方法发送数据
        session.push(b"Connect Success")

    def do_login(self, session, line):
        name = line.strip()
        if not name:
            session.push(b'User name is empty')
        elif name in self.server.users:
            session.push(b'User name exists')
        else:
            session.name = name
            session.enter(self.server.main_room)
class LogoutRoom(Room):
    '''
    处理退出用户
    '''
    def add(self, session):
        try:
            del self.server.users[session.name]
        except KeyError:
            pass


class ChatRoom(Room):
    '''
    聊天用的房间
    '''
    def add(self, session):
        session.push(b'Login Success!')
        self.broadcast((session.name + 'has entered the room.\n').encode('utf-8'))
        self.server.users[session.name] = session
        Room.add(self, session)

    def remove(self, session):
        Room.remove(self, session)
        self.broadcast((session.name + 'has left the room\n').encode('utf-8'))

    def do_say(self, session, line):
        self.broadcast((session.name)+': ' + line).encode('utf-8')

    def do_look(self, session, line):
        session.push(b'Online users:\n')
        for other in self.sessions:
            session.push((other.name + '\n').encode('utf-8'))

if __name__ == '__main__':
    s = ChatServer(PORT)
    try:
        print "chat server run at '0:0:0:0:{0}'".format(PORT)
        asyncore.loop()
    except KeyboardInterrupt:
        print "system exit"



