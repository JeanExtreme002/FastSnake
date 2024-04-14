import sys

from fastsnake.algorithms.binary_search import *

index = binary_search([0, 1, 1, 1, 2, 5, 9, 20, 40, 100, 120, 150, 200, 3000, 9300], 9)

sys.exit(int(binary_search.__module__ != "__main__" or index != 6))

