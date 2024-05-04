from fastsnake.application.config import contest_config_filename

import json
import os


template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")


def start_contest(
    solutions_namespace: str,
    test_cases_namespace: str, 
    test_generators_namespace: str, 
    contest_id: int, 
    problems: list[str]
) -> None:
    """
    Start a contest at the directory.
    """
    config = {
        "solutions_namespace": solutions_namespace,
        "test_cases_namespace": test_cases_namespace,
        "test_generators_namespace": test_generators_namespace,
        "contest_id": contest_id,
        "problems": problems
    }

    # Create folder with Python modules for writting solutions.
    if not os.path.exists(config["solutions_namespace"]):
        os.mkdir(config["solutions_namespace"])

    if os.path.exists(config["solutions_namespace"]):
        for filename in os.listdir(config["solutions_namespace"]):
            os.remove(os.path.join(config["solutions_namespace"], filename))

    if os.path.exists(config["test_generators_namespace"]):
        for filename in os.listdir(config["test_generators_namespace"]):
            os.remove(os.path.join(config["test_generators_namespace"], filename))

    for problem in config["problems"]:
        with open(os.path.join(config["solutions_namespace"], problem.upper() + ".py"), "w") as file:
            file.write("# Solution for problem " + problem + "\n\n")

            with open(os.path.join(template_path, "solution.py")) as template_file:
                file.write(template_file.read())

            file.write("\n\n")

    # Create folder with Python modules for writting test case generators.
    if not os.path.exists(config["test_generators_namespace"]):
        os.mkdir(config["test_generators_namespace"])

    for filename in os.listdir(config["test_generators_namespace"]):
        os.remove(os.path.join(config["test_generators_namespace"], filename))

    for problem in config["problems"]:
        with open(os.path.join(config["test_generators_namespace"], "generator_" + problem.upper() + ".py"), "w") as file:
            file.write("# Test case generator for problem " + problem + ". Modify this file.\n\n")
            
            with open(os.path.join(template_path, "test_generator.py")) as template_file:
                file.write(template_file.read())

            file.write("\n")

    # Create config file.
    with open(contest_config_filename, "w") as file:
        file.write(json.dumps(config))

