import hashlib, time, random
from pymongo import MongoClient


class Database:
    def __init__(self):
        self.db = MongoClient("localhost", 27017)['chat']
        self.messages = self.db['messages']
        self.users = self.db['users']
        self.rooms = self.db['rooms']
        self.mods = self.db['mods']
        self.bans = self.db['bans']
        self.stylesheets = self.db['stylesheet']
        self.pms = self.db['PMS']

    def getUserByEmail(self, email):
        return self.users.find_one({"email": email})

    def getUserByName(self, name):
        return self.users.find_one({"user": name})

    def getRoom(self, name):
        return self.rooms.find_one({"name": name})

    def loginCheck(self, email, password):
        found = self.users.find_one({"email": email})
        if found:
            password = self.hashpassword(password)
            if found['password'] == password:
                return True

    def addUser(self, username, email, password):
        if self.getUserByEmail(email):
            return 0
        if self.getUserByName(username):
            return -1
        else:
            password = self.hashpassword(password)
            self.users.insert_one({
                "user": username,
                "email": email,
                "password": password,
                "time": time.time()
            })
            return True

    def removeUser(self, name):
        self.users.delete_one({"user": name})

    def addRoom(self, roomname, owner):
        if not self.getRoom(roomname):
            self.rooms.insert_one({
                "name": roomname,
                "owner": owner,
                "time": time.time()
            })
            return True

    def removeRoom(self, name):
        self.rooms.delete_one({"name": name})

    def getRoomsByOwner(self, owner, check=False):
        if not check: return self.rooms.find({"owner": owner})
        else: return self.rooms.find_one({"owner": owner})

    def generateMID(self):
        abc = "abcdefghijklnmopqrstuvwxyz"
        abc_up = abc.upper()
        num = "1234567890"
        symbols = "!@#$%^&*()_-=+{}[]:;'<>,./\\"
        f = []
        for symbol in symbols:
            f.append(symbol)
            random.shuffle(f)
        for n in num:
            f.append(n)
            random.shuffle(f)
        for l in abc + abc_up:
            f.append(l)
            random.shuffle(f)
        string = "".join(f)
        md5 = hashlib.md5()
        md5.update(string.encode())
        return md5.hexdigest()

    def addMessage(self, name, roomname, raw_ip, uuid, mid, message):
        self.messages.insert_one({
            "name": name,
            "roomname": roomname,
            "ip": raw_ip,
            "message_id": mid,
            "user_id": uuid,
            "message": message,
            "time": time.time()
        })

    def getMessageById(self, id):
        return self.messages.find_one({"message_id": id})

    def getMessagesByRoomName(self, name):
        return self.messages.find({"roomname": name})

    def getMessagesByUserId(self, id):
        return self.messages.find({"user_id": id})

    def getMessagesByIp(self, ip):
        return self.messages.find({"ip": ip})

    def getMessagesByUserIdAndRoom(self, id, name):
        return self.messages.find({"user_id": id, "roomname": name})

    def getMessagesByIpAndRoom(self, ip, name):
        return self.messages.find({"ip": ip, "roomname": name})

    def getMessagesByUser(self, name):
        return self.messages.find({"name": name})

    def getMessagesByUserAndRoom(self, name, roomname):
        return self.messages.find({"name": name, "roomname": roomname})

    def banUser(self, room, target, user, uuid):
        if not self.getBannedUser(room, user):
            self.bans.insert_one({
                "roomname": room,
                "name": target,
                "by": user,
                "user_id": uuid,
                "time": time.time()
            })

    def getBannedUser(self, room, user):
        return self.bans.find_one({
            "roomname": room,
            "name": user
        })

    def getBannedUserById(self, room, id, check=False):
        if not check:
            return self.bans.find({
                "roomname": room,
                "user_id": id
            })
        else:
            return self.bans.find_one({
                "roomname": room,
                "user_id": id
            })

    def removeBan(self, room, id):
        self.bans.delete_many(

                {
                    "user_id": id,
                    "roomname": room
                })

    def getMods(self, room):
        return self.mods.find({
            "roomname": room
        })

    def isOwner(self, room, user):
        r = self.getRoom(room)
        if r:
            owner = r['owner']
            if owner == user:
                return True

    def getMod(self, room, modname):
        return self.mods.find_one({
            "roomname": room,
            "name": modname

        })

    def addMod(self, room, modname):
        if not self.getMod(room, modname):
            self.mods.insert_one({
                "roomname": room,
                "name": modname,
                "time": time.time()
            })

    def removeMod(self, room, modname):
        self.mods.delete_one({
            "roomname": room,
            "name": modname
        })

    def getStylesheet(self, room):
        return self.stylesheets.find_one({"roomname": room})

    def setStylesheet(self, room, sheet):
        if self.getStylesheet(room):
            self.stylesheets.delete_one({"roomname": room})
            self.stylesheets.insert_one({
                "roomname": room,
                "stylesheet": sheet
            })
        else:
            self.stylesheets.insert_one({
                "roomname": room,
                "stylesheet": sheet
            })

    def generateId(self, ip):
        md51 = hashlib.md5()
        md51.update("$%#$^))&*_-=+".encode())
        ip += md51.hexdigest()
        md52 = hashlib.md5()
        md52.update(ip.encode())
        return md52.hexdigest()

    def hashpassword(self, password):
        salt = hashlib.sha3_512()
        salt.update("$%&^&*())(&*^&%%$##$$#$%&^^(*(*++===".encode())
        password += salt.hexdigest()
        passw = hashlib.sha3_224()
        passw.update(password.encode())
        return passw.hexdigest()


if __name__ == "__main__":
    db = Database()
    print(db.getBannedUserById("examplegroup", "admin"))