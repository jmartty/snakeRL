import random
import pygame
import sys
from game import *
from painter import *

pygame.init()
clock = pygame.time.Clock()
game = Game(10, 15)
screen = pygame.display.set_mode((640, 480))
painter = Painter(screen, game, clock)

while True:

    # Input logic
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.move(Game.MOVE_LEFT)
            if event.key == pygame.K_RIGHT:
                game.move(Game.MOVE_RIGHT)
            if event.key == pygame.K_UP:
                game.move(Game.MOVE_UP)
            if event.key == pygame.K_DOWN:
                game.move(Game.MOVE_DOWN)
            if event.key == pygame.K_ESCAPE:
                sys.exit()
    # Game logic
    game.update()

    # Drawing
    painter.paint()

    # End game logic
    if game.isGameOver():
        if game.state == Game.WON:
            print("You win!")
        elif game.state == Game.LOST:
            print("Game-over!")
        pygame.time.wait(3000)
        game.startNew()