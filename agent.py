import os
import numpy as np
import random
import pickle
import game

QSTATE_ACTION_VALUE_INITIAL = 1000000

class QState:

    def __init__(self, num_actions):
        self.num_actions = num_actions
        self.action_values = [QSTATE_ACTION_VALUE_INITIAL for _ in range(self.num_actions)]
        self.new = True

    def getMaxActionValue(self):
        return max(self.action_values)

    def getArgMaxActionValue(self):
        m = self.getMaxActionValue()
        idx = [i for i, v in enumerate(self.action_values) if v == m]
        if len(idx) == 1:
            return idx[0]
        else:
            idx.sort()
            return idx[0]

    def firstVisit(self):
        return self.new

    def update(self, action, next_state_max, reward, alpha, gamma):
        if self.new: self.new = False
        delta = reward + (gamma*next_state_max) - self.action_values[action]
        self.action_values[action] += alpha * delta

class Agent:

    def __init__(self, epsilon, alpha, gamma, num_actions, file):
        self.file = file
        self.q = {}
        self.load()
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.num_actions = num_actions
        self.newEpisode()

    def load(self):
        if self.file == None: return
        try:
            with open(self.file, 'rb') as f:
                self.__dict__.update(pickle.load(f))
                print("Loaded agent from file")
        except EnvironmentError:
            print("Error loading agent from file, starting fresh")

    def save(self):
        if self.file == None: return
        try:
            with open(self.file, 'wb') as f:
                pickle.dump(self.__dict__, f)
                print("Saved agent to file - "+str(int(os.path.getsize(self.file)/(1024*1024)))+"MB")

        except EnvironmentError:
            print("Error saving agent to file")

    def stateCount(self):
        return len(self.q)

    def newEpisode(self):
        self.step = 0
        self.length = 0
        self.prev_state = None
        self.last_action = None

    def lowerAlpha(self):
        self.alpha -= 0.01
        if(self.alpha <= 0):
            self.alpha = 0
        return self.alpha

    def increaseAlpha(self):
        self.alpha += 0.01
        if(self.alpha >= 1):
            self.alpha = 1
        return self.alpha

    def lowerEpsilon(self):
        self.epsilon -= 0.01
        if(self.epsilon <= 0):
            self.epsilon = 0
        return self.epsilon

    def increaseEpsilon(self):
        self.epsilon += 0.01
        if(self.epsilon >= 1):
            self.epsilon = 1
        return self.epsilon

    def getQforState(self, state):
        if state not in self.q:
            # New state, gen action history for state
            self.q[state] = QState(self.num_actions)
        return self.q[state]

    def sampleStateAction(self, state, reward):
        # Update epsilon
        self.step += 1
        # if self.epsilon > 0:
        #     self.epsilon = self.epsilon * 0.99999
        #     if self.epsilon < 1e-5: self.epsilon = 0
        # if self.alpha > 0:
        #     self.alpha = self.alpha * 0.999995
        # Keep track of length
        self.length += 1 if reward > 0 else 0
        # Q update
        if self.prev_state != None and self.last_action != None:
            qs_prev = self.getQforState(self.prev_state)
            next_max = self.getQforState(state).getMaxActionValue()
            qs_prev.update(self.last_action,
                           next_max,
                           reward,
                           self.alpha,
                           self.gamma)
        # Update latest state
        self.prev_state = state

    def nextAction(self, state, grid):
        # Get actions
        qs = self.getQforState(state)
        # Little boost to get started
        if self.length == 0 and qs.firstVisit():
            self.last_action = grid.fruitDirectionActionIdx()
        # Take random action with epsilon probability
        elif self.epsilon > 0 and np.random.random() < self.epsilon:
            # # Take only positive
            # positive_action_indices = list(filter(lambda x: qs.action_values[x] > 0, range(self.num_actions)))
            # # If there are no positive action values, we've trapped ourselves; pick random
            # if len(positive_action_indices) == 0:
            positive_action_indices = list(range(self.num_actions))
            self.last_action = random.choice(positive_action_indices)
        else:
            # Sort by reward
            self.last_action = qs.getArgMaxActionValue()

        return self.last_action