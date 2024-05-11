# Test case generator for problem E. Modify this file.

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
    yield "3 11 1 4"
    yield "0 1 2 3 4 5 4 3 2 1 0"
    yield "0 1 2 3 2 1 2 3 3 2 0"
    yield "0 1 2 3 5 5 5 5 5 2 0"


def test_output(input_: list, output: str) -> bool:
    """
    Receives the original generated input and the output from the solution as a raw string.
    """
    return output.rstrip("\n") == "4"



