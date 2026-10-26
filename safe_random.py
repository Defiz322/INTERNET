import random as _random
import sys

class SafeRandom:
    def __getattr__(self, name):
        return getattr(_random, name)
    
    def randint(self, a, b):
        try:
            if a > b:
                a, b = b, a
            if a == b:
                return a
            return _random.randint(a, b)
        except:
            return a if 'a' in locals() else 0
    
    def randrange(self, *args):
        try:
            if len(args) == 1:
                if args[0] <= 0:
                    return 0
                return _random.randrange(args[0])
            elif len(args) == 2:
                start, stop = args[0], args[1]
                if stop <= start:
                    return start
                return _random.randrange(start, stop)
            elif len(args) == 3:
                start, stop, step = args[0], args[1], args[2]
                if stop <= start:
                    return start
                return _random.randrange(start, stop, step)
            return 0
        except:
            return 0
    
    def choice(self, seq):
        try:
            if not seq:
                return None
            return _random.choice(seq)
        except:
            if seq:
                return seq[0]
            return None
    
    def sample(self, population, k):
        try:
            if not population or k <= 0:
                return []
            pop_list = list(population)
            if k >= len(pop_list):
                k = len(pop_list)
            if k == 0:
                return []
            return _random.sample(pop_list, k)
        except:
            if population:
                pop_list = list(population)
                return pop_list[:min(k, len(pop_list))]
            return []
    
    def shuffle(self, x):
        try:
            _random.shuffle(x)
        except:
            pass
    
    def random(self):
        try:
            return _random.random()
        except:
            return 0.5
    
    def uniform(self, a, b):
        try:
            if a > b:
                a, b = b, a
            return _random.uniform(a, b)
        except:
            return a
    
    def seed(self, *args, **kwargs):
        try:
            _random.seed(*args, **kwargs)
        except:
            pass

sys.modules['random'] = SafeRandom()
