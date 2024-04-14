from fastsnake.util.codeforces import get_contest_problem
from fastsnake.util.compiler import compile_code

import fastsnake
import sys


def load_codeforces_problem(contest_id, problem):
    """
    Download test cases from Codeforces of a problem.
    """
    inputs, outputs = get_contest_problem(contest_id, problem)

    for id_ in range(len(inputs)):
        with open(f"contest_{contest_id}_problem_{problem}_{id_}.in", "w") as file:
            file.write(inputs[id_].strip().strip("\n"))

    for id_ in range(len(outputs)):
        with open(f"contest_{contest_id}_problem_{problem}_{id_}.out", "w") as file:
            file.write(outputs[id_].strip().strip("\n"))
            

def main():
    if sys.argv[1] in ["help", "-h", "--help"]:
        print("- compile [filename.py] : Compile a python solution that uses fastsnake")
        print("- codeforces load | -cl [contest_id] [problem_letter] : Download test cases from codeforces")
        print("- help | --help | -h : Print the CLI commands")
        print("- version | --version | -v : Print the version of fastsnake")

    if sys.argv[1] == "compile":
        compile_code(sys.argv[2], "compiled_" + sys.argv[2])

    elif sys.argv[1] in ["version", "--version", "-v"]:
        print(fastsnake.__version__)

    elif sys.argv[1] == "codeforces" or sys.argv[1].startswith("-c"):
        if sys.argv[1].startswith("-c"):
            sys.argv.insert(2, sys.argv[1][2:])
   
        if sys.argv[2].startswith("l"):
            contest_id, problem = int(sys.argv[-2]), sys.argv[-1]
            load_codeforces_problem(contest_id, problem)
        
if __name__ == "__main__":
    main()
