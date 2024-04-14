from fastsnake.algorithms.knapsack import *


def test_knapsack():
    assert knapsack([], [], 10) == 0
    assert knapsack([1], [1], 10) == 1
    assert knapsack([10], [10], 10) == 10
    assert knapsack([10], [11], 10) == 0
    assert knapsack([10, 20, 50, 40, 40, 30], [10, 10, 10, 10, 10, 10], 10) == 50
    assert knapsack([10, 7, 15], [5, 3, 7], 10) == 22
    assert knapsack([60, 100, 120, 30, 70, 110], [10, 20, 30, 5, 15, 25], 50) == 260
    assert knapsack([60, 100, 120, 30, 70, 110], [10, 20, 30, 5, 15, 25], 65) == 310