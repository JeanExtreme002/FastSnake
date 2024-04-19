from fastsnake.util.atcoder import *
import os


def test_get_problems():
    problems = get_problems("abc341")
    assert "".join(problems) == "ABCDEFG"


def test_load_problem_test_cases():
    folder = os.path.join(os.path.dirname(__file__), "sample_abc341_E")

    n_input = len([x for x in os.listdir(folder) if x.endswith(".in")])
    n_output = len([x for x in os.listdir(folder) if x.endswith(".out")])

    inputs, outputs = get_problem_test_cases("abc341", "E")

    assert len(inputs) == n_input and len(outputs) == n_output

    for i in range(n_input):
        with open(os.path.join(folder, f"{i}.in")) as file:
            assert file.read().strip().strip("\n") == inputs[i].strip().strip("\n")

    for i in range(n_output):
        with open(os.path.join(folder, f"{i}.out")) as file:
            assert file.read().strip().strip("\n") == outputs[i].strip().strip("\n")