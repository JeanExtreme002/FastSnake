from fastsnake.algorithms.min_coins import *


def test_min_coins():
    assert min_coins([1, 3, 5, 9], 0) == 0
    assert min_coins([1, 3, 5, 9], 1) == 1
    assert min_coins([1, 3, 5, 9], 2) == 2
    assert min_coins([1, 3, 5, 9], 3) == 1
    assert min_coins([1, 3, 5, 9], 4) == 2
    assert min_coins([1, 3, 10, 9], 5) == 3
    assert min_coins([1, 3, 6, 10, 15], 20) == 2
    assert min_coins([1, 3, 6, 10, 15], 26) == 3
    assert min_coins([1, 3, 6, 10, 15], 98) == 8