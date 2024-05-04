# [START STEP COUNTER]

# Python is NOT recommended for recursive solutions.
import sys
sys.setrecursionlimit(2 * 10**9)

# Time-complexity of Python implementations: https://wiki.python.org/moin/TimeComplexity
# A deque (double-ended queue) is a doubly linked list. Complexity O(1) for append and pop operations.
# Add elements with the method append (left to right). Use it as a stack (pop) or as a queue (popLeft).

from collections import deque

# Priority Queue Algorithm [Complexity O(log(n))]: https://docs.python.org/3/library/heapq.html
# Use the heapq.heapify(x) to transform a list into a heap. All functions will use this transformed list.
# Hint: heapq.heapreplace(...) is more efficient than a heappop(...) followed by heappush(...)

import heapq


# IMPORT FASTSNAKE ALGORITHMS OR STRUCTURES OR YOUR EXTERNAL MODULES.
# from fastsnake.algorithms.something import *
# from fastsnake.structures.something import *
# from fastsnake.external.your_external_module import *

# Just remove the fastsnake code below if you will not use it.
# ======================================================================
from fastsnake.entries import *
put = input
puti = input_int
putf = input_float
puta = input_int_array   # Other: input_float_array
putm = input_int_matrix  # Other: input_{char, float, string}_array
# ======================================================================

# >>> HEY, RIGHT HERE!! Write your code below:
# Remember, sometimes the solution is much simpler than you think S2

for test_case in range(int(input())):
    n = int(input())
    pass


# [WARNING]: THIS IS AN **UNCOMPILED** SOLUTION!! Remember to REMOVE fastsnake code if you will NOT COMPILE this code.


