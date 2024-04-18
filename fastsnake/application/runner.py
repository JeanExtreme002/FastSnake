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
            shell=False,
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
            with open(input_filename) as file:
                input_data = file.read()

            print(f"Failed at test case #{test_case}!!")
            print("[Input]:")
            print(input_data)
            print("=" * 40)
            print("[Your Output]:")
            print(error if error and not result else result)
            print("=" * 40)
            print("[Expected Output]:")
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
    
    # Import the generator module.
    path = config["test_generators_namespace"]

    if path not in sys.path:
        sys.path.append(path)

    generator = importlib.import_module(f"generator_{problem}")

    # Run the tests.
    for test_id in range(tests):
        input_data = [str(line) for line in generator.generate(test_id)]

        # Create an input file.
        with NamedTemporaryFile("w", delete=False) as input_file:
            input_file.write("\n".join(input_data) + "\n")

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
            shell=False,
        )
        result, error = process.communicate()

        result = result.decode("utf-8").strip().rstrip("\n").replace("\r", "")
        error = error.decode("utf-8")

        try:
            check = generator.test_output(input_data, result)
        except NotImplementedError:
            print("ERROR: You must implement the generator() and test_ouput() at the generator module.")
            return False

        # Check the output.
        if not check:
            print(f"Failed at the generated test case #{test_id}!!")
            print("[Input]:")
            print("\n".join(input_data))
            print("=" * 40)
            print("[Output]:")
            print(result if result and not error else error)
            return False
        
    print(f"SUCCESS!! Your solution was accepted at all {tests} test cases.")
    return True