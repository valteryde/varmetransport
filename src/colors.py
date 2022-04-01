WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
GREY = (120,120,120)

class Gradient:
    """Rainbow"""
    #https://colordesigner.io/gradient-generator

    def __init__(self, a, b, gradient):
        self.gradient = gradient
        self.a = a #small border
        self.b = b #large border
        self.lengthm1 = len(self.gradient) - 1


    def get(self, val, procent=False):
        if val >= self.b:
            res = self.gradient[-1]
        elif val <= self.a:
            res = self.gradient[0]
        else:
            res = self.gradient[round(((val - self.a) / self.b) * self.lengthm1)]
        if procent:
            return tuple(map(lambda v: v/255, res))
        return res

def dround(val, d):
    return round(val * (10**d)) / (10**d)
