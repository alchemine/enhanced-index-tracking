from Env.env import *


@njit
def NORMALIZE(arr):
    arr = np.where(arr < 0, 0, arr)
    return arr / np.sum(arr)
