from grid import *
from agent import *

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
    NUM_ACTIONS = 4

    actionsMap = {0:'MOVE_UP',
                  1:'MOVE_DOWN',
                  2:'MOVE_LEFT',
                  3:'MOVE_RIGHT'}

    def __init__(self, w, h):
        # Grid to hold the map
        self.grid = Grid(w, h)
        self.startNew()
        self.nextMove = None

    def actionToString(action):
        return Game.actionsMap[action]

    def startNew(self):
        self.grid.reset()
        self.state = Game.RUNNING
        self.score = 0

    def update(self):
        # Process next move and return reward
        if self.nextMove != None:
            res = self.grid.doMove(self.nextMove)
            if res == Grid.MOVE_OK:
                reward = -1
            elif res == Grid.MOVE_SCORE:
                self.score += 1
                reward = +10
            elif res == Grid.MOVE_FAIL:
                self.state = Game.LOST
                reward = -10
            elif res == Grid.MOVE_WIN:
                self.score += 1
                self.state = Game.WON
                reward = +10000
            self.nextMove = None
            return reward

    def getState(self, vision=0):
        return self.grid.stringRepSurroundings(vision)

    def move(self, move):
        self.nextMove = move

    def isGameOver(self):
        return self.state == Game.WON or self.state == Game.LOST