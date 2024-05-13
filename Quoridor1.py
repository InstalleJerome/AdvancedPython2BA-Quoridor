# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 08:46:21 2024

@author: User
"""

import socket
import json

sconnect=socket.socket()

#adresse de connection
address=(('localhost',3000))
#identité
matricule=input("matricule :")
port=int(input("port :"))
nom=input("Nom :")

#requete pour se connecter
jsonrequest={
   "request": "subscribe",
   "port": port,
   "name": nom,
   "matricules": [matricule]
}

request=json.dumps(jsonrequest).encode()

#permet d'envoyer la requete et de recevoir la réponse à cette requete (connection reussie ou non)
sconnect.connect(address)
sconnect.send(request)
res = sconnect.recv(2048).decode()
print(json.loads(res))

sconnect.close()

#permet de se déplacer verticalement
def move_up(p_init1,p_init2):
    if p_init2[0]==p_init1[0]-2 and p_init2[1]==p_init1[1]:
        p_init1=[p_init1[0]-4,p_init1[1]]
    else:
        p_init1=[p_init1[0]-2,p_init1[1]]
    return p_init1

def move_down(p_init1,p_init2):
    if p_init2[0]==p_init1[0]+2 and p_init2[1]==p_init1[1]:
        p_init1=[p_init1[0]+4,p_init1[1]]
    else:
        p_init1=[p_init1[0]+2,p_init1[1]]
    return p_init1


#permet de se déplacer sur la gauche
def move_left(p_init1,p_init2):
    if p_init2[1]==p_init1[1]-2 and p_init1[0]==p_init2[0]:
        p_init1=[p_init1[0],p_init1[1]-4]
    else:
        p_init1=[p_init1[0],p_init1[1]-2]
    return p_init1

#permet de se déplacer sur la droite
def move_right(p_init1,p_init2):
    if p_init2[1]==p_init1[1]+2 and p_init1[0]==p_init2[0]:
        p_init1=[p_init1[0],p_init1[1]+4]
    else:
        p_init1=[p_init1[0],p_init1[1]+2]
    return p_init1

def distance(position1,position2,indice):
    my_distance=0
    other_distance=0
    if indice==float(0):
        my_distance=16-position1[0]
        other_distance=position2[0]
    elif indice==float(1):
        my_distance=position1[0]
        other_distance=16-position2[0]
    return [my_distance,other_distance]

def block(position,indice,left_case,right_case):
    blocker_pos1=[]
    blocker_pos2=[]
    if indice==float(0):
        blocker_pos1=[position[0]-1,position[1]]
        if position[1]==16:
            blocker_pos2=[position[0]-3,position[1]-2]
            blocker_pos1=[position[0]-3,position[1]]
        elif right_case==4:
            blocker_pos2=[position[0]-1,position[1]-2]
        elif left_case==4:
            blocker_pos2=[position[0]-1,position[1]+2]
        elif position[1]==0:
            blocker_pos2=[position[0]-3,position[1]+2]
            blocker_pos1=[position[0]-3,position[1]]
        else:
            blocker_pos2=[position[0]-1,position[1]-2]
    if indice==float(1):
        blocker_pos1=[position[0]+1,position[1]]
        if position[1]==16:
            blocker_pos2=[position[0]+3,position[1]-2]
            blocker_pos1=[position[0]+3,position[1]]
        elif right_case==4:
            blocker_pos2=[position[0]+1,position[1]-2]
        elif left_case==4:
            blocker_pos2=[position[0]+1,position[1]+2]
        elif position[1]==0:
            blocker_pos2=[position[0]+1,position[1]+2]
            blocker_pos1=[position[0]+3,position[1]]
        else:
            blocker_pos2=[position[0]+1,position[1]-2]
    return [blocker_pos1,blocker_pos2]


#crée un socket qui va servir de serveur
server=socket.socket()
server.settimeout(0.5)

ping_request={
   "request": "ping"
}

#se connecte au client de jeu
server.bind(('localhost',int(port)))
server.listen()

last_move=None

response={
    "response" : "pong"
}

#boucle d'actions
while True:
    try :
        client,address= server.accept() #accepte la connection du client
        finished=False
        msg=b''
        req=None
        while not finished: #boucle assurant la reception de l'entiereté du message
            msg+=client.recv(2048)
            try:
                req=json.loads(msg.decode('utf8'))
                finished=True
            except json.JSONDecodeError:
                pass
            except UnicodeDecodeError:
                pass
        
        if req["request"]=="ping": #répond à la demande pour assurer la présence du joueur
            response_pong=json.dumps(response).encode()
            x=0
            while x<len(response_pong):
                x += client.send(response_pong)
        if req["request"]=="play": #repond à la demande d'action de jeu
            my_indice=0
            other_indice=0
            my_position=[0,0]
            other_position=[0,0]
            other_fwd_case=0
            if req["state"]["players"][0]==nom: #permet de savoir si on est joueur 1 ou 2
                my_indice=float(0)
                other_indice=float(1)
            else:
                my_indice=float(1)
                other_indice=float(0)
            #permet de trouver les positions des 2 joueurs
            for i in range(len(req["state"]["board"])):
                for j in range(len(req["state"]["board"][i])):
                    if req["state"]["board"][i][j]==my_indice:
                        my_position=[i,j]
                    if req["state"]["board"][i][j]==other_indice:
                        other_position=[i,j]
            if other_indice==0:
                other_fwd_case=req["state"]["board"][other_position[0]+1][other_position[1]]
            else:
                other_fwd_case=req["state"]["board"][other_position[0]-1][other_position[1]]
            if distance(my_position,other_position,my_indice)[0]>distance(my_position,other_position,my_indice)[1] and req["state"]["blockers"][int(my_indice)]>0 and other_fwd_case==3:
                if my_indice==float(0) and req["state"]["board"][other_position[0]-1][other_position[1]]==3:
                    if other_position[1]==16:
                        move={
                        "type":"blocker",
                        "position":block(other_position,my_indice,req["state"]["board"][other_position[0]-1][other_position[1]-2],None)
                    }
                    elif other_position[1]==0:
                        {
                        "type":"blocker",
                        "position":block(other_position,my_indice,None,req["state"]["board"][other_position[0]-1][other_position[1]+2])
                    }
                    else:
                        move={
                            "type":"blocker",
                            "position":block(other_position,my_indice,req["state"]["board"][other_position[0]-1][other_position[1]-2],req["state"]["board"][other_position[0]-1][other_position[1]+2])
                        }
                elif my_indice==float(1) and req["state"]["board"][other_position[0]+1][other_position[1]]==3:
                    if other_position[1]==16:
                        move={
                        "type":"blocker",
                        "position":block(other_position,my_indice,req["state"]["board"][other_position[0]+1][other_position[1]-2],None)
                    }
                    elif other_position[1]==0:
                        move={
                        "type":"blocker",
                        "position":block(other_position,my_indice,None,req["state"]["board"][other_position[0]+1][other_position[1]+2])
                    }
                    else:
                        move={
                            "type":"blocker",
                            "position":block(other_position,my_indice,req["state"]["board"][other_position[0]+1][other_position[1]-2],req["state"]["board"][other_position[0]+1][other_position[1]+2])
                        }
            else:            
                if my_indice==float(0): #permet de bouger sur le plateau
                    if req["state"]["board"][my_position[0]+1][my_position[1]]==float(3):
                        move={
                            "type":"pawn",
                            "position": [move_down(my_position,other_position)],
                        }
                        last_move="down"
                    else:
                        indice=[0,45]
                        indice_column=17
                        if my_position[1]!=0 and req["state"]["board"][my_position[0]][my_position[1]-1]==4:
                            if abs(my_position[1]-indice[1])>4:
                                move={
                                "type":"pawn",
                                "position": [move_up(my_position,other_position)],
                                }
                                last_move="up"
                            else:
                                move={
                                "type":"pawn",
                                "position":[move_right(my_position,other_position)]
                                }
                                last_move="right"
                        elif my_position[1]!=16 and req["state"]["board"][my_position[0]][my_position[1]+1]==4:
                            if abs(my_position[1]-indice[1])>4:
                                move={
                                "type":"pawn",
                                "position": [move_up(my_position,other_position)],
                                }
                                last_move="up"
                            else:
                                move={
                                "type":"pawn",
                                "position":[move_left(my_position,other_position)]
                                }
                                last_move="left"
                        if req["state"]["board"][my_position[0]][my_position[1]-1]==4 and req["state"]["board"][my_position[0]][my_position[1]+1]==4:
                            move={
                            "type":"pawn",
                            "position": [move_up(my_position,other_position)],
                        }
                            last_move="up"
                        for i in range(len(req["state"]["board"][my_position[0]+1])):
                            if req["state"]["board"][my_position[0]+1][i]==3:
                                if i<my_position[1]:
                                    indice[0]=i
                                elif i>my_position[1] and i<indice[1]:
                                    indice[1]=i     
                        if last_move=="left" and req["state"]["board"][my_position[0]][my_position[1]-1]!=4:
                            move={
                                "type":"pawn",
                                "position":[move_left(my_position,other_position)]
                            }
                            last_move="left"
                        elif abs(my_position[1]-indice[0])<=abs(my_position[1]-indice[1]) or my_position[1]==16:
                            move={
                                "type":"pawn",
                                "position":[move_left(my_position,other_position)]
                            }
                            last_move="left"
                        elif abs(my_position[1]-indice[0])>abs(my_position[1]-indice[1]) or my_position[1]==0:
                            move={
                                "type":"pawn",
                                "position":[move_right(my_position,other_position)]
                            }
                            last_move="right"
                if my_indice==float(1):
                    if req["state"]["board"][my_position[0]-1][my_position[1]]==float(3):
                        if req["state"]["board"][my_position[0]][my_position[1]-1]==4 or req["state"]["board"][my_position[0]][my_position[1]+1]==4 and last_move=="down":
                             move={
                            "type":"pawn",
                            "position": [move_down(my_position,other_position)],
                        }
                             last_move="down"
                        else:
                            move={
                                "type":"pawn",
                                "position": [move_up(my_position,other_position)],
                            }
                            last_move="up"
                    else:
                        indice=[0,16]
                        if req["state"]["board"][my_position[0]][my_position[1]-1]==4 and req["state"]["board"][my_position[0]][my_position[1]+1]==4:
                            move={
                            "type":"pawn",
                            "position": [move_down(my_position,other_position)],
                        }
                            last_move="down"
                        for i in range(len(req["state"]["board"][my_position[0]-1])):
                            if req["state"]["board"][my_position[0]+1][i]==3:
                                if i<my_position[0]:
                                    indice[0]=i
                                elif i>my_position[0] and i<indice[1]:
                                    indice[1]=i
                        if abs(my_position[0]-indice[0])<=abs(my_position[1]-indice[1]):
                            move={
                                "type":"pawn",
                                "position":[move_left(my_position,other_position)]
                            }
                            last_move="left"
                        elif abs(my_position[0]-indice[0])>abs(my_position[1]-indice[1]):
                            move={
                                "type":"pawn",
                                "position":[move_right(my_position,other_position)]
                            }
                            last_move="right"
            response_move={
                    "response": "move",
                    "move": move,
                    "message": "Yo yo yo"
                    }
            rep_move=json.dumps(response_move).encode()
            x=0
            #boucle d'envoi de l'action a effectuer
            while x<len(rep_move):
                x+=client.send(rep_move)
        client.close()
    except socket.timeout:
        pass