from fastsnake.application.arg_parser import main_parser
from fastsnake.application.config import contest_config_filename
from fastsnake.application.contest import start_contest
from fastsnake.application.test_runner import run_test
from fastsnake.util.codeforces import *
from fastsnake.util.compiler import compile_code

import fastsnake
import json
import os


project_path = os.path.join(os.path.dirname(__file__), "..")
args = main_parser.parse_args()


def compile(args) -> None:
    """
    Compile a solution.
    """
    if args.test_and_compile:
        args.compile = args.test_and_compile
        
    # If the provided filename does not contains PY extension, check if it is a contest problem.
    if not args.compile.endswith(".py"):
        if args.test or os.path.exists(contest_config_filename):
            with open(contest_config_filename) as file:
                config = json.load(file)
                
            if args.compile:
                args.compile = os.path.join(config["solutions_namespace"], args.compile + ".py")

            elif args.test:
                args.compile = os.path.join(config["solutions_namespace"], args.test + ".py")

    # Get the output filename and compile the solution.
    base_name = os.path.basename(args.compile)
    directory = os.path.dirname(args.compile)

    output_filename = os.path.join(directory, "compiled_" + base_name)
    
    compile_code(args.compile, output_filename)


def load_codeforces_problem(contest_id: int, problem: str, directory: str, namespace: str = "contest") -> None:
    """
    Download test cases from Codeforces of a problem.
    """
    inputs, outputs = get_problem_test_cases(contest_id, problem, namespace)

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


def load_codeforces_problems(contest_id: int, directory: str, namespace: str = "contest") -> List[str]:
    """
    Download test cases from every problem of Codeforces contest.
    """
    problems = get_problems(contest_id, namespace)

    for problem in problems:
        load_codeforces_problem(contest_id, problem, directory, namespace)

    return problems


def start_codeforces_contest(contest_id: int) -> None:
    """
    Initialize a Codeforces contest.
    """
    directory = "codeforces"

    test_cases = directory + "_contest_test_cases"
    solutions = directory + "_contest_solutions"

    problems = load_codeforces_problems(contest_id, test_cases)
    start_contest(test_cases, solutions, contest_id, problems)


def start_codeforces_gym(gym_id: int) -> None:
    """
    Initialize a Codeforces contest.
    """
    directory = "codeforces"

    test_cases = directory + "_gym_test_cases"
    solutions = directory + "_gym_solutions" 

    problems = load_codeforces_problems(gym_id, test_cases, "gym")
    start_contest(test_cases, solutions, gym_id, problems)


def main() -> None:
    """
    Main function.
    """
    # Compile a fastsnake solution.
    if args.compile:
        compile(args)

    # Print the version of the project.
    elif args.version:
        print(fastsnake.__version__)

    # List algorithms and structures.
    elif args.list:
        for name in os.listdir(os.path.join(project_path, args.list)):
            if "__" not in name:
                print(f"- {name.replace('.py','').replace('_', ' ').title()}")

    # Test the solution.
    elif args.test or args.test_and_compile:
        result = run_test(args.test if args.test else args.test_and_compile)

        if result and args.test_and_compile: 
            compile(args)

    # Tools for Codeforces.
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

            elif args.start_gym:
                start_codeforces_gym(args.start_gym)


if __name__ == "__main__":
    main()