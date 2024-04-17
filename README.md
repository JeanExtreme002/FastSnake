# FastSnake

[![Python Package](https://github.com/JeanExtreme002/FastSnake/workflows/Python%20Package/badge.svg)](https://github.com/JeanExtreme002/FastSnake/actions)
[![Pypi](https://img.shields.io/pypi/v/FastSnake?logo=pypi)](https://pypi.org/project/FastSnake/)
[![License](https://img.shields.io/pypi/l/FastSnake)](https://github.com/JeanExtreme002/FastSnake)
[![Python Version](https://img.shields.io/badge/python-3.7+-8A2BE2)](https://pypi.org/project/FastSnake/)

Tired of having to copy-paste your library code into every solution you write? FastSnake is a command-line tool that allows you to easily create, expand, run and test Python solutions for competitive programming problems.

This project provides useful CLI tools for competitive programming, such as algorithms and data structures, and tools for Codeforces. But you will have to write your own code and library for the problems you want to solve.

## Installing FastSnake:
**For Python with pip:**
```
$ pip install FastSnake
```

## Basic Usage:
Starting a contest from Codeforces...
```
$ fastsnake codeforces -sc <contest_id>
```
**Note:** The contest ID can be found at contest URL `https://codeforces.com/contest/<id>`
<br>

Once you have written your solution, test it.
```
$ fastsnake -t <problem>
```

### Algorithms and Structures

FastSnake provides some algorithms and structures that can be injected to your final solution. See the sample below:

**Python Solution:**
```py
from fastsnake.algorithms.min_coins import *

n = int(input())
coins = []

for x in input().split():
    coins.append(int(x))

value = int(input())

print(min_coins(coins, value))  # Result
```
Use the argument `--list <algorithms | structures>` to see all algorithms and structures provided by FastSnake.

**Injecting the algorithm to the final solution...**
```
$ fastsnake -c main.py
```
Check out the code of the generated Python module.
<br>

### Testing and Compiling:
You may test and compile your solution using the command below:
```
$ fastsnake -tc <problem>
```
If the solution was accepted at all test cases, it will be compiled.
