import numpy
from classes.graph.graph import *
from algorithms.bfs import *
import operator
import itertools

def checkIsomorphismMatrix(a : np.array, b : np.array):
    if a.shape != b.shape:
        return False
    n = a.shape[0]
    perms = [i for i in range(0, n)]
    for perm in itertools.permutations(perms):
        matrix = np.zeros((n, n))
        i0 = 0
        for i in perm:
            j0 = 0
            for j in perm:
                matrix[i0][j0] = b[i][j]
                j0 += 1
            i0 += 1
        flag = True
        for i in range(0, n):
            for j in range(0, n):
                if matrix[i][j] != a[i][j]:
                    flag = False
                    break
            if not flag:
                break
        if flag:
            return True
    return False

