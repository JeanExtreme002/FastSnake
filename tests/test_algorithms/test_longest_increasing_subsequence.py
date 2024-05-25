from fastsnake.algorithms.longest_increasing_subsequence import *

import random


def test_longest_increasing_subsequence():
    assert lis([]) == 0
    assert lis([1]) == 1
    assert lis(range(100)) == 100
    assert lis([1, 2, 3, 4, -1, 6, 7, 8, 9]) == 8
    assert lis([1, 2, 3, -20, -1, 6, 7, 8, 9]) == 7
    assert lis([1, 2, -3, -20, -1, 6, 7, 8, 9]) == 6
    assert lis([1, 2, -3, -20, -1, 6, 7, 4, 9]) == 5
    assert lis([1, 2, -3, -20, -1, 6, 7, 4, 5]) == 4
    assert lis([1, 2, -3, -20, -1, 6, 7, 4, 5, 8]) == 5
    assert lis([1, 2, -3, -20, -1, 6, 7, 4, 5, 8, 9]) == 6
    assert lis([1, 2, -3, -20, -1, 6, 7, 4, 5, 8, 9, 10]) == 7
    assert lis([1, 2, -3, -20, -1, 6, 7, 3, -4, -5, -9, -10]) == 4
    assert lis([1, 2, -3, -20, -1, -6, -7, 3, 4, -5, -9, -10]) == 4
    assert lis([1, 2, -3, -20, -1, 6, 7, 3, 4, -5, -9, -10]) == 4
    assert lis([1, 2, -3, -20, -1, 6, 7, 3, 4, 5, -10]) == 5
