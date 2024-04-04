# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 08:46:21 2024

@author: User
"""

import socket
import json

sconnect=socket.socket()

address=(('Localhost',3000))

jsonrequest={
   "request": "subscribe",
   "port": 8888,
   "name": "fun_name_for_the_client",
   "matricules": ["22237"]
}

request=json.dumps(jsonrequest).encode()

sconnect.connect(address)
sconnect.send(request)
res = sconnect.recv(2048).decode()
print(json.loads(res))

sconnect.close()


server=socket.socket()

ping_request={
   "request": "ping"
}
server.bind(('localhost',8888))
server.listen()



response={
    "response" : "pong"
}
while True:
    client,address= server.accept()
    req=json.loads(client.recv(2048).decode())
    if req["request"]=="ping":
        response_pong=json.dumps(response).encode()
        x=0
        while x<len(response_pong):
               x += client.send(response_pong)
    client.close()