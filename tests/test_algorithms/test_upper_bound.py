from fastsnake.algorithms.upper_bound import *

import random


def test_upper_bound():
    assert upper_bound([], 0) == -1
    assert upper_bound([0], 0) == 0
    assert upper_bound([0, 1], 0) == 0
    assert upper_bound([0, 1, 2], 0) == 0
    assert upper_bound([0, 1, 2], 1) == 1
    assert upper_bound([0, 1, 1, 2], 1) == 2
    assert upper_bound([0, 1, 1, 1, 2], 1) == 3
    assert upper_bound([0, 1, 1, 1, 2], 2) == 4
    assert upper_bound([0, 1, 1, 1, 2], 10) == -1
    assert upper_bound([0, 1, 1, 1, 2], -10) == -1
    assert upper_bound([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 200, 3000, 9300], 1) == 3
    assert upper_bound([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 200, 3000, 9300], 9) == 6
    assert upper_bound([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 200, 3000, 9300], 150) == 11
    assert upper_bound([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 150, 200, 3000, 9300], 150) == 12
    assert upper_bound([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 150, 150, 200, 3000, 9300], 150) == 13
    assert upper_bound([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 150, 150, 200, 3000, 9300], 10) == -1