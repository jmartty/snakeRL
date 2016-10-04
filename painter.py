import pygame
from game import *

SQ_SIZE = 16
BLACK = (24 , 24 , 24 )
WHITE = (225, 225, 225)
LGRAY = (175, 175, 175)
GRAY  = (125, 125, 125)
RED   = (200, 0  , 0  )

class Painter:

    def __init__(self, screen, game, clock):
        self.screen = screen
        self.screen.fill(BLACK)
        self.game = game
        self.clock = clock
        # +1 square for each edge
        self.game_surface = pygame.Surface(( (game.grid.w+2)*SQ_SIZE, (game.grid.h+2)*SQ_SIZE))
        self.font = pygame.font.SysFont("verdana", 12)

    def paint(self):
        self.screen.fill(BLACK)
        self.game_surface.fill(BLACK)
        self.paintGame()
        pygame.display.update()
        self.clock.tick(30)

    def paintGame(self):
        self.paintEdges()
        self.paintGrid()
        self.screen.blit(self.game_surface,
            (self.screen.get_width()/2 - self.game_surface.get_width()/2,
            self.screen.get_height()/2 - self.game_surface.get_height()/2))
        self.paintScore()
        self.paintResult()

    def paintScore(self):
        score_surface = self.font.render("Score: "+str(self.game.score), True, LGRAY)
        self.screen.blit(score_surface,
            (self.screen.get_width()/2 - score_surface.get_width()/2,
            self.screen.get_height()/2 - self.game_surface.get_height()/2 - score_surface.get_height() - 5))

    def paintResult(self):
        if self.game.isGameOver():
            outcome = None
            if self.game.state == Game.WON:
                outcome = "You win!"
            elif self.game.state == Game.LOST:
                outcome = "Game-over!"

            result_surface = self.font.render(outcome, True, LGRAY)
            self.screen.blit(result_surface,
                (self.screen.get_width()/2 - result_surface.get_width()/2,
                self.screen.get_height()/2 + self.game_surface.get_height()/2 + result_surface.get_height() - 5))

    def paintEdges(self):
        # Left edge
        self.game_surface.fill(GRAY, pygame.Rect(0,0,SQ_SIZE,self.game_surface.get_height()))
        # Right edge
        self.game_surface.fill(GRAY, pygame.Rect(
            self.game_surface.get_width()-SQ_SIZE,
            0,SQ_SIZE,self.game_surface.get_height()))
        # Top edge
        self.game_surface.fill(GRAY, pygame.Rect(0,0,self.game_surface.get_width(),SQ_SIZE))
        # Bottom edge
        self.game_surface.fill(GRAY, pygame.Rect(
            0, self.game_surface.get_height()-SQ_SIZE,
            self.game_surface.get_width(),SQ_SIZE))

    def paintGrid(self):
        # Paint fruit
        fp = self.game.grid.fruitPosition
        self.game_surface.fill(RED, pygame.Rect(self.logic2pixels(fp), (SQ_SIZE,SQ_SIZE)))
        # Paint player and tail
        pp = self.game.grid.playerPosition
        self.game_surface.fill(WHITE, pygame.Rect(self.logic2pixels(pp), (SQ_SIZE,SQ_SIZE)))
        tail_size = len(self.game.grid.playerPreviousPositions)
        i = 1
        for tail_part in self.game.grid.playerPreviousPositions:
            scale = 0.75 + 0.25*i/tail_size
            color = (LGRAY[0]*scale,)*3
            self.game_surface.fill(color, pygame.Rect(self.logic2pixels(tail_part), (SQ_SIZE,SQ_SIZE)))
            i += 1

    def logic2pixels(self, pos):
        return (SQ_SIZE*(pos[0]+1),SQ_SIZE*(pos[1]+1))