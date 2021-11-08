from functools import wraps
from collections import defaultdict

class Logger:
    level = 1
    level_val = defaultdict(lambda: 1)

def L(fn):
    @wraps(fn)
    def log(*args, **kwargs):
        print("Enter")
        print(f"-- {fn.__name__} : level: {Logger.level}, val: {Logger.level_val[Logger.level]}")
        Logger.level += 1
        rst = fn(*args, **kwargs)
        print("Exit")
        Logger.level -= 1
        Logger.level_val[Logger.level] += 1
        return rst
    return log



@L
def A(x):
    pass

@L
def B(x):
    BA(x)
    BB(x)

@L
def BA(x):
    BAA(x)

@L
def BB(x):
    pass

@L
def BAA(x):
    pass

@L
def C(x):
    CA(x)

@L
def CA(x):
    pass


if __name__ == "__main__":
    A(1)
    B(1)
    C(1)
