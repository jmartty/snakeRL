import numpy as np
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
    FRUIT = 1
    WALL = 2
    PLAYER = 3
    BODY = 4

    def stringRepFull(self):
        # Init all blank
        self.squares = [[Grid.EMPTY for _ in range(self.h)] for _ in range(self.w)]
        # Replace fruit square
        self.squares[self.fruitPosition[0]][self.fruitPosition[1]] = Grid.FRUIT
        # Replace player squares
        # Head
        self.squares[self.playerPosition[0]][self.playerPosition[1]] = Grid.PLAYER
        # Tail
        i = 0
        for prev in reversed(self.playerPreviousPositions):
            self.squares[prev[0]][prev[1]] = Grid.BODY + i
            i += 1

        # Join as flattened string
        return ''.join([str(square) for rows in self.squares for square in rows])

    def stringRepSurroundings(self, vision):
        if vision == 0: return self.stringRepFull()
        # Surroundings width (from center)
        w = vision
        h = vision
        # Player coords
        x = self.playerPosition[0]
        y = self.playerPosition[1]
        # Init all blank
        self.squares = [[Grid.EMPTY for _ in range(w*2+1)] for _ in range(h*2+1)]
        # Head
        self.squares[w][h] = Grid.PLAYER
        # Tail
        i = 0
        for prev in reversed(self.playerPreviousPositions):
            if np.abs(prev[0] - x) <= w and np.abs(prev[1] - y) <= h:
                self.squares[prev[0]-x+w][prev[1]-y+h] = Grid.BODY + i
            i += 1
        # Replace fruit square
        if np.abs(self.fruitPosition[0] - x) <= w and np.abs(self.fruitPosition[1] - y) <= h:
            self.squares[self.fruitPosition[0]-x+w][self.fruitPosition[1]-y+h] = Grid.FRUIT
        # Place walls
        if x < w:
            for j in range(w*2+1):
                self.squares[w-1-x][j] = Grid.WALL
        if x > self.w-1-w:
            for j in range(w*2+1):
                self.squares[w+self.w-x][j] = Grid.WALL
        if y < h:
            for i in range(h*2+1):
                self.squares[i][h-1-y] = Grid.WALL
        if y > self.h-1-h:
            for i in range(h*2+1):
                self.squares[i][h+self.h-y] = Grid.WALL

        # Add "normalized" fruit direction
        direct = [self.fruitPosition[0]-self.playerPosition[0],
                  self.fruitPosition[1]-self.playerPosition[1]]
        direct[0] = direct[0]/np.abs(direct[0]) if direct[0] != 0 else 0
        direct[1] = direct[1]/np.abs(direct[1]) if direct[1] != 0 else 0
        self.squares.extend([direct])
        # Join as flattened string
        return ''.join([str(square) for rows in self.squares for square in rows])

    def tailLength(self):
        return len(self.playerPreviousPositions)

    def fruitDirectionActionIdx(self):
        direct = [self.fruitPosition[0]-self.playerPosition[0],
                  self.fruitPosition[1]-self.playerPosition[1]]
        if direct[0] > 0:
            return game.Game.MOVE_RIGHT
        elif direct[0] < 0:
            return game.Game.MOVE_LEFT
        elif direct[1] > 0:
            return game.Game.MOVE_DOWN
        elif direct[1] < 0:
            return game.Game.MOVE_UP
        else:
            # Should never land here
            return None