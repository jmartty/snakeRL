import numpy as np
import random
import pickle

QSTATE_ACTION_VALUE_INITIAL = 16

class QState:

    def __init__(self, num_actions):
        self.num_actions = num_actions
        self.action_values = [QSTATE_ACTION_VALUE_INITIAL for _ in range(self.num_actions)]
        self.new = True

    def getMaxActionValue(self):
        return max(self.action_values)

    def getArgMaxActionValue(self):
        idx = [i[0] for i in sorted(enumerate(self.action_values), key=lambda x:x[1])]
        return idx[-1]

    def firstVisit(self):
        return self.new

    def update(self, action, next_state_max, reward, alpha, gamma):
        self.action_values[action] += alpha * (reward + gamma*next_state_max - self.action_values[action])
        self.new = False

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
                print("Saved agent to file")
        except EnvironmentError:
            print("Error saving agent to file")

    def stateCount(self):
        return len(self.q)

    def newEpisode(self):
        self.step = 0
        self.length = 0
        self.prev_state = None
        self.last_action = None

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
        self.step += 1
        self.length += 1 if reward > 0 else 0
        if self.prev_state != None and self.last_action != None:
            qs_prev = self.getQforState(self.prev_state)
            qs_prev.update(self.last_action,
                           self.getQforState(state).getMaxActionValue(),
                           reward,
                           self.alpha,
                           self.gamma)

    def nextAction(self, state):
        # Get actions
        qs = self.getQforState(state)
        # Take random action with epsilon probability or if we dont have any info on the future
        if self.length == 0 or qs.firstVisit() or (np.random.random() < self.epsilon):
            # # Take only positive
            positive_action_indices = list(filter(lambda x: qs.action_values[x] > 0, range(self.num_actions)))
            # If there are no positive action values, we've trapped ourselves; pick random
            if len(positive_action_indices) == 0:
                positive_action_indices = list(range(self.num_actions))
            self.last_action = random.choice(positive_action_indices)
        else:
            # Sort by reward
            self.last_action = qs.getArgMaxActionValue()

        self.prev_state = state
        return self.last_action