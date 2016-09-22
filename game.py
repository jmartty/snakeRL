from grid import *

class Game:

    # Game states
    RUNNING = 0
    LOST = 1
    WON = 2

    # Possible moves
    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3

    def __init__(self, w, h):
        # Grid to hold the map
        self.grid = Grid(w, h)
        self.startNew()
        self.nextMove = None

    def startNew(self):
        self.grid.reset()
        self.state = Game.RUNNING
        self.score = 0

    def update(self):
        # Process next move
        if self.nextMove != None:
            res = self.grid.doMove(self.nextMove)
            if res == Grid.MOVE_OK:
                # Do nothing
                pass
            elif res == Grid.MOVE_SCORE:
                self.score += 1
            elif res == Grid.MOVE_FAIL:
                self.state = Game.LOST
            elif res == Grid.MOVE_WIN:
                self.state = Game.WON
            self.nextMove = None

    def move(self, move):
        self.nextMove = move

    def isGameOver(self):
        return self.state == Game.WON or self.state == Game.LOST