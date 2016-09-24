import numpy as np
import pickle

class ActionHistory:

    def __init__(self):
        self.count = 0
        self.mean_reward = 0.0

    def sample(self, value):
        self.count += 1
        self.mean_reward += 1/self.count * (value - self.mean_reward)

class Agent:

    def __init__(self, epsilon, num_actions, file):
        self.epsilon = epsilon
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
        self.acc_reward = 0
        self.step = 0

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
            self.q[state] = [ActionHistory() for _ in range(self.num_actions)]
        return self.q[state]

    def sampleStateAction(self, state, value):
        self.step += 1
        self.acc_reward += (0.95 ** self.step) * value
        q = self.getQforState(state)
        q[self.last_action].sample(self.acc_reward)

    def nextAction(self, state):
        if np.random.random() < self.epsilon:
            # Explore action at random
            self.last_action = np.random.randint(0, self.num_actions)
            return self.last_action
        else:
            # Exploit best known action at the moment
            actions = self.getQforState(state)
            max_val = max([a.mean_reward for a in actions])
            self.last_action = actions.index(next(a for a in actions if a.mean_reward == max_val))
            return self.last_action