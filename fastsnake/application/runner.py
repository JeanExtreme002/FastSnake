from fastsnake.application.config import contest_config_filename
from fastsnake.util.compiler import compile_code
from fastsnake.util.step_counter import inject_step_counter

from tempfile import NamedTemporaryFile

import importlib
import json
import os
import random
import sys
import subprocess
import string


def compile(filename: str) -> None:
    """
    Compile a solution.
    """        
    # Get the output filename and compile the solution.
    base_name = os.path.basename(filename)
    directory = os.path.dirname(filename)

    output_filename = os.path.join(directory, "compiled_" + base_name)
    
    compile_code(filename, output_filename)

    return output_filename


def run_test(
    problem: str, 
    step_counter: bool = False, 
    compile_before: bool = False, 
    compile_after: bool = False, 
    case_insensitive: bool = False,
    debug: bool = False
) -> bool:
    """
    Run the solution for a problem of the contest.
    """
    with open(contest_config_filename) as file:
        config = json.load(file)

    if not problem in config["problems"]:
        raise ValueError(f"Invalid problem ID: {problem}")

    # Get the source code.
    module = os.path.join(config["solutions_namespace"], problem.upper() + ".py")

    if compile_before:
        module = compile(module)

    with open(module) as file:
        source_code = file.read() + "\n"

    # Check the solution for the test cases.
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

        with NamedTemporaryFile("w", delete=False) as temp_module:
            temp_module.write(inject + source_code)

        # Inject the step counter to the code, if required.
        step_counter_variable = None

        if step_counter:
            step_counter_variable = inject_step_counter(temp_module.name, temp_module.name)

        # Inject code to get a specific success code.
        ascii_range = string.ascii_lowercase + string.ascii_uppercase
        success_code = ":success_code" + "".join(random.choice(ascii_range) for _ in range(100)) + ":"

        with open(temp_module.name, mode="a") as file:
            file.write(f"print('{success_code}')\n")

        # Print the name of the module that will be executed, if debug is True.
        if debug: print(f"[DEBUG] Temp Module Path of Test #{test_case}:", temp_module.name)

        # Run the solution.
        command = "python" if "win32" in sys.platform else "python3"

        process = subprocess.Popen(
            [command, temp_module.name], 
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

        result = result.rstrip("\n")

        # Load the expected output.
        output_filename = os.path.abspath(os.path.join(config["test_cases_namespace"], filename[:-2] + "out"))

        with open(output_filename) as file:
            output = file.read().strip().replace("\r", "").rstrip("\n")

        # Compare the outputs.
        if case_insensitive:
            result = result.lower()
            output = output.lower()

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
    
    if compile_after and not compile_before:
        compile(module)

    return True


def run_test_generator(
    problem: str, 
    tests: int = 1, 
    step_counter: bool = False,
    compile_before: bool = False,
    compile_after: bool = False,
    case_insensitive: bool = False,
    debug: bool = False
) -> bool:
    """
    Run the solution for a problem of the contest.
    """
    with open(contest_config_filename) as file:
        config = json.load(file)

    if not problem in config["problems"]:
        raise ValueError(f"Invalid problem ID: {problem}")
    
    # Get the source code.
    module = os.path.join(config["solutions_namespace"], problem.upper() + ".py")

    if compile_before:
        module = compile(module)

    with open(module) as file:
        source_code = file.read() + "\n"

    # Import the generator module.
    path = config["test_generators_namespace"]

    if path not in sys.path:
        sys.path.append(path)

    generator = importlib.import_module(f"generator_{problem}")

    # Run the tests.
    for test_id in range(tests):
        input_data = [str(line) for line in generator.generate(test_id, case_insensitive=case_insensitive)]

        # Create an input file.
        with NamedTemporaryFile("w", delete=False) as input_file:
            input_file.write("\n".join(input_data) + "\n")

        # Get the absolute path for the input file.
        input_filename = os.path.abspath(input_file.name)

        # Copy the module, injecting a code for loading input data.
        inject = f"import sys\nsys.stdin = open(r'{input_filename}', 'r')\n\n"

        with NamedTemporaryFile("w", delete=False) as temp_module:
            temp_module.write(inject + source_code)

        # Inject the step counter to the code, if required.
        step_counter_variable = None

        if step_counter:
            step_counter_variable = inject_step_counter(temp_module.name, temp_module.name)

        # Inject code to get a specific success code.
        ascii_range = string.ascii_lowercase + string.ascii_uppercase
        success_code = ":success_code" + "".join(random.choice(ascii_range) for _ in range(100)) + ":"

        with open(temp_module.name, mode="a") as file:
            file.write(f"print('{success_code}')\n")

        # Print the name of the module that will be executed, if debug is True.
        if debug: print(f"[DEBUG] Temp Module Path of Test #{test_id}:", temp_module.name)

        # Run the solution.
        command = "python" if "win32" in sys.platform else "python3"

        process = subprocess.Popen(
            [command, temp_module.name], 
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

        result = result.rstrip("\n")

        # Check the output.
        if case_insensitive:
            result = result.lower()

        try:
            check = generator.test_output(input_data, result, case_insensitive=case_insensitive)
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

    if compile_after and not compile_before:
        compile(module)

    return True