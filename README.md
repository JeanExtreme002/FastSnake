# FastSnake

[![Python Package](https://github.com/JeanExtreme002/FastSnake/workflows/Python%20Package/badge.svg)](https://github.com/JeanExtreme002/FastSnake/actions)
[![Pypi](https://img.shields.io/pypi/v/FastSnake?logo=pypi)](https://pypi.org/project/FastSnake/)
[![License](https://img.shields.io/pypi/l/FastSnake)](https://github.com/JeanExtreme002/FastSnake)
[![Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20Linux-8A2BE2)](https://pypi.org/project/FastSnake/)
[![Python Version](https://img.shields.io/badge/python-3.7+-yellow)](https://pypi.org/project/FastSnake/)
[![Downloads](https://static.pepy.tech/personalized-badge/fastsnake?period=total&units=international_system&left_color=grey&right_color=orange&left_text=downloads)](https://pypi.org/project/FastSnake/)

FastSnake is a command-line tool that allows you to easily create, expand, run, and test Python / C++ solutions for competitive programming problems, besides automatically downloading test cases from the best contest platforms.

This project provides useful CLI tools for competitive programming, such as test case generators, algorithms and data structures, tools for platforms Codeforces and AtCoder, and other features that assist you during the development and testing of solutions.

## Installing FastSnake:
```
$ pip install FastSnake
```

Use one of the commands below to check if the installation was successful.
```
$ fastsnake -v
```
or
```
$ python3 -m fastsnake -v
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
$ fastsnake test <problem>
```

You can also create your own generator, at `test_generators` folder, to bruteforce your solution.
```
$ fastsnake test <problem> -g <n_tests>
```
*Note:* By default, FastSnake will analyze the output with case sensitivity. However, you can enable case-insensitive analysis by using the `--case-insensitive` flag.


### Starting a Custom Contest
Use the command below to start your own contest.
```
$ fastsnake start-custom-contest <n_problems>
```

### Algorithms and Structures

FastSnake provides some algorithms and structures that can be injected to your final solution. See the sample below:

**Python Solution:**
```py
from fastsnake.algorithms.min_coins import *

coins = []

for x in input().split():
    coins.append(int(x))

value = int(input())

result = min_coins(coins, value)
print(result)
```
Use the argument `--list <algorithms | structures | external>` to see all algorithms and structures provided by FastSnake.

**Injecting the algorithm to the final solution...**
```
$ fastsnake compile main.py
```
Check out the code of the generated Python module.
<br>

### Testing and Compiling
You may test and compile your solution using the command below:
```
$ fastsnake test <problem> -c
```
If the solution was accepted at all test cases, it will be compiled.


### Adding External Modules
You may also add your own modules to the external package of fastsnake.
```
$ fastsnake add-external <path | url> --name <module_name> [--url]
```
For downloading the module from web, use the flag `--url`.


## Step Counter
The `--step-counter` flag of the command `test` can be used to count the approximate number of steps executed by your solution. 

By default, it analyzes the entire code, but you can set a starting point by adding the following comment on the line:
```
# [START STEP COUNTER]
...
```
**Note:** The step counter only analyzes the code that has been required for testing. This means that if you don't compile your code before testing using the `--compile-before` flag, it won't consider fastsnake algorithms and structures.

## Support for C++ Language
You may use C++ language to solve contests by using the flag `--cpp` when starting a contest. 

However, some features available in the Python language won't yet be available for C++. 

## More Information
Use the following command for more information about FastSnake CLI:
```
$ fastsnake -h
```
