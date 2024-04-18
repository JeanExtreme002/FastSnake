from fastsnake.application.arg_parser import main_parser
from fastsnake.application.config import contest_config_filename
from fastsnake.application.contest import start_contest
from fastsnake.application.runner import run_test, run_test_generator
from fastsnake.util.codeforces import *
from fastsnake.util.compiler import compile_code

import fastsnake
import json
import os


project_path = os.path.join(os.path.dirname(__file__), "..")
args = main_parser.parse_args()


def compile(filename: str, problem: bool = False) -> None:
    """
    Compile a solution.
    """        
    # If the provided filename does not contains PY extension, check if it is a contest problem.
    if not filename.endswith(".py") and problem:
        with open(contest_config_filename) as file:
            config = json.load(file)
                
        filename = os.path.join(config["solutions_namespace"], filename + ".py")

    # Get the output filename and compile the solution.
    base_name = os.path.basename(filename)
    directory = os.path.dirname(filename)

    output_filename = os.path.join(directory, "compiled_" + base_name)
    
    compile_code(filename, output_filename)


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
    directory = "codeforces_contest"

    solutions = os.path.join(directory, "solutions")
    test_cases = os.path.join(directory, "test_cases")
    test_generators = os.path.join(directory, "test_generators")

    if not os.path.exists(directory):
        os.mkdir(directory)

    problems = load_codeforces_problems(contest_id, test_cases)
    start_contest(solutions, test_cases, test_generators, contest_id, problems)


def start_codeforces_gym(gym_id: int) -> None:
    """
    Initialize a Codeforces contest.
    """
    directory = "codeforces_gym"

    solutions = os.path.join(directory, "solutions")
    test_cases = os.path.join(directory, "test_cases")
    test_generators = os.path.join(directory, "test_generators")

    if not os.path.exists(directory):
        os.mkdir(directory)

    problems = load_codeforces_problems(gym_id, test_cases, namespace="gym")
    start_contest(solutions, test_cases, test_generators, gym_id, problems)


def start_custom_contest(n_problems: int) -> None:
    """
    Initialize a custom contest.
    """
    directory = "custom_contest"
    contest_id = "x"

    solutions = os.path.join(directory, "solutions")
    test_cases = os.path.join(directory, "test_cases")
    test_generators = os.path.join(directory, "test_generators")

    if not os.path.exists(directory):
        os.mkdir(directory)

    if not os.path.exists(test_cases):
        os.mkdir(test_cases)

    problems = [chr(ord("A")+i) for i in range(min(n_problems, 26))]

    for problem in problems:
        filename = f"contest_{contest_id}_problem_{problem}_0.in"
        filename = os.path.join(test_cases, filename)

        with open(filename, "w") as file:
            file.write("\n")

        filename = f"contest_{contest_id}_problem_{problem}_0.out"
        filename = os.path.join(test_cases, filename)

        with open(filename, "w") as file:
            file.write("\n")

    start_contest(solutions, test_cases, test_generators, contest_id, problems)


def main() -> None:
    """
    Main function.
    """
    # Print the version of the project.
    if args.version:
        print(fastsnake.__version__)

    # List algorithms and structures.
    elif args.list:
        for name in os.listdir(os.path.join(project_path, args.list)):
            if "__" not in name:
                print(f"- {name.replace('.py', '').replace('_', ' ').title()}")

    # CLI Commands.
    elif args.command:

        # Test the solution.
        if args.command == "test":
            if args.generator:
                result = run_test_generator(args.problem, args.generator)
            else:
                result = run_test(args.problem)

            if result and args.test_and_compile: 
                compile(args.problem, problem=True)
        
        # Compile a fastsnake solution.
        elif args.command == "compile":
            compile(args.filename)

        # Start a custom contest.
        elif args.command == "start-custom-contest":
            start_custom_contest(args.n_problems)


        # Tools for Codeforces.
        elif args.command == "codeforces":
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