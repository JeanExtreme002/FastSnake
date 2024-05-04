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
    yield gen_int(0, 100)
    yield gen_int_array(10, 0, 100)
    yield gen_string(10, string.ascii_uppercase)
    yield gen_string_array(10, 1, 20, string.ascii_uppercase + string.ascii_lowercase)


def test_output(input_: list, output: str) -> bool:
    """
    Receives the original generated input and the output from the solution as a raw string.
    """
    output = output.split('\n')
    input_.pop(0)  # Remove number of test cases

    lines_per_test_case = 2
    lines_per_output = 1
    lptc = lines_per_test_case
    lpo = lines_per_output

    for index in range(len(output)):  # This is just a template. Change it as needed.
        test_case_lines = input_[index * lptc: index * lptc + lptc]
        output_lines = output[index * lpo: index * lpo + lpo]

        for output_line in output_lines:
            output_line = [int(x.strip()) for x in output_line.split()]
            pass  # Check output here ...

    raise NotImplementedError()

