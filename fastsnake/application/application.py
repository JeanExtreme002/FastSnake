from fastsnake.application.arg_parser import main_parser
from fastsnake.application.external import add_external_module, delete_external_module
from fastsnake.application.contest import start_contest
from fastsnake.application.runner import compile, run_test, run_test_generator
from fastsnake.util import atcoder
from fastsnake.util import codeforces

from typing import List

import fastsnake
import os


project_path = os.path.join(os.path.dirname(__file__), "..")
args = main_parser.parse_args()


def load_atcoder_problem(contest_id: str, problem: str, directory: str, namespace: str) -> None:
    """
    Download test cases from AtCoder of a problem.
    """
    inputs, outputs = atcoder.get_problem_test_cases(contest_id, problem, namespace)

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


def load_atcoder_problems(contest_id: str, directory: str, namespace: str) -> List[str]:
    """
    Download test cases from every problem of AtCoder contest.
    """
    problems = atcoder.get_problems(contest_id, namespace)

    for problem in problems:
        load_atcoder_problem(contest_id, problem, directory, namespace)

    return problems


def load_codeforces_problem(contest_id: int, problem: str, directory: str, namespace: str) -> None:
    """
    Download test cases from Codeforces of a problem.
    """
    inputs, outputs = codeforces.get_problem_test_cases(contest_id, problem, namespace)

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


def load_codeforces_problems(contest_id: int, directory: str, namespace: str) -> List[str]:
    """
    Download test cases from every problem of Codeforces contest.
    """
    problems = codeforces.get_problems(contest_id, namespace)

    for problem in problems:
        load_codeforces_problem(contest_id, problem, directory, namespace)

    return problems


def start_atcoder_contest(contest_id: str) -> None:
    """
    Initialize a AtCoder contest.
    """
    directory = "atcoder_contest"

    solutions = os.path.join(directory, "solutions")
    test_cases = os.path.join(directory, "test_cases")
    test_generators = os.path.join(directory, "test_generators")

    if not os.path.exists(directory):
        os.mkdir(directory)

    problems = load_atcoder_problems(contest_id, test_cases, namespace="contests")
    start_contest(solutions, test_cases, test_generators, contest_id, problems)


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

    problems = load_codeforces_problems(contest_id, test_cases, namespace="contest")
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
    # Print the information of the project.
    if args.version:
        print(fastsnake.__version__)

    elif args.author:
        print(fastsnake.__author__)

    elif args.credits:
        print(fastsnake.__credits__)

    # List algorithms and structures.
    elif args.list:
        print(f"[{args.list.upper()} MODULES]:")

        for name in os.listdir(os.path.join(project_path, args.list)):
            if "__" not in name:
                print(f"- {name.replace('.py', '').replace('_', ' ').title()}")

    # CLI Commands.
    elif args.command:

        # Test the solution.
        if args.command == "test":
            if args.generator:
                run_test_generator(
                    args.problem, 
                    args.generator, 
                    args.step_counter, 
                    compile_before=args.compile_before,
                    compile_after=args.test_and_compile,
                    case_insensitive=args.case_insensitive,
                    debug=args.debug
                )
            else:
                run_test(
                    args.problem, 
                    args.step_counter, 
                    compile_before=args.compile_before,
                    compile_after=args.test_and_compile,
                    case_insensitive=args.case_insensitive,
                    debug=args.debug
                )
        
        # Compile a fastsnake solution.
        elif args.command == "compile":
            compile(args.filename)

        # Start a custom contest.
        elif args.command == "start-custom-contest":
            start_custom_contest(args.n_problems)

        # Add a external module.
        elif args.command == "add-external":
            add_external_module(args.filename, args.name, bool(args.url))

        # Delete a external module.
        elif args.command == "delete-external":
            delete_external_module(args.module)

        # Tools for AtCoder.
        elif args.command == "atcoder":
            if args.load:
                contest_id, problem = args.load[0], args.load[1]
                load_atcoder_problem(contest_id, problem, args.save, namespace="contests")

            elif args.load_all:
                load_atcoder_problems(args.load_all, args.save, namespace="contests")

            elif args.start_contest:
                start_atcoder_contest(args.start_contest)

        # Tools for Codeforces.
        elif args.command == "codeforces":
            if args.load:
                try: 
                    contest_id, problem = int(args.load[0]), args.load[1]
                except: 
                    contest_id, problem = int(args.load[1]), args.load[0]

                load_codeforces_problem(contest_id, problem, args.save, namespace="contest")

            elif args.load_all:
                load_codeforces_problems(args.load_all, args.save, namespace="contest")

            elif args.start_contest:
                start_codeforces_contest(args.start_contest)

            elif args.start_gym:
                start_codeforces_gym(args.start_gym)
                

if __name__ == "__main__":
    main()