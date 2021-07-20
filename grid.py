import pygame



WIDTH = 900
HEIGHT = 900
BROWN = (133, 88, 63)
WHITE = (239, 241, 228)
def is_odd(number):
    return number % 2 != 0

class Grid():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size_to_square = WIDTH // width
        temp_grid = []

        for i in range(1, width + 1):
            temp_grid.append([])
            for j in range(1, height + 1):
                temp_grid[-1].append(j)


        self.grid = temp_grid


    def draw(self, win):
        beforeColor = WHITE
        for i in range(0, len(self.grid) + 1):
            RectColor = beforeColor

            for j in range(0, len(self.grid[i - 1])):

                if RectColor == BROWN:
                    pygame.draw.rect(win, BROWN, (self.size_to_square * j, self.size_to_square * i, self.size_to_square, self.size_to_square))
                    RectColor = WHITE
                    beforeColor = BROWN

                else:
                    pygame.draw.rect(win, WHITE, (self.size_to_square * j, self.size_to_square * i, self.size_to_square, self.size_to_square))
                    RectColor = BROWN
                    beforeColor =WHITE


        self.draw_grid(win)


    def draw_grid(self, win):

        for i in range(0, len(self.grid) + 1):

            pygame.draw.line(win, (0, 0, 0), (0, self.size_to_square * i), (WIDTH, self.size_to_square * i), width=3)

            for j in range(0, len(self.grid[i - 1])):

                pygame.draw.line(win, (0, 0, 0), (self.size_to_square * j, 0), (self.size_to_square * j, HEIGHT), width=3)