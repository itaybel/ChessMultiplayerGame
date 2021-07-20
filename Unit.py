class Unit():
    def __init__(self, row, column):

        self.row = row
        self.column = column

class Knight(Unit):
    def __init__(self, row, column, color):
        Unit.__init__(self, row, column)
        self.color = color
        self.moves = ["special"]
        self.img = "assests/knight-" + color + ".png"


class Bishop(Unit):
    def __init__(self, row, column, color):
        Unit.__init__(self,  row, column)
        self.moves = ["rightup-all","leftup-all", "rightdown-all","leftdown-all"]

        self.color = color
        self.img = "assests/bishop-" + color + ".png"

class King(Unit):
    def __init__(self,  row, column, color):
        Unit.__init__(self, row, column)
        self.moves = ["cross-rightup", "cross-leftup", "cross-leftdown", "cross-rightdown", "down", "up", "right", "left"]
        self.color = color
        self.img = "assests/king-" + color + ".png"

class Pawn(Unit):
    def __init__(self, color, row, column):
        Unit.__init__(self, row, column)
        self.moves = ["up", "up2", "cross-right", "cross-left"]
        self.movedtwice = False

        self.color = color
        self.img = "assests/pawn-" + color + ".png"



class Queen(Unit):
    def __init__(self,  row, column, color):
        Unit.__init__(self, row, column)

        self.moves = ["rightup-all","leftup-all", "rightdown-all","leftdown-all", "down-all", "up-all", "right-all", "left-all"]

        self.color = color
        self.img = "assests/queen-" + color + ".png"

class Rook(Unit):
    def __init__(self, row, column, color):
        Unit.__init__(self, row, column)
        self.moves = ["down-all", "up-all", "right-all", "left-all"]

        self.color = color
        self.img = "assests/rook-" + color + ".png"