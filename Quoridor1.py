# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 08:46:21 2024

@author: User
"""

import socket
import json

sconnect=socket.socket()

address=(('localhost',3000))
matricule=input("matricule :")
port=int(input("port :"))
nom=input("Nom :")
jsonrequest={
   "request": "subscribe",
   "port": port,
   "name": nom,
   "matricules": [matricule]
}

request=json.dumps(jsonrequest).encode()

sconnect.connect(address)
sconnect.send(request)
res = sconnect.recv(2048).decode()
print(json.loads(res))

sconnect.close()

    
server=socket.socket()
server.settimeout(0.5)

ping_request={
   "request": "ping"
}
server.bind(('localhost',int(port)))
server.listen()



response={
    "response" : "pong"
}
while True:
    try :
        client,address= server.accept()
        req=json.loads(client.recv(2048).decode())
        if req["request"]=="ping":
            response_pong=json.dumps(response).encode()
            x=0
            while x<len(response_pong):
                x += client.send(response_pong)
        if req["request"]=="play":
            print(req["state"]["board"])
        client.close()
    except socket.timeout:
        pass