import copy
import random
import game

class Grid:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.freePositions = None
        self.playerPosition = None
        self.fruitPosition = None
        self.playerPreviousPositions = []

    def reset(self):
        # Used to keep track of where to spawn fruit / player
        self.freePositions = [(x,y) for x in range(self.w) for y in range(self.h)]
        random.shuffle(self.freePositions)
        # Init player and fruit
        self.playerPosition = self.freePositions.pop()
        self.fruitPosition = self.freePositions.pop()
        self.playerPreviousPositions = []

    # Movement results
    MOVE_OK = 0
    MOVE_SCORE = 1
    MOVE_WIN = 2
    MOVE_FAIL = -1

    def doMove(self, direction):
        newPos = list(self.playerPosition)
        if direction == game.Game.MOVE_UP:
            newPos[1] -= 1
        elif direction == game.Game.MOVE_DOWN:
            newPos[1] += 1
        elif direction == game.Game.MOVE_LEFT:
            newPos[0] -= 1
        elif direction == game.Game.MOVE_RIGHT:
            newPos[0] += 1
        else:
            raise ValueError('Invalid direction')
        return self.updatePlayerPosition(tuple(newPos))

    def updatePlayerPosition(self, newPos):
        # Check if we have gone out of bounds
        if newPos[0] < 0 or newPos[0] >= self.w or newPos[1] < 0 or newPos[1] >= self.h:
            return Grid.MOVE_FAIL
        # Check if we have collided we ourselves
        elif newPos in self.playerPreviousPositions:
            return Grid.MOVE_FAIL
        # Check if we have taken the fruit
        elif newPos == self.fruitPosition:
            self.playerPreviousPositions.append(self.playerPosition)
            self.playerPosition = newPos
            if len(self.freePositions) > 0:
                self.fruitPosition = self.freePositions.pop()
                return Grid.MOVE_SCORE
            else:
                return Grid.MOVE_WIN
        else:
            # else just update position and the tails
            # Add previous pos to head of tail
            self.playerPreviousPositions.append(self.playerPosition)
            # Remove last tail element
            self.freePositions.append(self.playerPreviousPositions.pop(0))
            # Update player position
            self.playerPosition = newPos
            self.freePositions.remove(newPos)
            random.shuffle(self.freePositions)
            return Grid.MOVE_OK

    # Grid slots
    EMPTY = 0
    PLAYER = 1
    BODY = 2
    FRUIT = 3

    def stringRep(self):
        # Init all blank
        self.squares = [[Grid.EMPTY for _ in range(self.h)] for _ in range(self.w)]
        print(self.squares)
        # Replace fruit square
        self.squares[self.fruitPosition[0]][self.fruitPosition[1]] = Grid.FRUIT
        # Replace player squares
        # Head
        self.squares[self.playerPosition[0]][self.playerPosition[1]] = Grid.PLAYER
        # Tail
        for prev in self.playerPreviousPositions:
            self.squares[prev[0]][prev[1]] = Grid.BODY

        # Join as flattened string
        return ''.join([str(square) for rows in self.squares for square in rows])