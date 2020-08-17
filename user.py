import json
import time

class User(object):

    _users = dict()

    def __init__(self, name=None, id=None, ip=None, uid=None, socket=None):

        self.name = name
        self.id = id
        self.ip = ip
        self.uid = uid
        self.roomname = None
        self._socket = socket
        self.isLoggedIn = False
        self.isMod = False
        self.isOwner = False
        self.time = None

    def addUser(self, id):
        self._users[id] = self

    def delUser(self, id=None):
        if id:
            del self._users[id]
        else:
            del self._users[self.id]

    def get(self, id):
        if id in self._users:
            return self._users[id]

    def send(self, **kwargs):
        self._socket.write_message(json.dumps(kwargs).encode("utf-8"))

    def sendall(self, **kwargs):
        for user in list(self._users.values()):
            user.send(kwargs)

    def setName(self, name):

        self.name = name

    def setRoomName(self, name):

        self.roomname = name
        self.time = time.time() * 1000

    def setLoggedIn(self, boolean):

        self.isLoggedIn = bool(boolean)

    def setMod(self, boolean):
        self.isMod = bool(boolean)

    def setOwner(self, boolean):
        self.isOwner = bool(boolean)

    def getLoggedIn(self):
        return self.isLoggedIn

    def getMod(self):
        return self.isMod

    def getOwner(self):
        return self.isOwner

    def __repr__(self):
        return f"<User {self.id}>"

    loggedIn = property(getLoggedIn)
    mod = property(getMod)
    owner = property(getOwner)