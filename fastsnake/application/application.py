from fastsnake.application.arg_parser import main_parser
from fastsnake.util.codeforces import *
from fastsnake.util.compiler import compile_code

from tempfile import NamedTemporaryFile

import fastsnake
import json
import os
import subprocess
import sys


path = os.path.join(os.path.dirname(__file__), "..")
args = main_parser.parse_args()


def run_test(problem):
    """
    Run the solution for a problem of the contest.
    """
    with open("contest.json") as file:
        config = json.load(file)

    if not problem in config["problems"]:
        raise ValueError("Invalid problem ID")

    test_case = 0
    
    for filename in os.listdir(config["test_cases_namespace"]):
        
        # Check if the file is an input for the problem.
        if not filename.endswith(".in"): 
            continue 

        if not filename.startswith(f"contest_{config['contest_id']}_problem_{problem}"): 
            continue

        # Get the absolute path for the input file.
        input_filename = os.path.abspath(os.path.join(config["test_cases_namespace"], filename))

        # Copy the module, injecting a code for loading input data.
        inject = f"import sys\nsys.stdin = open(r'{input_filename}', 'r')\n\n"

        module = os.path.join(config["solutions_namespace"], problem.upper() + ".py")

        with open(module) as module:
            code = module.read()

        with NamedTemporaryFile("w", delete=False) as module:
            module.write(inject + code)

        # Run the solution.
        command = "python" if "win32" in sys.platform else "python3"

        process = subprocess.Popen([command, module.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result, error = process.communicate()

        result = result.decode("utf-8").strip().rstrip("\n").replace("\r", "")
        error = error.decode("utf-8")

        # Load the expected output.
        output_filename = os.path.abspath(os.path.join(config["test_cases_namespace"], filename[:-2] + "out"))

        with open(output_filename) as file:
            output = file.read().strip().replace("\r", "").rstrip("\n")

        # Compare the outputs.
        if output != result:
            print(f"Failed at test case #{test_case}!!")
            print("Your Output:")
            print(error if error and not result else result)
            print("Expected Output:")
            print(output)
            return
        
        test_case += 1
        
    print(f"SUCCESS!! Your solution was accepted at all {test_case} test cases.")


def load_codeforces_problem(contest_id, problem, directory):
    """
    Download test cases from Codeforces of a problem.
    """
    inputs, outputs = get_contest_problem_test_cases(contest_id, problem)

    if directory != "." and not os.path.exists(directory):
        os.mkdir(directory)

    for id_ in range(len(inputs)):
        filename = f"contest_{contest_id}_problem_{problem}_{id_}.in"
        filename = os.path.join(directory, filename)

        with open(filename, "w") as file:
            file.write(inputs[id_].strip().strip("\n"))
            file.flush()

    for id_ in range(len(outputs)):
        filename = f"contest_{contest_id}_problem_{problem}_{id_}.out"
        filename = os.path.join(directory, filename)

        with open(filename, "w") as file:
            file.write(outputs[id_].strip().strip("\n"))
            file.flush()


def load_codeforces_problems(contest_id, directory):
    """
    Download test cases from every problem of Codeforces contest.
    """
    problems = get_contest_problems(contest_id)

    for problem in problems:
        load_codeforces_problem(contest_id, problem, directory)

    return problems


def start_contest(test_cases_namespace, solutions_namespace, contest_id, problems: list[str]):
    config = {
        "test_cases_namespace": test_cases_namespace,
        "solutions_namespace": solutions_namespace,
        "contest_id": contest_id,
        "problems": problems
    }

    if not os.path.exists(config["solutions_namespace"]):
        os.mkdir(config["solutions_namespace"])

    for filename in os.listdir(config["solutions_namespace"]):
        os.remove(os.path.join(config["solutions_namespace"], filename))

    for problem in config["problems"]:
        with open(os.path.join(config["solutions_namespace"], problem.upper() + ".py"), "w") as file:
            file.write("# Solution for problem " + problem + "\n\n")

    with open("contest.json", "w") as file:
        file.write(json.dumps(config))


def start_codeforces_contest(contest_id):
    """
    Initialize a Codeforces contest.
    """
    directory = "codeforces"

    test_cases = directory + "_test_cases"
    solutions = directory + "_solutions" 

    problems = load_codeforces_problems(contest_id, directory)
    start_contest(test_cases, solutions, contest_id, problems)


def main():
    if args.compile:
        compile_code(args.compile, "compiled_" + args.compile)

    elif args.version:
        print(fastsnake.__version__)

    elif args.list:
        for name in os.listdir(os.path.join(path, args.list)):
            if "__" not in name:
                print(f"- {name.replace('.py','').replace('_', ' ').title()}")

    elif args.test:
        run_test(args.test)

    elif args.contest:
        if args.contest == "codeforces":
            if args.load:
                try: 
                    contest_id, problem = int(args.load[0]), args.load[1]
                except: 
                    contest_id, problem = int(args.load[1]), args.load[0]

                load_codeforces_problem(contest_id, problem, args.save)

            elif args.load_all:
                load_codeforces_problems(args.load_all, args.save)

            elif args.start_contest:
                start_codeforces_contest(args.start_contest)
