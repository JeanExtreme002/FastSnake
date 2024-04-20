from fastsnake.application.config import contest_config_filename
from fastsnake.util.step_counter import inject_step_counter

from tempfile import NamedTemporaryFile
import importlib
import json
import os
import random
import sys
import subprocess
import string


def run_test(problem: str, step_counter: bool = False, debug: bool = False) -> bool:
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

        # Inject the step counter to the code, if required.
        step_counter_variable = None

        if step_counter:
            step_counter_variable = inject_step_counter(module.name, module.name)

        # Inject code to get a specific success code.
        ascii_range = string.ascii_lowercase + string.ascii_uppercase
        success_code = ":success_code" + "".join(random.choice(ascii_range) for _ in range(100)) + ":"

        with open(module.name, mode="a") as file:
            file.write(f"print('{success_code}')\n")

        # Print the name of the module that will be executed, if debug is True.
        if debug: print(f"[DEBUG] Temp Module Path of Test #{test_case}:", module.name)

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

        # Check if there is any error.
        success = False

        if result.endswith(success_code):
            result = result.replace(success_code, "").rstrip("\n")
            success = True

        # Get the result of the step counter.
        step_counter_result = -1

        if success and step_counter and result.endswith(step_counter_variable):
            result, sc_result = result.split(f"{step_counter_variable}:")
            step_counter_result = int(sc_result.replace(f":{step_counter_variable}", ""))

        # Load the expected output.
        output_filename = os.path.abspath(os.path.join(config["test_cases_namespace"], filename[:-2] + "out"))

        with open(output_filename) as file:
            output = file.read().strip().replace("\r", "").rstrip("\n")

        # Compare the outputs.
        if output != result or not success:
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
    if step_counter: print(f"Approximate number of steps executed: {step_counter_result}")
    
    return True


def run_test_generator(problem: str, tests: int = 1, step_counter: bool = False, debug: bool = False) -> bool:
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

        # Inject the step counter to the code, if required.
        step_counter_variable = None

        if step_counter:
            step_counter_variable = inject_step_counter(module.name, module.name)

        # Inject code to get a specific success code.
        ascii_range = string.ascii_lowercase + string.ascii_uppercase
        success_code = ":success_code" + "".join(random.choice(ascii_range) for _ in range(100)) + ":"

        with open(module.name, mode="a") as file:
            file.write(f"print('{success_code}')\n")

        # Print the name of the module that will be executed, if debug is True.
        if debug: print(f"[DEBUG] Temp Module Path of Test #{test_id}:", module.name)

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

        # Check if there is any error.
        success = False

        if result.endswith(success_code):
            result = result.replace(success_code, "").rstrip("\n")
            success = True

        # Get the result of the step counter.
        step_counter_result = -1

        if success and step_counter and result.endswith(step_counter_variable):
            result, sc_result = result.split(f"{step_counter_variable}:")
            step_counter_result = int(sc_result.replace(f":{step_counter_variable}", ""))

        # Check the output.
        try:
            check = generator.test_output(input_data, result)
        except NotImplementedError:
            print("ERROR: You must implement the generator() and test_ouput() at the generator module.")
            return False

        if not check or not success:
            print(f"Failed at the generated test #{test_id}!!")
            print("[Input]:")
            print("\n".join(input_data))
            print("=" * 40)
            print("[Output]:")
            print(result if result and not error else error)
            return False
        
        if step_counter: print(f"Approximate number of steps executed for test #{test_id}: {step_counter_result}")
        
    print(f"SUCCESS!! Your solution was accepted at all {tests} generated tests.")
    return True