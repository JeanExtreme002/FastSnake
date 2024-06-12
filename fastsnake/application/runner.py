from fastsnake.application import runner_tools
from fastsnake.application.config import contest_config_filename
from fastsnake.util.compiler import compile_code
from fastsnake.util.step_counter import inject_step_counter

from tempfile import NamedTemporaryFile

import importlib
import json
import math
import os
import random
import sys
import subprocess
import string

def check_support_for_cpp(
    step_counter: bool = False, 
    step_counter_10: bool = False, 
    compile_before: bool = False, 
    compile_after: bool = False,
    **kwargs
) -> None:
    """
    Check if there is any runner option that is not supported for C++ solutions.
    """
    if step_counter or step_counter_10:
        print("Step Counter is supported only by the Python language for now.")
        quit()
        
    if compile_before or compile_after:
        print("Compiler is supported only by the Python language for now.")
        quit()     


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


def sort_output_lines(output: str):
    """
    Sort the lines of the output.
    """
    return "\n".join(sorted(output.split("\n")))


def sort_output_elements(output: str):
    """
    Sort the elements of every line of the output.
    """
    new_output = ""

    for line in output.split("\n"):
        new_output += " ".join(sorted(line.split(" "))) + "\n"

    return new_output


def strip_output_lines(output: str):
    """
    Strip every line of the output.
    """
    return "\n".join([line.strip() for line in output.split("\n")])


def run_test(
    problem: str, 
    step_counter: bool = False, 
    step_counter_10: bool = False, 
    compile_before: bool = False, 
    compile_after: bool = False, 
    sort_lines: bool = False, 
    sort_elements: bool = False, 
    case_insensitive: bool = False,
    debug: bool = False
) -> bool:
    """
    Run the solution for a problem of the contest.
    """
    step_counter = step_counter or step_counter_10

    with open(contest_config_filename) as file:
        config = json.load(file)

    if not problem in config["problems"]:
        raise ValueError(f"Invalid problem ID: {problem}")
    
    # Get the language.
    language = config["language"]
    is_python = language == "py"

    if not is_python:
        check_support_for_cpp(
            step_counter=step_counter,
            step_counter_10=step_counter_10,
            compile_after=compile_after,
            compile_before=compile_before,
            sort_lines=sort_lines,
            sort_elements=sort_elements,
            case_insensitive=case_insensitive,
            debug=debug
        )

    # Get the source code.
    module = os.path.join(config["solutions_namespace"], problem.upper() + "." + language)

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

        if not is_python: inject = ""

        with NamedTemporaryFile("w", delete=False) as temp_module:
            temp_module.write(inject + source_code)

        # Inject the step counter to the code, if required.
        step_counter_variable = None

        if step_counter:
            step_counter_variable = inject_step_counter(temp_module.name, temp_module.name)

        # Inject code to get a specific success code.
        success_code = runner_tools.inject_success_code(temp_module, language)

        # Print the name of the module that will be executed, if debug is True.
        if debug: print(f"[DEBUG] Temp Module Path of Test #{test_case}:", temp_module.name + (".cpp" if not is_python else ""))

        # Run the solution.
        if is_python:
            command = "python" if "win32" in sys.platform else "python3"

            process = subprocess.Popen(
                [command, temp_module.name], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                shell=False,
            )
        else:
            dirname = os.path.dirname(temp_module.name)
            program = os.path.join(dirname, "program")

            exec_module = os.path.splitext(temp_module.name)[0] + ".cpp"
            os.rename(temp_module.name, exec_module)

            if os.system(f"g++ -o {program} {exec_module}") != 0:
                print("Erro de compilação.")
                quit()
            
            process = subprocess.Popen(
                [program, input_filename], 
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                shell=False,
            )
            with open(input_filename) as file:
                process.stdin.write(bytearray(file.read(), "utf-8"))
        
        result, error = process.communicate()

        result = result.decode("utf-8").strip().strip("\n").replace("\r", "")
        error = error.decode("utf-8")

        # Check if there is any error.
        success = False

        if result.endswith(success_code):
            result = result.replace(success_code, "").strip("\n")
            success = True

        # Get the result of the step counter.
        step_counter_result = -1

        if success and step_counter and result.endswith(step_counter_variable):
            result, sc_result = result.split(f"{step_counter_variable}:")
            step_counter_result = int(sc_result.replace(f":{step_counter_variable}", ""))

        # Load the expected output.
        output_filename = os.path.abspath(os.path.join(config["test_cases_namespace"], filename[:-2] + "out"))

        with open(output_filename) as file:
            output = file.read().replace("\r", "").strip("\n").strip()

        result = result.strip("\n").strip()

        # Compare the outputs.
        result = strip_output_lines(result)
        output = strip_output_lines(output)

        if case_insensitive:
            result = result.lower()
            output = output.lower()

        if sort_elements:
            result = sort_output_elements(result)
            output = sort_output_elements(output)

        if sort_lines:
            result = sort_output_lines(result)
            output = sort_output_lines(output)

        if output != result or not success:
            with open(input_filename) as file:
                input_data = file.read()

            print(f"Failed at test case #{test_case}!!")
            print("[Input]:")
            print(input_data)
            print("=" * 40)
            print("[Your Output]:")
            print(result)
            if error: print(error)
            print("=" * 40)
            print("[Expected Output]:")
            print(output)
            return False
        
        test_case += 1
        
    print(f"SUCCESS!! Your solution was accepted at all {test_case} test cases.")
    
    if step_counter: 
        if step_counter_10:
            step_counter_result = int(step_counter_result)
            exp = int(math.log(step_counter_result, 10))
            n = int(step_counter_result / (10**exp))
            step_counter_result = f"{n} * 10 ^ {exp}"
        print(f"Approximate number of steps executed: {step_counter_result}")
    
    if compile_after and not compile_before:
        compile(module)

    return True


def run_test_generator(
    problem: str, 
    tests: int = 1, 
    step_counter: bool = False,
    step_counter_10: bool = False,
    compile_before: bool = False,
    compile_after: bool = False,
    sort_lines: bool = False, 
    sort_elements: bool = False, 
    case_insensitive: bool = False,
    debug: bool = False
) -> bool:
    """
    Run the solution for a problem of the contest.
    """
    step_counter = step_counter or step_counter_10

    with open(contest_config_filename) as file:
        config = json.load(file)

    if not problem in config["problems"]:
        raise ValueError(f"Invalid problem ID: {problem}")
    
    # Get the language.
    language = config["language"]
    is_python = language == "py"

    if not is_python:
        check_support_for_cpp(
            step_counter=step_counter,
            step_counter_10=step_counter_10,
            compile_after=compile_after,
            compile_before=compile_before,
            sort_lines=sort_lines,
            sort_elements=sort_elements,
            case_insensitive=case_insensitive,
            debug=debug
        )

    # Get the source code.
    module = os.path.join(config["solutions_namespace"], problem.upper() + "." + language)

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
        input_data = list()
        original_input_data = list()

        for line in generator.generate(test_id):
            if type(line) in [bool, int, float, str]:
                input_data.append(str(line))
            else:
                input_data.append(" ".join([str(element) for element in line]))

            original_input_data.append(line)

        # Create an input file.
        with NamedTemporaryFile("w", delete=False) as input_file:
            input_file.write("\n".join(input_data) + "\n")

        # Get the absolute path for the input file.
        input_filename = os.path.abspath(input_file.name)

        # Copy the module, injecting a code for loading input data.
        inject = f"import sys\nsys.stdin = open(r'{input_filename}', 'r')\n\n"

        if not is_python: inject = ""

        with NamedTemporaryFile("w", delete=False) as temp_module:
            temp_module.write(inject + source_code)

        # Inject the step counter to the code, if required.
        step_counter_variable = None

        if step_counter:
            step_counter_variable = inject_step_counter(temp_module.name, temp_module.name)

        # Inject code to get a specific success code.
        success_code = runner_tools.inject_success_code(temp_module, language)

        # Print the name of the module that will be executed, if debug is True.
        if debug: print(f"[DEBUG] Temp Module Path of Test #{test_id}:", temp_module.name + (".cpp" if not is_python else ""))
        
        # Run the solution.
        if is_python:
            command = "python" if "win32" in sys.platform else "python3"

            process = subprocess.Popen(
                [command, temp_module.name], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                shell=False,
            )
        else:
            dirname = os.path.dirname(temp_module.name)
            program = os.path.join(dirname, "program")

            exec_module = os.path.splitext(temp_module.name)[0] + ".cpp"
            os.rename(temp_module.name, exec_module)

            if os.system(f"g++ -o {program} {exec_module}") != 0:
                print("Erro de compilação.")
                quit()
            
            process = subprocess.Popen(
                [program, input_filename], 
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                shell=False,
            )
            with open(input_filename) as file:
                process.stdin.write(bytearray(file.read(), "utf-8"))
                
        result, error = process.communicate()

        result = result.decode("utf-8").replace("\r", "").strip().strip("\n")
        error = error.decode("utf-8")

        # Check if there is any error.
        success = False

        if result.endswith(success_code):
            result = result.replace(success_code, "").strip("\n")
            success = True

        # Get the result of the step counter.
        step_counter_result = -1

        if success and step_counter and result.endswith(step_counter_variable):
            result, sc_result = result.split(f"{step_counter_variable}:")
            step_counter_result = int(sc_result.replace(f":{step_counter_variable}", ""))

        result = result.strip("\n").strip()

        # Check the output.
        result = strip_output_lines(result)

        if case_insensitive:
            result = result.lower()

        if sort_elements:
            result = sort_output_elements(result)

        if sort_lines:
            result = sort_output_lines(result)

        try:
            check = generator.test_output(original_input_data, result)
        except NotImplementedError:
            print("ERROR: You must implement the generator() and test_ouput() at the generator module.")
            return False

        if not check or not success:
            print(f"Failed at the generated test #{test_id}!!")
            print("[Input]:")
            print("\n".join(input_data))
            print("=" * 40)
            print("[Output]:")
            print(result)
            if error: print(error)
            return False
        
        if step_counter: 
            if step_counter_10:
                step_counter_result = int(step_counter_result)
                exp = int(math.log(step_counter_result, 10))
                n = int(step_counter_result / (10**exp))
                step_counter_result = f"{n} * 10 ^ {exp}"
            print(f"Approximate number of steps executed for test #{test_id}: {step_counter_result}")
        
    print(f"SUCCESS!! Your solution was accepted at all {tests} generated tests.")

    if compile_after and not compile_before:
        compile(module)

    return True