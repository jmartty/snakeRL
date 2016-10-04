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
VISION = 0

pygame.init()
clock = pygame.time.Clock()
game = Game(WIDTH, HEIGHT)
screen = pygame.display.set_mode((640, 480))
painter = Painter(screen, game, clock)

agent = Agent(epsilon=0.0, alpha=0.15, gamma=1.0, num_actions=Game.NUM_ACTIONS, file=None)

following = False
score_ma = MovingAverage(0.001)
wins_ma = MovingAverage(0.001)
steps_ma = MovingAverage(0.0001)
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

    # Get move from agent and perform it
    game.move(agent.nextAction(game.getState(VISION), game.grid))
    # Update game and pass reward to agent
    reward = game.update()
    # Resample state
    agent.sampleStateAction(game.getState(VISION), reward)

    # Drawing
    if following:
        painter.paint()
        pygame.time.wait(200)

    # End game logic
    if game.isGameOver():

        # Stats keeping
        if game.state == Game.WON:
            wins_ma.sample(100)
        elif game.state == Game.LOST:
            wins_ma.sample(0)

        if following or it % 500 == 0:            
            print("avg_target%: "+f2s((score_ma.mean*100/((WIDTH*HEIGHT)-1)))
                  +" avg_score: "+f2s(score_ma.mean)
                  +" wins%: "+f2s(wins_ma.mean)
                  +" avg_steps: "+f2s(steps_ma.mean)
                  +" a.e: "+f2s(agent.epsilon, '6')
                  +" a.a: "+f2s(agent.alpha, '6')
                  +" it: "+str(it)
                  +" states: "+str(agent.stateCount()))
            
            if following:
                pygame.time.wait(1500)
        
        if it % 50000 == 0:
            agent.save()
        it += 1

        score_ma.sample(game.score)
        steps_ma.sample(agent.step)
        
        # Reset game and restart agent
        game.startNew()
        agent.newEpisode()
