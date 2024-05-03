from fastsnake.application.config import contest_config_filename

import json
import os

def start_contest(
    solutions_namespace: str,
    test_cases_namespace: str, 
    test_generators_namespace: str, 
    contest_id: int, 
    problems: list[str]
) -> None:
    """
    Start a contest at the directory.
    """
    config = {
        "solutions_namespace": solutions_namespace,
        "test_cases_namespace": test_cases_namespace,
        "test_generators_namespace": test_generators_namespace,
        "contest_id": contest_id,
        "problems": problems
    }

    # Create folder with Python modules for writting solutions.
    if not os.path.exists(config["solutions_namespace"]):
        os.mkdir(config["solutions_namespace"])

    if os.path.exists(config["solutions_namespace"]):
        for filename in os.listdir(config["solutions_namespace"]):
            os.remove(os.path.join(config["solutions_namespace"], filename))

    if os.path.exists(config["test_generators_namespace"]):
        for filename in os.listdir(config["test_generators_namespace"]):
            os.remove(os.path.join(config["test_generators_namespace"], filename))

    for problem in config["problems"]:
        with open(os.path.join(config["solutions_namespace"], problem.upper() + ".py"), "w") as file:
            file.write("# Solution for problem " + problem + "\n\n")
            file.write("# [START STEP COUNTER]\n\n")
            file.write("# Python is NOT recommended for recursive solutions.\n")
            file.write("import sys\n")
            file.write("sys.setrecursionlimit(2 * 10**9)\n")
            file.write("\n")
            file.write("# Time-complexity of Python implementations: https://wiki.python.org/moin/TimeComplexity\n")
            file.write("# A deque (double-ended queue) is a doubly linked list. Complexity O(1) for append and pop operations.\n")
            file.write("# Add elements with the method append (left to right). Use it as a stack (pop) or as a queue (popLeft).\n\n")
            file.write("from collections import deque\n")
            file.write("\n")
            file.write("# Priority Queue Algorithm [Complexity O(log(n))]: https://docs.python.org/3/library/heapq.html\n")
            file.write("# Use the heapq.heapify(x) to transform a list into a heap. All functions will use this transformed list.\n")
            file.write("# Hint: heapq.heapreplace(...) is more efficient than a heappop(...) followed by heappush(...)\n\n")
            file.write("import heapq\n")
            file.write("\n\n")
            file.write("# IMPORT FASTSNAKE ALGORITHMS OR STRUCTURES OR YOUR EXTERNAL MODULES.\n")
            file.write("# from fastsnake.algorithms.something import *\n")
            file.write("# from fastsnake.structures.something import *\n")
            file.write("# from fastsnake.external.your_external_module import *\n")
            file.write("\n")
            file.write("# Just remove the fastsnake code below if you will not use it.\n")
            file.write("# " + "=" * 70 + "\n")
            file.write("from fastsnake.entries import *\n")
            file.write("put = input\n")
            file.write("puti = input_int\n")
            file.write("putf = input_float\n")
            file.write("puta = input_int_array   # Other: input_float_array\n")
            file.write("putm = input_int_matrix  # Other: input_{char, float, string}_array\n")
            file.write("# " + "=" * 70 + "\n")
            file.write("\n")
            file.write("# >>> HEY, RIGHT HERE!! Write your code below:\n")
            file.write("# Remember, sometimes the solution is much simpler than you think S2\n")
            file.write("\n")
            file.write("for test_case in range(int(input())):\n")
            file.write("    n = int(input())\n")
            file.write("    pass\n")
            file.write("\n\n")
            file.write("# [WARNING]: THIS IS AN **UNCOMPILED** SOLUTION!! Remember to REMOVE fastsnake code if you will NOT COMPILE this code.\n")
            file.write("\n\n")

    # Create folder with Python modules for writting test case generators.
    if not os.path.exists(config["test_generators_namespace"]):
        os.mkdir(config["test_generators_namespace"])

    for filename in os.listdir(config["test_generators_namespace"]):
        os.remove(os.path.join(config["test_generators_namespace"], filename))

    for problem in config["problems"]:
        with open(os.path.join(config["test_generators_namespace"], "generator_" + problem.upper() + ".py"), "w") as file:
            file.write("# Test case generator for problem " + problem + ". Modify this file.\n\n")
            file.write("from typing import Generator\n")
            file.write("import random\n")
            file.write("import string\n")
            file.write("\n\n")
            file.write("def gen_int(start: int, end: int):\n")
            file.write("    return random.randint(start, end)\n")
            file.write("\n\n")
            file.write("def gen_int_array(size: int, start: int, end: int):\n")
            file.write("    return ' '.join(str(gen_int(start, end)) for _ in range(size))\n")
            file.write("\n\n")
            file.write("def gen_string(size: int, letters: str = string.ascii_lowercase):\n")
            file.write("    return ''.join(random.choice(letters) for _ in range(size))\n")
            file.write("\n\n")
            file.write("def gen_string_array(size: int, start: int, end: int, letters: str = string.ascii_lowercase):\n")
            file.write("    return ' '.join(gen_string(gen_int(start, end), letters) for _ in range(size))\n")
            file.write("\n\n")
            file.write("def generate(test_id: int) -> Generator:  # Yield any data type (it will be converted to str later)\n")
            file.write("    # Sample code ...\n")
            file.write("    yield gen_int(0, 100)\n")
            file.write("    yield gen_int_array(10, 0, 100)\n")
            file.write("    yield gen_string(10, string.ascii_uppercase)\n")
            file.write("    yield gen_string_array(10, 1, 20, string.ascii_uppercase + string.ascii_lowercase)\n")
            file.write("\n\n")
            file.write("def test_output(input_: list, output: str) -> bool:\n")
            file.write("    \"\"\"\n")
            file.write("    Receives the original generated input and the output from the solution as a raw string.\n")
            file.write("    \"\"\"\n")
            file.write("    output = output.split('\\n')\n")
            file.write("    input_.pop(0)  # Remove number of test cases\n")
            file.write("\n")
            file.write("    lines_per_test_case = 2\n")
            file.write("    lines_per_output = 1\n")
            file.write("    lptc = lines_per_test_case\n")
            file.write("    lpo = lines_per_output\n")
            file.write("\n")
            file.write("    for index in range(len(output)):  # This is just a template. Change it as needed.\n")
            file.write("        test_case_lines = input_[index * lptc: index * lptc + lptc]\n")
            file.write("        output_lines = output[index * lpo: index * lpo + lpo]\n")
            file.write("\n")
            file.write("        for output_line in output_lines:\n")
            file.write("            output_line = [int(x.strip()) for x in output_line.split()]\n")
            file.write("            pass  # Check output here ...\n")
            file.write("\n")
            file.write("    raise NotImplementedError()\n")
            file.write("\n")

    # Create config file.
    with open(contest_config_filename, "w") as file:
        file.write(json.dumps(config))

