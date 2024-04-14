from fastsnake.algorithms.mex import *

import random


def test_mex():
    assert mex([]) == 0
    assert mex([1]) == 0
    assert mex([0]) == 1
    assert mex([0, 1]) == 2
    assert mex([0, 1, 2, 3, 5, 6, 7]) == 4
    assert mex([0, 1, 2, 3, 4, 9]) == 5
    assert mex([0, 1, 2, 4, 9]) == 3

    array = list(range(0, 10**6))

    # Mex must be N = max(array) + 1
    assert mex(array) == 10**6
    
    # Mex must be between 1000 and 90000
    value = random.randint(10**4, (10**5) * 9)
    random.shuffle(array)
    array.remove(value)

    assert mex(array) == value

    # Mex must be between 100 and 9000
    value = random.randint(10**2, (10**3) * 9)
    random.shuffle(array)
    array.remove(value)

    assert mex(array) == value

    # Mex must be the constant 1
    array.remove(1)
    random.shuffle(array)

    assert mex(array) == 1
