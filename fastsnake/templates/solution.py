# [START STEP COUNTER]

import sys

# Python is NOT recommended for recursive solutions.
# If you use PyPy, consider removing the line below.
sys.setrecursionlimit(2 * 10**9)

# Optimizations to speed up input and output.
def optimized_input(remove_newline: bool = True):
    string = sys.stdin.readline()
    return string.rstrip("\n") if remove_newline else string

def optimized_print(*args, end="\n"):
    sys.stdout.write(" ".join(map(str, args)) + end)

# Set by default, as this input customization is generally better.
input = optimized_input

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

# [WARNING]: Just remove the fastsnake code below if you will not use it.
# ======================================================================
from fastsnake.entries import *
put = input
puti = input_int
putf = input_float
puta = input_int_array   # Other: input_float_array
putm = input_int_matrix  # Other: input_{char, float, string}_array
# ======================================================================

print = optimized_print

# >>> HEY, RIGHT HERE!! Write your code below:
# Remember, sometimes the solution is much simpler than you think S2
import math

for test_case in range(int(input())):
    n = int(input())
    pass


# [WARNING]: THIS IS AN **UNCOMPILED** SOLUTION!! Remember to REMOVE fastsnake code if you will NOT COMPILE this code.


