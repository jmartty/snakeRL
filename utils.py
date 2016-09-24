class MovingAverage:

    def __init__(self, rate):
        self.mean = 0.0
        self.rate = rate

    def sample(self, value):
        self.mean += self.rate*(value - self.mean)

def f2s(f):
    return "{0:.2f}".format(f)