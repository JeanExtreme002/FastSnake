from fastsnake.application.config import contest_config_filename

import json
import os

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
    with open(contest_config_filename, "w") as file:
        file.write(json.dumps(config))