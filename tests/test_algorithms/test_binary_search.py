from fastsnake.algorithms.binary_search import *

import random


def test_binary_search():
    assert binary_search([], 0) == -1
    assert binary_search([0], 0) == 0
    assert binary_search([0, 1], 0) == 0
    assert binary_search([0, 1, 2], 0) == 0
    assert binary_search([0, 1, 2], 1) == 1
    assert binary_search([0, 1, 1, 2], 1) in [1, 2]
    assert binary_search([0, 1, 1, 1, 2], 1) in [1, 2, 3]
    assert binary_search([0, 1, 1, 1, 2], 2) == 4
    assert binary_search([0, 1, 1, 1, 2], 10) == -1
    assert binary_search([0, 1, 1, 1, 2], -10) == -1
    assert binary_search([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 200, 3000, 9300], 9) == 6
    assert binary_search([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 200, 3000, 9300], 150) == 11
    assert binary_search([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 200, 3000, 9300], 10) == -1