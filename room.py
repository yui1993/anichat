import json
import database


class Room:

    rooms = dict()

    def __init__(self):

        self.__db = database.Database()
        self.users = list()
        self.mods = list()
        self.name = None

    def addRoom(self, name):
        self.rooms[name] = self
        self.name = name

    def addUser(self, user):

        if self.__db.isOwner(self.name, user.name):
            user.setOwner(True)
        if self.__db.getMod(self.name, user.name):
            user.setMod(True)
        self.users.append(user)

    def removeUser(self, user):
        self.users.remove(user)

    def delRoom(self, name):

        if name in self.rooms:
            del self.rooms[name]

    def get(self, name):

        if name in self.rooms:
            return self.rooms[name]

    def send(self, **kw):

        for user in self.users:
            user.send(**kw)

    def sendMods(self, **kw):
        for user in self.users:
            if user.mod or user.owner:
                user.send(**kw)

    def getUserCount(self):

        return len(self.users)

    def __repr__(self):
        return f"<Room {self.name}>"

    count = property(getUserCount)
