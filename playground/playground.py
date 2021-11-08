import numpy as np
from numba import njit


@njit
def f(shape):
    arr = np.zeros(shape, dtype=np.uint8)
    return arr


if __name__ == '__main__':
    f(shape=(10, 10))
