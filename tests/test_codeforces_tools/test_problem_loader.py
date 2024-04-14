from fastsnake.util.codeforces import get_contest_problem
import os


def test_load_problem_test_cases():
    folder = os.path.join(os.path.dirname(__file__), "sample_1949_J")

    n_input = len([x for x in os.listdir(folder) if x.endswith(".in")])
    n_output = len([x for x in os.listdir(folder) if x.endswith(".out")])

    inputs, outputs = get_contest_problem(1949, "J")

    assert len(inputs) == n_input and len(outputs) == n_output

    for i in range(n_input):
        with open(os.path.join(folder, f"{i}.in")) as file:
            assert file.read().strip().strip("\n") == inputs[i].strip().strip("\n")

    for i in range(n_output):
        with open(os.path.join(folder, f"{i}.out")) as file:
            assert file.read().strip().strip("\n") == outputs[i].strip().strip("\n")