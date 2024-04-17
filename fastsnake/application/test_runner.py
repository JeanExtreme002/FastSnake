from fastsnake.application.config import contest_config_filename

from tempfile import NamedTemporaryFile
import importlib
import json
import os
import sys
import subprocess


def run_test(problem: str) -> bool:
    """
    Run the solution for a problem of the contest.
    """
    with open(contest_config_filename) as file:
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


def run_test_generator(problem: str, tests: int = 1) -> bool:
    """
    Run the solution for a problem of the contest.
    """
    with open(contest_config_filename) as file:
        config = json.load(file)

    if not problem in config["problems"]:
        raise ValueError(f"Invalid problem ID: {problem}")
    
    path = config["test_cases_namespace"] + "_generators"

    if path not in sys.path:
        sys.path.append(path)

    generator = importlib.import_module(f"generator_{problem}")

    for t in range(tests):
        input_data = generator.generate()

        # Create an input file.
        with NamedTemporaryFile(delete=False) as input_file:
            input_file.write(input_data)

        # Get the absolute path for the input file.
        input_filename = os.path.abspath(input_file.name)

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

        # Check the output.
        if not generator.test_output(result):
            print(f"Failed at the generated test case!!")
            print("Input:")
            print(input_data)
            print("Output:")
            print(result)
            return False
        
    print(f"SUCCESS!! Your solution was accepted at all {tests} test cases.")
    return True