import numpy as np
import random
import pickle

class ActionHistory:

    def __init__(self):
        self.count = 0
        self.mean_reward = 0.0

    def sample(self, value):
        self.count += 1
        self.mean_reward += 1/self.count * (value - self.mean_reward)

class Agent:

    def __init__(self, epsilon, beta, num_actions, file):
        self.epsilon = epsilon
        self.beta = beta
        self.q = {}
        self.num_actions = num_actions
        self.last_action = None
        self.newEpisode()
        self.file = file
        self.load()

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

    def stateActionCount(self):
        s = 0
        for k,v in self.q.items():
            s += len(v)
        return s

    def newEpisode(self):
        self.acc_reward = 1000
        self.step = 0

    def lowerEpsilon(self):
        self.epsilon -= 1
        if(self.epsilon <= 1):
            self.epsilon = 1
        return self.epsilon

    def increaseEpsilon(self):
        self.epsilon += 1
        if(self.epsilon >= 4):
            self.epsilon = 4
        return self.epsilon

    def lowerBeta(self):
        self.beta -= 0.1
        if(self.beta <= 0):
            self.beta = 0
        return self.beta

    def increaseBeta(self):
        self.beta += 0.1
        if(self.beta >= 1):
            self.beta = 1
        return self.beta

    def getQforState(self, state):
        if state not in self.q:
            # New state, gen action history for state
            self.q[state] = [ActionHistory() for _ in range(self.num_actions)]
        return self.q[state]

    def sampleStateAction(self, state, value):
        self.step += 1
        self.acc_reward += (0.95 ** self.step) * value
        q = self.getQforState(state)
        q[self.last_action].sample(self.acc_reward)

    def nextAction(self, state):
        actions = self.getQforState(state)
        # Sort by reward
        positive_action_indices = [i[0] for i in sorted(enumerate(actions), key=lambda x:x[1].mean_reward)][::-1]
        # Take only positive
        positive_action_indices = list(filter(lambda x: actions[x].mean_reward >= 0, range(4)))
        # If there are no positive actions, we've trapped ourselves; pick random
        if len(positive_action_indices) == 0:
            positive_action_indices = list(range(4))
        # Take epsilon elements or all with beta probability
        if (np.random.random() < self.beta):
            self.last_action = random.choice(positive_action_indices)
        else:
            self.last_action = random.choice(positive_action_indices[:self.epsilon])
        return self.last_action