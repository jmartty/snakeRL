from pprint import pprint
import pickle
import random
import pygame
import sys
from game import *
from painter import *
from utils import *

# Grid dimensions
WIDTH = 4
HEIGHT = 3
VISION = 2

pygame.init()
clock = pygame.time.Clock()
game = Game(WIDTH, HEIGHT)
screen = pygame.display.set_mode((640, 480))
painter = Painter(screen, game, clock)

agent = Agent(epsilon=0.05, alpha=0.01, gamma=1.0, num_actions=Game.NUM_ACTIONS, file=None)

following = False
score_ma = MovingAverage(0.001)
wins_ma = MovingAverage(0.01)
it = 0

while True:

    # Input logic
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                following = not following
                print("-following toggle-")
            if event.key == pygame.K_UP:
                print("Agent e: "+str(agent.increaseEpsilon()))
            if event.key == pygame.K_DOWN:
                print("Agent e: "+str(agent.lowerEpsilon()))
            if event.key == pygame.K_RIGHT:
                print("Agent a: "+str(agent.increaseAlpha()))
            if event.key == pygame.K_LEFT:
                print("Agent a: "+str(agent.lowerAlpha()))
            if event.key == pygame.K_s:
                agent.save()
            if event.key == pygame.K_ESCAPE:
                agent.save()
                sys.exit()

    # String rep for current grid
    curr_grid_state = game.grid.stringRepSurroundings(VISION)
    # Get move from agent
    game.move(agent.nextAction(curr_grid_state, game.grid))
    # Update game and pass reward to agent
    agent.sampleStateAction(curr_grid_state, game.update())

    # Drawing
    if following:
        painter.paint()
        pygame.time.wait(150)

    # End game logic
    if game.isGameOver():

        if game.state == Game.WON:
            wins_ma.sample(100)
        elif game.state == Game.LOST:
            wins_ma.sample(0)

        if following or it % 500 == 0:            
            print("avg_target%: "+f2s((score_ma.mean*100/((WIDTH*HEIGHT)-1)))
                  +" avg_score: "+f2s(score_ma.mean)
                  +" wins%: "+f2s(wins_ma.mean)
                  +" a.e: "+f2s(agent.epsilon, '4')
                  +" a.a: "+f2s(agent.alpha)
                  +" it: "+str(it)
                  +" s: "+str(agent.stateCount()))
            
            if following:
                pygame.time.wait(1500)
        
        if it % 50000 == 0:
            agent.save()
        it += 1

        score_ma.sample(game.score)
        
        game.startNew()
        agent.newEpisode()
