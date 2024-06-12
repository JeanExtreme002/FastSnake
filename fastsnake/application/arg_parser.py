from argparse import ArgumentParser


__all__ = ["main_parser"]


main_parser = ArgumentParser(prog="FastSnake", description="CLI Tools for Competitive Programming")

main_parser.add_argument("-l", "--list", type=str, choices=["algorithms", "structures", "external"], help="List algorithm, structure or external modules")
main_parser.add_argument("-v", "--version", action="store_true", help="Print the fastsnake's version")
main_parser.add_argument("--author", action="store_true", help="Print the author name")
main_parser.add_argument("--credits", action="store_true", help="Print the credits of the project")
main_parser.add_argument("-tp", "--template-path", dest="template_path", action="store_true", help="Return the path to the location where the templates are stored")

command_parser = main_parser.add_subparsers(title="Fastsnake CLI Commands", dest="command")

# Testing Solutions.
test_parser = command_parser.add_parser("test", help="Test a solution for a contest problem")
test_parser.add_argument("problem", type=str, help="Problem of the contest")
test_parser.add_argument("-c", "--compile", action="store_true", dest="test_and_compile", help="Test the solution and compile the solution")
test_parser.add_argument("-cb", "--compile-before", action="store_true", dest="compile_before", help="Compile the solution and test after")
test_parser.add_argument("-g", "--generator", type=int, metavar="n_tests", dest="generator", help="Use generator module to test the solution")
test_parser.add_argument("-s", "--step-counter", action="store_true", dest="step_counter", help="Returns the approximate number of steps executed")
test_parser.add_argument("-s10", "--step-counter-10", action="store_true", dest="step_counter_10", help="Returns the approximate number of steps executed, in power of ten notation")
test_parser.add_argument("-ci", "--case-insensitive", action="store_true", dest="case_insensitive", help="Indicates the output is case insensitive")
test_parser.add_argument("-sl", "--sort-lines", action="store_true", dest="sort_lines", help="Sort lines of the output to compare")
test_parser.add_argument("-se", "--sort-elements", action="store_true", dest="sort_elements", help="Sort elements of every line of the output to compare")
test_parser.add_argument("--return-temp-module-for-debug", action="store_true", dest="debug")

# Compiling Solutions.
compile_parser = command_parser.add_parser("compile", help="Compile a python fastsnake solution")
compile_parser.add_argument("filename", type=str, help="Python module")

# Custom Contest.
custom_contest_parser = command_parser.add_parser("start-custom-contest", help="Start a custom contest")
custom_contest_parser.add_argument("n_problems", type=int, help="Amount of problems")
custom_contest_parser.add_argument("-cpp", "--cpp", action="store_true", dest="language_cpp", help="Use C++ language for solutions")

# Add External Module.
add_external_contest_parser = command_parser.add_parser("add-external", help="Add an external module")
add_external_contest_parser.add_argument("filename", metavar="filename or url", type=str, help="Python module or URL")
add_external_contest_parser.add_argument("-n", "--name", type=str, required=True, dest="name", help="External module name")
add_external_contest_parser.add_argument("-u", "--url", action="store_true", dest="url", help="Indicates to download the code from the URL")

# Delete External Module.
delete_external_contest_parser = command_parser.add_parser("delete-external", help="Delete an external module")
delete_external_contest_parser.add_argument("module", type=str, help="External module name")

# Tools for AtCoder Platforms.
atcoder_parser = command_parser.add_parser("atcoder", help="Tools for Atcoder platform")
atcoder_parser.add_argument("--load-all", metavar="contest_id", type=str, dest="load_all", help="Download test cases from every problem of a contest")
atcoder_parser.add_argument("--load", metavar=("contest_id", "problem"), type=str, nargs=2, dest="load", help="Download test cases from a problem")
atcoder_parser.add_argument("--save", metavar="directory", type=str, default="atcoder", dest="save", help="Directory for saving downloaded files")
atcoder_parser.add_argument("-sc", "--start-contest", metavar="contest_id", type=str, dest="start_contest", help="Initialize a Codeforces contest")
atcoder_parser.add_argument("-cpp", "--cpp", action="store_true", dest="language_cpp", help="Use C++ language for solutions")

# Tools for Contest Platforms.
codeforces_parser = command_parser.add_parser("codeforces", help="Tools for Codeforces platform")
codeforces_parser.add_argument("--load-all", metavar="contest_id", type=int, dest="load_all", help="Download test cases from every problem of a contest")
codeforces_parser.add_argument("--load", metavar=("contest_id", "problem"), type=str, nargs=2, dest="load", help="Download test cases from a problem")
codeforces_parser.add_argument("--save", metavar="directory", type=str, default="codeforces", dest="save", help="Directory for saving downloaded files")
codeforces_parser.add_argument("-sc", "--start-contest", metavar="contest_id", type=int, dest="start_contest", help="Initialize a Codeforces contest")
codeforces_parser.add_argument("-sg", "--start-gym", metavar="gym_id", type=int, dest="start_gym", help="Initialize a Codeforces gym")
codeforces_parser.add_argument("-cpp", "--cpp", action="store_true", dest="language_cpp", help="Use C++ language for solutions")