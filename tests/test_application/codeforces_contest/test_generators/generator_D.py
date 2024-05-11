# Test case generator for problem D. Modify this file.

from typing import Generator
import random
import string


def gen_int(start: int, end: int):
    return random.randint(start, end)


def gen_int_array(size: int, start: int, end: int):
    return ' '.join(str(gen_int(start, end)) for _ in range(size))


def gen_string(size: int, letters: str = string.ascii_lowercase):
    return ''.join(random.choice(letters) for _ in range(size))


def gen_string_array(size: int, start: int, end: int, letters: str = string.ascii_lowercase):
    return ' '.join(gen_string(gen_int(start, end), letters) for _ in range(size))


def generate(test_id: int) -> Generator:  # Yield any data type (it will be converted to str later)
    # Sample code ...
    yield 1
    yield [10, 7, 4]
    yield "2 ?"
    yield "9 1"
    yield "4 ?"
    yield "7 0"
    yield "2 0"
    yield "8 1"
    yield "5 ?"


def test_output(input_: list, output: str) -> bool:
    """
    Receives the original generated input and the output from the solution as a raw string.
    """
    lines = output.split("\n")
    return lines[0] == "4" and lines[1] == "3 5 7 9"


