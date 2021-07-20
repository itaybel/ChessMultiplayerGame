import pygame
from os import listdir
from os.path import isfile, join
from board import Board
from grid import Grid

import random
from player import Player

class Game:
    def __init__(self, id, rows, screen_width):
        self.ready = False
        self.id = id
        self.rows = rows
        self.screen_width = screen_width
        self.players = [Player("white"), Player("black")]
        self.grid = Grid(width=rows , height=rows)
        self.board = Board(900, 900, 8 , self)
        self.current_turn = random.choice(["white", "black"])



    def connected(self):
        return self.ready




    def resetWent(self):
        self.__init__(self.id, self.rows, self.screen_width)

    def send_to_server(self, n):
        game = n.send(self)
        self = game



    def get_winner(self):


        first_board = self.board.boards["white"]
        first_board_to_strings = []
        for i in first_board:
            for j in i:
                if j == None: continue
                first_board_to_strings.append((j.__class__.__name__, j.color))




        found_kings = {
            "white": False,
            "black": False
        }

        for j in first_board_to_strings:
            name, color =  j
            if name == "King":
                found_kings[color] = True

        if found_kings["white"] and found_kings["black"]:
            return None

        if found_kings["white"] and not found_kings["black"]: #means that white won
            return "white"
        if not found_kings["white"] and  found_kings["black"]: #means that black won
            return "black"

        return None
