from fastsnake.application.arg_parser import main_parser
from fastsnake.util.codeforces import *
from fastsnake.util.compiler import compile_code

import fastsnake
import sys

import os


path = os.path.join(os.path.dirname(__file__), "..")
args = main_parser.parse_args()


def load_codeforces_problem(contest_id, problem, directory):
    """
    Download test cases from Codeforces of a problem.
    """
    inputs, outputs = get_contest_problem_test_cases(contest_id, problem)

    if directory != "." and not os.path.exists(directory):
        os.mkdir(directory)

    for id_ in range(len(inputs)):
        filename = f"contest_{contest_id}_problem_{problem}_{id_}.in"
        filename = os.path.join(directory, filename)

        with open(filename, "w") as file:
            file.write(inputs[id_].strip().strip("\n"))

    for id_ in range(len(outputs)):
        filename = f"contest_{contest_id}_problem_{problem}_{id_}.out"
        filename = os.path.join(directory, filename)

        with open(filename, "w") as file:
            file.write(outputs[id_].strip().strip("\n"))


def load_codeforces_problems(contest_id, directory):
    """
    Download test cases from every problem of Codeforces contest.
    """
    for problem in get_contest_problems(contest_id):
        load_codeforces_problem(contest_id, problem, directory)


def main():
    if args.compile:
        compile_code(args.compile, "compiled_" + args.compile)

    elif args.version:
        print(fastsnake.__version__)

    elif args.list:
        for name in os.listdir(os.path.join(path, args.list)):
            if "__" not in name:
                print(f"- {name.replace('.py','').replace('_', ' ').title()}")

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