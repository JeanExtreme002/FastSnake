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


def compile(args) -> None:
    """
    Compile a solution.
    """
    if args.test_and_compile:
        args.compile = args.test_and_compile
        
    # If the provided filename does not contains PY extension, check if it is a contest problem.
    if not args.compile.endswith(".py"):
        if args.test or os.path.exists("contest.json"):
            with open("contest.json") as file:
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


def run_test(problem: str) -> bool:
    """
    Run the solution for a problem of the contest.
    """
    with open("contest.json") as file:
        config = json.load(file)

    if not problem in config["problems"]:
        raise ValueError(f"Invalid problem ID: {problem}")

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

        process = subprocess.Popen(
            [command, module.name], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            shell=True,
        )
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
            return False
        
        test_case += 1
        
    print(f"SUCCESS!! Your solution was accepted at all {test_case} test cases.")
    return True


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


def start_contest(test_cases_namespace: str, solutions_namespace: str, contest_id: int, problems: list[str]) -> None:
    """
    Start a contest at the directory.
    """
    config = {
        "test_cases_namespace": test_cases_namespace,
        "solutions_namespace": solutions_namespace,
        "contest_id": contest_id,
        "problems": problems
    }

    # Create folder with Python modules for writting solutions.
    if not os.path.exists(config["solutions_namespace"]):
        os.mkdir(config["solutions_namespace"])

    for filename in os.listdir(config["solutions_namespace"]):
        os.remove(os.path.join(config["solutions_namespace"], filename))

    for problem in config["problems"]:
        with open(os.path.join(config["solutions_namespace"], problem.upper() + ".py"), "w") as file:
            file.write("# Solution for problem " + problem + "\n\n")

    # Create folder with Python modules for writting test case generators.
    if not os.path.exists(config["test_cases_namespace"] + "_generators"):
        os.mkdir(config["test_cases_namespace"] + "_generators")

    for filename in os.listdir(config["test_cases_namespace"] + "_generators"):
        os.remove(os.path.join(config["test_cases_namespace"] + "_generators", filename))

    for problem in config["problems"]:
        with open(os.path.join(config["test_cases_namespace"] + "_generators", "generator_" + problem.upper() + ".py"), "w") as file:
            file.write("# Test case generator for problem " + problem + ". Modify this file.\n\n")
            file.write("import random\n")
            file.write("import string\n\n")
            file.write("def gen_string(size: int, letters: str = string.ascii_lowercase):\n")
            file.write("    return ''.join(random.choice(letters) for _ in range(size))\n")
            file.write("\n")
            file.write("print(random.randint(0, 10**3))\n")
            file.write("print(' '.join([str(random.randint(0, 10**3)) for _ in range(0, random.randint(0, 10**3))]))\n")
            file.write("print(gen_string(random.randint(0, 10**3), string.ascii_uppercase))\n")
            file.write("\n")

    # Create config file.
    with open("contest.json", "w") as file:
        file.write(json.dumps(config))


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
        for name in os.listdir(os.path.join(path, args.list)):
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