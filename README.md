# Anichat
a chat page using tailwindcss, python for server side (tornado)

# Installation
```bash
pip install tornado pymongo
sudo apt install mongodb
```
for windows you have to install mongodb from their website
then start the mongodb service


for ws://
edit server.py find ssl_options and remove it
then find client/chat.html
find ```ws = new WebSocket("wss://anichat.ga:9000/serv");```
and change it to ```js ws = new WebSocket("ws://localhost:9000/serv");```

for wss://
find client/chat.html
find ```ws = new WebSocket("wss://anichat.ga:9000/serv");```
and change it to ```ws = new WebSocket("wss://localhost:9000/serv");```
then go to server.py
find ```ssl_ctx.load_cert_chain("certs/cert.pem","certs/privkey.pem")```
and change to your keys


# Running Server
```bash
python3 server.py
```
# Issues
join protocol doesn't send

userlist protocol wont display all users unless sent again

ban / unban hasn't been added in client haven't hid certain buttons unless mod or owner

# What Works

 delete - delete user
 
 delete message - delete message
 
 history
 
 sending messages
 
 register
 
 login
 
 create room
 
 join
