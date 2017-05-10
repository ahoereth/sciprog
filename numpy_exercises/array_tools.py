"""Scientific programming in python exercice 4."""
from math import ceil

import numpy as np


def sub_array(array, shape, center, fill=None):
    """Extract a subarray of an array."""
    array = np.asarray(array)
    height, width = array.shape
    rows, cols = shape
    row, col = center
    tlr, tlc = row - ceil(rows / 2) + 1, col - ceil(cols / 2) + 1
    brr, brc = tlr + rows, tlc + cols
    result = array[max(tlr, 0):brr, max(tlc, 0):brc]
    if fill is not None:
        left = abs(tlc) * (tlc < 0)  # 0 if tlc >= 0 else abs(tlc)
        right = 0 if brc <= width else brc - width
        top = 0 if tlr >= 0 else abs(tlr)
        bottom = 0 if brr <= height else brr - height
        result = np.pad(result, ((top, bottom), (left, right)),
                        mode='constant', constant_values=fill)
    return result


def test():
    """Test the implementation with the examples from the homework sheet and
       more.

    Props to @shoeffner
    """
    in_array = np.asarray(range(1, 31)).reshape(5, 6)

    out_array_0 = np.array([
        [8, 9, 10],
        [14, 15, 16],
        [20, 21, 22]
    ])

    out_array_1 = np.array([
        [8, 9, 10],
        [14, 15, 16],
        [20, 21, 22],
        [26, 27, 28]
    ])

    out_array_2 = np.array([
        [13, 14, 15, 16, 17],
        [19, 20, 21, 22, 23],
        [25, 26, 27, 28, 29],
    ])

    out_array_3 = np.array([
        [9, 10, 11, 12, 1],
        [15, 16, 17, 18, 1],
        [21, 22, 23, 24, 1],
        [27, 28, 29, 30, 1],
        [1, 1, 1, 1, 1],
    ])

    out_array_4 = np.array([
        [13, 14, 15, 16, 17, 18],
        [19, 20, 21, 22, 23, 24],
        [25, 26, 27, 28, 29, 30],
    ])

    out_array_5 = np.array([
        [1, 1, 1],
        [1, 1, 2],
        [1, 7, 8],
    ])

    out_array_6 = np.pad(in_array, 1, 'constant', constant_values=1)

    out_array_7 = np.pad(in_array, 3, 'constant', constant_values=2)

    test0 = np.all(sub_array(in_array, (3, 3), (2, 2)) == out_array_0)
    assert test0, 'Test 0:\n' + str(sub_array(in_array, (3, 3), (2, 2)))

    test1 = np.all(sub_array(in_array, (4, 3), (2, 2)) == out_array_1)
    assert test1, 'Test 1:\n' + str(sub_array(in_array, (4, 3), (2, 2)))

    test2 = np.all(sub_array(in_array, (4, 5), (3, 2)) == out_array_2)
    assert test2, 'Test 2:\n' + str(sub_array(in_array, (4, 5), (3, 2)))

    test3 = np.all(sub_array(in_array, (5, 5), (3, 4), 1) == out_array_3)
    assert test3, 'Test 3:\n' + str(sub_array(in_array, (4, 5), (3, 4), 1))

    test4 = np.all(sub_array(in_array, (4, 6), (3, 2)) == out_array_4)
    assert test4, 'Test 4:\n' + str(sub_array(in_array, (4, 6), (3, 2)))

    test5 = np.all(sub_array(in_array, (3, 3), (0, 0), 1) == out_array_5)
    assert test5, 'Test 5:\n' + str(sub_array(in_array, (3, 3), (0, 0), 1))

    test6 = np.all(sub_array(in_array, (7, 8), (2, 2), 1) == out_array_6)
    assert test6, 'Test 6:\n' + str(sub_array(in_array, (7, 8), (2, 2), 1))

    test7 = np.all(sub_array(in_array, (11, 12), (2, 2), 2) == out_array_7)
    assert test7, 'Test 7:\n' + str(sub_array(in_array, (11, 12), (2, 2), 2))

    testx = np.all(sub_array(array=in_array, shape=(4, 3), center=(2, 2),
                             fill=None) == out_array_1)
    assert testx, 'Test x:\nNamed args do not work'


if __name__ == '__main__':
    # Some random tests used while implementing.
    A = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]
    B = [[5, 6],
         [8, 9]]
    assert np.all(sub_array(A, (2, 2), (1, 1)) == B)
    C = [[2, 3],
         [5, 6],
         [8, 9]]
    assert np.all(sub_array(A, (3, 2), (1, 1)) == C)
    assert np.all(sub_array(A, (2, 2), (2, 2)) == [[9]])
    D = [[9, 0],
         [0, 0]]
    assert np.all(sub_array(A, (2, 2), (2, 2), fill=0) == D)
    E = [[0, 0, 0],
         [0, 1, 2],
         [0, 4, 5]]
    assert np.all(sub_array(A, (3, 3), (0, 0), fill=0) == E)
    F = [[1, 2, 3, 4, 5, 6],
         [7, 8, 9, 10, 11, 12],
         [13, 14, 15, 16, 17, 18],
         [19, 20, 21, 22, 23, 24],
         [25, 26, 27, 28, 29, 30]]
    G = [[0, 0, 7, 8, 9],
         [0, 0, 13, 14, 15],
         [0, 0, 19, 20, 21]]
    assert np.all(sub_array(F, (3, 5), (2, 0), 0) == G)

    # More tests used for verification after finishing the implementation.
    # Props @shoeffner
    test()
