
import socket
import threading
import pickle
from game import Game
from board import Board
import json
import random

server = socket.gethostbyname(socket.gethostname())
print(server)

port = 6010

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(5)
print("Waiting for a connection, Server Started")

games = {}
idCount = 0

def threaded_client(conn, p, gameId):

    print(gameId)
    print(p)

    while True:


        try:
            data = pickle.loads(conn.recv(4096 * 3))
        except Exception as e:
            continue

        if not data: break
        if data == "get":

            conn.send(pickle.dumps(games[gameId]))
        if data == "player":
            conn.send(str(p))
        if type(data) == Game:

            games[gameId] = data
            print("success", p)
            conn.send(pickle.dumps(games[gameID]))







while True:

    conn, addr = s.accept()
    print("Connected to:", addr)


    idCount += 1 #adding the people who connected
    p = "white"
    gameID = (idCount - 1) // 2

    if idCount % 2 == 1: #if we need to create a new game
        games[gameID] = Game(gameID, screen_width=900, rows=8)
        print("Creating a new game...")
    else:
        games[gameID].ready = True
        p = "black"

    conn.send(pickle.dumps(p))

    thread = threading.Thread(target=threaded_client, args=(conn, p, gameID))
    thread.start()