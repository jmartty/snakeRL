class MovingAverage:

    def __init__(self, rate):
        self.mean = 0.0
        self.rate = rate

    def sample(self, value):
        self.mean += self.rate*(value - self.mean)

def f2s(f, dec='2'):
    return ("{0:."+dec+"f}").format(f)