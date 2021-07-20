import pygame
from Unit import Unit, Bishop, King, Pawn, Queen, Rook, Knight
import random
WIDTH = 900
HEIGHT = 900
BROWN = (133, 88, 63)
WHITE = (239, 241, 228)


def get_start_unit(row, column, player_color):
    units_white = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    units_black = [Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook]
    if column > 7: column = 7
    if player_color == "white":
        if row == 0:
            return units_white[column](row, column, "black")
        else:
            return units_white[column](row, column, "white")
    else:
        if row == 0:
            return units_black[column](row, column, "white")
        else:
            return units_black[column](row, column, "black")


class Board():
    def __init__(self, width, height, rows, game):
        self.width = width
        self.height = height
        self.rows = rows
        self.size_to_square = WIDTH // rows
        self.boards = {}
        self.name = "".join([random.choice(["a", "b", "c", "r", "p"]) for i in range(5)])

        self.game = game

    def create_board(self, player_color):
        temp_board = []
        rows = self.rows
        print("created board for " + player_color)
        for i in range(rows + 1):

            temp_board.append([])
            for j in range(rows + 1):
                if i == 0 or i == rows - 1:
                    unit = get_start_unit(i, j, player_color)
                    temp_board[-1].append(unit)


                elif i == 1 or i == rows - 2:

                    if player_color == "white":
                        if i == 1:
                            unit = Pawn("black", row=i, column=j)
                        else:
                            unit = Pawn("white", row=i, column=j)
                    else:
                        if i == 1:
                            unit = Pawn("white", row=i, column=j)
                        else:
                            unit = Pawn("black", row=i, column=j)

                    temp_board[-1].append(unit)

                else:

                    temp_board[-1].append(None)
        self.boards[player_color] = temp_board



    def draw(self, win, player):

        for i in range(len(self.boards[player])):
            row = self.boards[player][i]
            for unit in row:

                unitIndex = row.index(unit)

                if unit == None: continue

                unitImage = pygame.image.load(unit.img)

                unitImage = pygame.transform.scale(unitImage, (110, 110))

                unitRect = unitImage.get_rect()

                unitRect.x = self.size_to_square * unitIndex
                unitRect.y = self.size_to_square * i



                win.blit(unitImage, unitRect)

    def get_clicked_pos(self, pos):
        x, y = pos

        row = y // self.size_to_square
        col = x // self.size_to_square

        return row, col

    def get_clicked_unit(self, player):

        for rowindex in range(len(self.boards[player])):
            row = self.boards[player][rowindex]
            for unitIndex in range(len(row)):
                unit = row[unitIndex]
                mouse_to_grid = self.get_clicked_pos(pygame.mouse.get_pos())

                if (rowindex, unitIndex) == mouse_to_grid:
                    if unit == None: return (unit, (rowindex, unitIndex, None))
                    else: return (unit, (rowindex, unitIndex, unit.color))


    def moveOrKill(self, unit, pos, player, n):


        print(pos)
        print(unit.row, unit.column)
        before_change_pos = (unit.row, unit.column)
        unit.row = pos[0]
        unit.column = pos[1]


        self.boards[player][pos[0]][pos[1]] = unit
        self.boards[player][before_change_pos[0] ][before_change_pos[1] ] = None

        other_player = {"white": "black", "black": "white"}[player]


        self.boards[other_player][7 - pos[0]][7 - pos[1]] = unit
        self.boards[other_player][7 - before_change_pos[0] ][7 - before_change_pos[1] ] = None


        #if he moves the pawn 2 squars
        if abs(before_change_pos[0] -  pos[0]) == 2 and unit.__class__.__name__ == "Pawn":
            unit.movedtwice = True

        self.game.current_turn = other_player
        self.game.board = self
        self.game.send_to_server(n)





