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

def vertical_move(p_init,indice,player):
    if player==True:
        if indice==float(1):
            p_init=[p_init[0]-4,p_init[1]]
    if indice==float(0):
        if player==True:
            p_init=[p_init[0]+4,p_init[1]]        
    return p_init

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
            indice=0
            my_position=[0,0]
            if req["state"]["players"][0]==nom:
                my_indice=float(0)
                other_indice=float(1)
            else:
                my_indice=float(1)
                other_indice=float(0)
            for i in range(len(req["state"]["board"])):
                for j in range(len(req["state"]["board"][i])):
                    if req["state"]["board"][i][j]==indice:
                        position=[i,j]
            if indice==float(0):
                if req["state"]["board"][position[0]+1][position[1]]==float(3):
                    move={
                        "type":"pawn",
                        "position": [vertical_move(position,indice)],
                    }
            if indice==float(1):
                if req["state"]["board"][position[0]-1][position[1]]==float(3):
                    move={
                        "type":"pawn",
                        "position": [vertical_move(position,indice)],
                    }
            response_move={
                    "response": "move",
                    "move": move,
                    "message": "Fun message"
                    }
            rep_move=json.dumps(response_move).encode()
            while x<len(rep_move):
                x+=client.send(rep_move)
        client.close()
    except socket.timeout:
        pass