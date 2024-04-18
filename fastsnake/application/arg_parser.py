from argparse import ArgumentParser


main_parser = ArgumentParser(prog="FastSnake", description="CLI Tools for Competitive Programming")

main_parser.add_argument("-l", "--list", type=str, choices=["algorithms", "structures"], help="List algorithm or structure modules")
main_parser.add_argument("-v", "--version", action="store_true", help="Print the fastsnake's version")

command_parser = main_parser.add_subparsers(title="Fastsnake CLI Commands", dest="command")

# Testing Solutions.
test_parser = command_parser.add_parser("test", help="Test a solution for a contest problem")
test_parser.add_argument("problem", type=str, help="Problem of the contest")
test_parser.add_argument("-c", "--compile", action="store_true", dest="test_and_compile", help="Test and compile the solution")
test_parser.add_argument("-g", "--generator", type=int, metavar="n_tests", dest="generator", help="Use generator module to test the solution")

# Compiling Solutions.
compile_parser = command_parser.add_parser("compile", help="Compile a python fastsnake solution")
compile_parser.add_argument("filename", type=str, help="Python module")

# Tools for Contest Platforms.
codeforces_parser = command_parser.add_parser("codeforces", help="Tools for Codeforces platform")
codeforces_parser.add_argument("--load-all", metavar="contest_id", type=int, dest="load_all", help="Download test cases from every problem of a contest")
codeforces_parser.add_argument("--load", metavar=("contest_id", "problem"), type=str, nargs=2, dest="load", help="Download test cases from a problem")
codeforces_parser.add_argument("--save", metavar="directory", type=str, default="codeforces", dest="save", help="Directory for saving downloaded files")
codeforces_parser.add_argument("-sc", "--start-contest", metavar="contest_id", type=int, dest="start_contest", help="Initialize a Codeforces contest")
codeforces_parser.add_argument("-sg", "--start-gym", metavar="gym_id", type=int, dest="start_gym", help="Initialize a Codeforces gym")
