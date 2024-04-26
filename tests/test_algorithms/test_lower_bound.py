from fastsnake.algorithms.lower_bound import *

import random


def test_lower_bound():
    assert lower_bound([], 0) == -1
    assert lower_bound([0], 0) == 0
    assert lower_bound([0, 1], 0) == 0
    assert lower_bound([0, 1, 2], 0) == 0
    assert lower_bound([0, 1, 2], 1) == 1
    assert lower_bound([0, 1, 1, 2], 1) == 1
    assert lower_bound([0, 1, 1, 1, 2], 1) == 1
    assert lower_bound([0, 1, 1, 1, 2], 2) == 4
    assert lower_bound([0, 1, 1, 1, 2], 10) == -1
    assert lower_bound([0, 1, 1, 1, 2], -10) == 0
    assert lower_bound([1, 2, 3, 4, 5], 0) == 0
    assert lower_bound([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 200, 3000, 9300], 1) == 1
    assert lower_bound([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 200, 3000, 9300], 9) == 6
    assert lower_bound([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 200, 3000, 9300], 150) == 11
    assert lower_bound([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 150, 200, 3000, 9300], 150) == 11
    assert lower_bound([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 150, 150, 200, 3000, 9300], 150) == 11
    assert lower_bound([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 150, 150, 200, 3000, 9300], 10) == 7