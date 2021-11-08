from Env.env import *


@njit(parallel=True)
def NORMALIZE(mat):
    mat = np.where(mat < 0, 0, mat)
    for idx_r in range(len(mat)):
        mat[idx_r] /= np.sum(mat[idx_r])
    return mat