import asyncio
import json
import ID
import user
import room
import time
import database
import utils
import sys
import tornado.ioloop
import tornado.websocket
import ssl 
 
class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    db = database.Database()

    def check_origin(self, origin):
        return True

    def open(self):
        self.id = ID.generate()
        user.User(id = self.id, socket = self, ip=self.request.remote_ip, uid=self.db.generateId(self.request.remote_ip)).addUser(self.id)
        print("Client connecting: {0}".format(self.request.remote_ip))
 
    def on_message(self, message):
        try:
            userobj = user.User().get(self.id)
            if user.User().get(self.id):
                roomobj = room.Room().get(userobj.roomname)
                if userobj.roomname and self.db.getRoom(userobj.roomname):
                    if not roomobj.get(userobj.roomname):
                        roomobj.addRoom(userobj.roomname)
                        roomobj = room.Room().get(userobj.roomname)
                        roomobj.addUser(userobj)
                    else:
                        roomobj = room.Room().get(userobj.roomname)
                        if userobj not in roomobj.users:
                            roomobj.addUser(userobj)
                print(message)
                js = json.loads(message)
                if "login" in js:
                    email = js['email']
                    password = js['password']
                    if self.db.loginCheck(email, password):
                        userobj.setLoggedIn(True)
                        userobj.setName(self.db.getUserByEmail(email)['user'])
                        userobj.send(login=1, name=userobj.name)
                    else:
                        userobj.send(login=0, error="incorrect login details")

                elif "join" in js:
                    if userobj.isLoggedIn:
                        rn = js['room'].lower()
                        if roomobj:
                            if userobj in roomobj.users:
                                roomobj.removeUser(userobj)
                            if room.Room().get(rn):
                                r = room.Room().get(rn)
                                userobj.send(joined=1)
                                userobj.setRoomName(rn)
                                r.addUser(userobj)
                                roomobj.send(left=1, name=userobj.name, time=time.time())
                                room.Room().get(rn).send(join=1, name=userobj.name, time=time.time())
                            else:
                                if self.db.getRoom(rn):
                                    room.Room().addRoom(rn)
                                    r = room.Room().get(rn)
                                    r.addUser(userobj)
                                    userobj.send(joined=1)
                                    userobj.setRoomName(rn)
                                else:
                                    userobj.send(joined=0, error="room doesn't exist")
                        else:
                            if self.db.getRoom(rn):
                                room.Room().addRoom(rn)
                                r = room.Room().get(rn)
                                r.addUser(userobj)
                                userobj.setRoomName(rn)
                                userobj.send(joined=1)
                                print(room.Room().rooms)
                    else:
                        userobj.send(denied=1, error="not logged in")
                elif "createroom" in js:
                    if userobj.isLoggedIn:
                        rn = js['room']
                        if utils.isAble(rn):
                            if not self.db.getRoom(rn.lower()):
                                self.db.addRoom(rn, userobj.name)
                                userobj.send(created=1)
                            else:
                                userobj.send(created=0, error="room already exists")
                        else:
                            userobj.send(created=0, error="8 chars max length and only symbol allowed is \"_\"")
                    else:
                        userobj.send(denied=1, error="not logged in")
                elif "register" in js:
                    email = js['email']
                    username = js['username'].lower()
                    password = js['password']
                    if self.db.getUserByEmail(email):
                        userobj.send(register=0, error="email taken")
                    if self.db.getUserByName(username):
                        userobj.send(register=0, error="username taken")
                    if not utils.isAble(username):
                        userobj.send(
                            register=0,
                            error="username must be 8 chars max or only contain alpha-numric and _"
                        )
                    else:
                        self.db.addUser(username, email, password)
                        userobj.send(register=1)
                elif "addmod" in js:
                    if userobj.owner:
                        if not self.db.getMod(roomobj.name, js['name']):
                            self.db.addMod(roomobj.name, js['name'])
                            roomobj.send(modded=1, name=js['name'])
                        else:
                            userobj.send(modded=0, error="already modded")
                    else:
                        userobj.send(modded=0, error="not owner")
                elif "removemod" in js:
                    if userobj.owner:
                        if self.db.getMod(roomobj.name, js['name']):
                            self.db.removeMod(roomobj.name, js['name'])
                            roomobj.send(demodded=1, name=js['name'])
                        else:
                            userobj.send(demodded=0, error="not modded")
                    else:
                        userobj.send(demodded=0, error="not owner")
                elif "mods" in js:
                    r = self.db.getRoom(roomobj.name)
                    m = {"modname": r['owner'], "time": r['time']}
                    for mod in self.db.getMods(roomobj.name):
                        del mod['_id']
                        userobj.send(mods=1, **mod)
                    userobj.send(**m)
                elif "ban" in js:
                    if userobj.mod or userobj.owner:
                        target = js['target']
                        id = js['id']
                        ts = time.time()
                        self.db.banUser(roomobj.name, target, userobj.name, id)
                        roomobj.sendMods(ban=1, target=target, id=id, by=userobj.name, time=ts)
                    else:
                        userobj.send(ban=0, error="not mod or owner")
                elif "unban" in js:
                    name = js['target']
                    rn = roomobj.name
                    ban = self.db.getBannedUser(rn, name)
                    id = ban['user_id']
                    if userobj.mod or userobj.owner:
                        self.db.removeBan(rn, id)
                        roomobj.sendMods(unbanned=1, target=name, time=time.time())
                    else:
                        userobj.send(unbanned=0, error="not mod or owner")
                elif "banlist" in js:
                    if userobj.mod or userobj.owner:
                        bans = self.db.bans.find({"roomname": roomobj.name})
                        for ban in bans:
                            del ban["_id"]
                            roomobj.sendMods(banlist=1, **ban)
                    else:
                        userobj.send(banlist=0, error="not mod or owner")
                elif "userlist" in js:
                    roomobj = room.Room().get(userobj.roomname)
                    for u in roomobj.users:
                        userobj.send(ul=1, name=u.name, time=u.time)
                elif "logout" in js:
                    userobj.setLoggedIn(False)
                    roomobj.removeUser(userobj)
                    userobj.send(logout=1)
                    roomobj.send(left=1, name=userobj.name, time=time.time())
                    userobj.setName(None)
                elif "message" in js:
                    if userobj.loggedIn:
                        roomobj = room.Room().get(userobj.roomname)
                        print(room.Room().rooms)
                        if not self.db.getBannedUser(roomobj.name, userobj.name):
                            if not self.db.getBannedUserById(roomobj.name, userobj.uid, check=True):
                                name = userobj.name
                                id = userobj.uid
                                mid = self.db.generateMID()
                                body = js['body']
                                ts = time.time()
                                roomobj.send(message=1, name=name, id=id, mid=mid, body=body, time=ts)
                                self.db.addMessage(name, roomobj.name, userobj.ip, id, mid, body)
                            else:
                                userobj.send(banned=1)
                        else:
                            userobj.send(banned=1)
                    else:
                        userobj.send(loggedin=1, error="not logged in")
                elif "history" in js:
                    if userobj.loggedIn:
                        count = 0
                        limit = js['limit']
                        start_at = js['start_at']
                        for message in self.db.getMessagesByRoomName(roomobj.name):
                            count += 1
                            if count >= start_at:
                                name = message['name']
                                id = message['user_id']
                                mid = message['message_id']
                                body = message['message']
                                ts = message['time']
                                userobj.send(history=1, name=name, id=id, mid=mid, time=ts, body=body)
                                if count >= limit:
                                    break
                    else:
                        userobj.send(history=0, error="not logged in")
                elif "deleteuser" in js:
                    if userobj.mod or userobj.owner:
                        name = js['name']
                        self.db.messages.delete_many({"roomname": roomobj.name, "name": name.lower()})
                        roomobj.send(delete=1, name=name, time=time.time())
                    else:
                        userobj.send(delete=0, error="not mod or owner")
                elif "delete" in js:
                    if userobj.mod or userobj.owner:
                        id = js['id']
                        self.db.messages.delete_one({"roomname": roomobj.name, "message_id": id})
                        roomobj.send(deletemessage=1, id=id)
                    else:
                        userobj.send(deletemessage=0, error="not mod or owner")

        except Exception as e:
            err = sys.exc_info()
            line = err[2].tb_lineno
            print(f"ERR: {e} at line {line}")
 
    def on_close(self):
        userobj = user.User().get(self.id)
        userobj.delUser()
        if userobj.roomname:
            roomobj = room.Room().get(userobj.roomname)
            roomobj.users.remove(userobj)
            print(f"[LEFT] [{userobj.ip}] [{userobj.name}] [{roomobj.name}] [{time.ctime}]")
            roomobj.send(left=1, name=userobj.name, time=time.time())
        else:
            print(f"[DISCONNECTED] [{userobj.ip}] [{time.ctime()}]")
class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("site/index.html")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
           (r'/', IndexPageHandler),
           (r'/serv', SimpleWebSocket),
        ]

        tornado.web.Application.__init__(self, handlers)


ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_ctx.load_cert_chain("certs/cert.pem", "certs/privkey.pem") 
def make_app():
    ws_app=Application()
    return tornado.httpserver.HTTPServer(ws_app, ssl_options=ssl_ctx)

if __name__ == "__main__":
    app = make_app()
    app.listen(9000)
    tornado.ioloop.IOLoop.current().start()
