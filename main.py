import pygame
import threading
import pickle
import time
from grid import Grid
from board import Board
import traceback
from Unit import Unit, Bishop, King, Pawn, Queen, Rook, Knight
from game import Game
from network import Network
import random
WIDTH = 900

HEIGHT = 900

pygame.init()


font = pygame.font.SysFont("Comic Sans MS", 35)

BROWN = (133, 88, 63)
WHITE = (239, 241, 228)

rows = 8
current_unit_path_to_draw = None
current_path_to_draw = []
lastboard = []
def reDrawWindow(win, grid, board, currentUnitToDraw, player, n):
    win.fill((255,255,255))
    grid.draw(win)
    board.draw(win, player)
    if not board.game.ready:
        draw_waiting_screen(win)
    handle_move(win, board, currentUnitToDraw)
    promoted_pawn = is_promoting(player, board)



    if promoted_pawn != None:

        choosed_piece = promote_screen(win, player)

        if choosed_piece != None:
            other_player = {"white": "black", "black": "white"}[player]

            strings_to_units = {"queen": Queen, "rook": Rook, "bishop": Bishop, "knight": Knight}

            createdUnit = strings_to_units[choosed_piece](promoted_pawn.row, promoted_pawn.column, promoted_pawn.color)
            board.boards[player][promoted_pawn.row][promoted_pawn.column] = createdUnit
            board.boards[other_player][7 - promoted_pawn.row][7 - promoted_pawn.column] = createdUnit

            board.game.send_to_server(n)

    if board.game.get_winner() != None:
        board.game.ready = False
        win_screen(win, board.game.get_winner())
        board.game.send_to_server(n)
    pygame.display.update()

def remove_tile(path, tile):
    filteredPath = []
    for x, y , color in path:
        if x == tile.row  - 1 and y == tile.column - 1:
            continue

        filteredPath.append((x, y , color))

    return filteredPath

def draw_path(win, path, board):
    global before_drawed_path
    try:
        #path = remove_tile(path, current_unit_path_to_draw)
        # .remove()
        pass


    except Exception as e:
        print(e)
    for (x, y, color) in path:
        pygame.draw.circle(win, (0, 255 , 0),   (board.size_to_square * y + (board.size_to_square // 2), board.size_to_square * x + (board.size_to_square // 2)) , 20)


def draw_waiting_screen(win):
    pygame.draw.rect(color=(255, 255, 255), rect=(100, 330,700 ,200), surface=win)
    textsurface = font.render("Waiting for another player to join", False, (0, 0, 0))  # "text", antialias, color
    win.blit(textsurface, (150, 400))

def win_screen(win, winner):
    pygame.draw.rect(color=(255, 255, 255), rect=(100, 330,700 ,200), surface=win)
    textsurface = font.render(f"{winner} won the game!", False, (0, 0, 0))
    win.blit(textsurface, (150, 400))

def closest_to_tile(tile, path):
    closest = (999, 999, None)
    secondClosest = (999 , 999, None)

    for i in path:
        x, y, color = i
        xTile, yTile, colorTile = tile.row, tile.column, tile.color

        if abs(xTile - x) <= closest[0] and abs(yTile - y) <= closest[1]:
            secondClosest = closest
            closest = i

    return closest, secondClosest




def get_in_loop(player, board, pos , path, move, iteration=0):

    x, y = pos

    moves_to_pos = {
    "down-all": [0, 1] ,
    "up-all": [0, -1],
    "right-all": [1, 0],
    "left-all": [-1, 0],
    "rightup-all": [-1 , 1],
    "leftup-all": [-1 , -1],
    "rightdown-all": [1 , 1],
    "leftdown-all": [1 , -1]

    }

    if x < 0 or x > 7 or y < 0 or y > 7:
        print("return in 1")

        return path

    curr_tile = board.boards[player][y][x]
    next_tile = board.boards[player][y + moves_to_pos[move][1]][x + moves_to_pos[move][0]]

    if curr_tile != None and curr_tile.color != None and curr_tile.color != player :

        path.append((y, x, curr_tile.color))
        return path

    if curr_tile != None and curr_tile.color == player and iteration != 0:
        return path

    if next_tile == None:

        path.append((y, x, None))
    else:
        path.append((y, x, next_tile.color))

    return get_in_loop(player=player, board=board, pos=(x + moves_to_pos[move][0], y + moves_to_pos[move][1]), path=path, move=move, iteration=iteration+1)



def handle_move(win, board, unit):
    if unit == None: return


    moves = unit.moves

    walkable_tiles = []

    x, y = unit.row  , unit.column


    for move in moves:

        try:

            if move == "special":
                #if its the horse


                #upper:

                upRightUnit = (x - 2, y + 1)
                upLeftUnit = (x - 2, y - 1)

                #right:

                rightUpUnit = (x - 1, y + 2)
                rightDownUnit = (x + 1, y + 2)


                #down:

                downRightUnit = (x + 2, y + 1)
                downLeftUnit = (x + 2, y - 1)

                #left:

                leftUpUnit = (x - 1, y - 2)
                leftDownUnit = (x + 1, y - 2)

                allwantedUnits = [upRightUnit, upLeftUnit, rightUpUnit, rightDownUnit, downRightUnit, downLeftUnit, leftUpUnit, leftDownUnit]

                for pos in allwantedUnits:
                    try:
                        currentUnit = board.boards[player][pos[0]][pos[1]]
                    except Exception as e:
                        print(traceback.format_exc())
                        continue

                    if currentUnit != None and currentUnit.color == player:

                        continue

                    if currentUnit == None: walkable_tiles.append((pos[0] , pos[1], None))
                    else: walkable_tiles.append((pos[0] , pos[1], currentUnit.color))






            if move == "left":

                if y - 1 >= 8 or x < 0: continue
                try:
                    currentUnit = board.boards[player][x][y - 1]
                except: continue
                if currentUnit != None and currentUnit.color == player:
                    continue
                if currentUnit == None: walkable_tiles.append((x , y - 1, None))
                else: walkable_tiles.append((x , y - 1 , currentUnit.color))


            if move == "right":

                if True:
                    if y + 1 >= 8 or x < 0: continue
                    try:
                        currentUnit = board.boards[player][x][y + 1]
                    except: continue

                    if currentUnit != None and currentUnit.color == player:
                        continue
                    if currentUnit == None: walkable_tiles.append((x , y + 1, None))
                    else: walkable_tiles.append((x , y + 1 , currentUnit.color))

            if move == "down":

                if True:
                    if y + 1 >= 8 or x < 0: continue
                    try:
                        currentUnit = board.boards[player][x + 1][y]
                    except: continue

                    if currentUnit != None and currentUnit.color == player:
                        continue
                    if currentUnit == None: walkable_tiles.append((x+ 1 , y , None))
                    else: walkable_tiles.append((x+ 1 , y , currentUnit.color))

            if move == "cross-rightdown":

                if True:
                    if y + 1 >= 8 or x  < 0: continue
                    currentUnit = board.boards[player][x+1][y+1]
                    if currentUnit != None and currentUnit.color == player:
                        continue
                    if currentUnit == None: walkable_tiles.append((x + 1, y + 1, None))
                    else: walkable_tiles.append((x + 1, y + 1, currentUnit.color))


            if move == "cross-leftdown":

                if True:
                    if y  >= 7 or x  < 0: continue
                    currentUnit = board.boards[player][x+1][y-1]
                    if currentUnit != None and currentUnit.color == player:
                        continue
                    if currentUnit == None: walkable_tiles.append((x + 1, y - 1, None))
                    else: walkable_tiles.append((x + 1, y - 1, currentUnit.color))

            if move == "cross-rightup":

                if True:
                    if y + 1 >= 8 or x  < 0: continue
                    currentUnit = board.boards[player][x-1][y+1]
                    if currentUnit != None and currentUnit.color == player:
                        continue
                    if currentUnit == None: walkable_tiles.append((x - 1, y + 1, None))
                    else: walkable_tiles.append((x - 1, y + 1, currentUnit.color))


            if move == "cross-leftup":

                if True:
                    if y < 0 or x  < 0: continue

                    currentUnit = board.boards[player][player][x-1][y-1]
                    if currentUnit != None and currentUnit.color == player:
                        continue

                    if currentUnit == None: walkable_tiles.append((x - 1, y - 1, None))
                    else: walkable_tiles.append((x - 1, y - 1, currentUnit.color))



            if move == "cross-right":


                if y + 1 >= 8 or x  < 0: continue
                currentUnit = board.boards[player][x-1][y+1]
                if currentUnit != None and currentUnit.color != player:

                    if currentUnit == None: walkable_tiles.append((x - 1, y + 1, None))
                    else: walkable_tiles.append((x - 1, y + 1, currentUnit.color))


            if move == "cross-left":



                currentUnit = board.boards[player][x-1][y-1]
                if currentUnit != None and currentUnit.color != player:
                    if currentUnit == None: walkable_tiles.append((x - 1, y - 1, None))
                    else: walkable_tiles.append((x - 1, y - 1, currentUnit.color))




            if move in ["rightup-all","leftup-all", "rightdown-all","leftdown-all", "down-all", "up-all", "right-all", "left-all"]:
                walkable_tiles = get_in_loop(player, board, (y, x), walkable_tiles, move)

                if (x, y, player) in walkable_tiles:

                    walkable_tiles.remove((x, y, player))
                if (x, y, None) in walkable_tiles:
                    walkable_tiles.remove((x, y, None))




            if move == "up":

                currentUnit =board.boards[player][x - 1][y]
                if currentUnit == None:

                    walkable_tiles.append((x - 1, y, None))

                currentUnit = board.boards[player][x - 1][y]
                if currentUnit == None:
                    walkable_tiles.append((x - 1, y, None))


            if move == "up2":
                if board.boards[player][x][y].movedtwice:
                    continue

                currentUnit = board.boards[player][x - 2][y]
                if currentUnit == None:
                    walkable_tiles.append((x - 2, y , None))


                currentUnit = board.boards[player][x - 2][y]
                if currentUnit == None:
                    walkable_tiles.append((x - 2, y, None))





        except Exception as e:
            print(e)
            pass


    draw_path(win, walkable_tiles, board)

    return walkable_tiles




def handle_clickes(win, board, player, n):

    global current_path_to_draw

    global current_unit_path_to_draw


    clickedUnit, clickPos = board.get_clicked_unit(player)

    if clickedUnit == None or clickedUnit.color != player:
        if player == board.game.current_turn:
            if (clickPos[0], clickPos[1]) in [(i[0], i[1]) for i in current_path_to_draw]:  # if the player clicked in the greendot

                print("player", player)

                board.moveOrKill(current_unit_path_to_draw, clickPos, player, n)
                current_path_to_draw = []

            current_path_to_draw = []
            current_unit_path_to_draw = None



    else:
        if board.game.current_turn == player:
            current_unit_path_to_draw = clickedUnit
            walkable_tiles = handle_move(win, board, clickedUnit)

            current_path_to_draw = walkable_tiles
def is_promoting(player, board):
    for rowI in range(len(board.boards[player])):
        row = board.boards[player][rowI]
        for boxI in range(len(row)):
            box = row[boxI]
            if box.__class__.__name__ == "Pawn":
                if rowI == 0:
                    return box
    return None

def promote_screen(win, player):
    pygame.draw.rect(color=(0, 0, 0), rect=(100, 330,700 ,200), surface=win)
    pieces_to_promote = ["queen", "rook", "bishop", "knight"]
    positions = {}
    for i in range(1, len(pieces_to_promote) + 1):


        unitImage = pygame.image.load(f"assests/{pieces_to_promote[i - 1]}-" + player + ".png")

        unitImage = pygame.transform.scale(unitImage, (110, 110))

        unitRect = unitImage.get_rect()

        unitRect.x = 100 + (i * 120)
        unitRect.y = 360


        pygame.draw.rect(color=(255, 255, 255), rect=(105 + (i * 120), 360, 100, 100), surface=win)

        win.blit(unitImage, unitRect)

        positions[pieces_to_promote[i -1]] = (105 + (i * 120), 360, 100, 100)

    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()

        for i in range(len(pieces_to_promote)):
            piece = pieces_to_promote[i]
            x, y, w, h = positions[piece]

            if mx > x and mx < (x + w):
                if my > y and my < (y + h):
                    return piece
    return None


def main():
    global player

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    run = True
    clock = pygame.time.Clock()


    global current_path_to_draw

    global current_unit_path_to_draw

    n = Network()




    game = n.send("get")

    player = n.player_color

    game.board.create_board(player)

    print(game.board.boards.keys())

    game = n.send(game)
    print(game.board.boards)

    while run:
        clock.tick(30)

        game = n.send("get")
        board = game.board
        grid = game.grid

        reDrawWindow(win, grid, board, current_unit_path_to_draw, player, n)
        promote_screen(win, player)


        for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if pygame.mouse.get_pressed()[0] and game.ready:

                    handle_clickes(win, board, player, n)

        #n.send(pickle.dumps(game))

    pygame.quit()


if __name__ == '__main__':

    main()