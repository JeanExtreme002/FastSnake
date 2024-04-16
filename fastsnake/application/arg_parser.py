from argparse import ArgumentParser

main_parser = ArgumentParser(
    prog="FastSnake",
    description="CLI Tools for Competitive Programming",
)

main_parser.add_argument("-c", "--compile", type=str, metavar="filename", help="Compile a python fastsnake solution")
main_parser.add_argument("-t", "--test", metavar="problem", type=str, help="Test the solution for a problem of the contest")
main_parser.add_argument("-l", "--list", type=str, choices=["algorithms", "structures"], help="List algorithm or structure modules")
main_parser.add_argument("-v", "--version", action="store_true", help="Print the fastsnake's version")

contest_parser = main_parser.add_subparsers(title="Contest Platforms", dest="contest")

codeforces_parser = contest_parser.add_parser("codeforces", help="Tools for Codeforces")
codeforces_parser.add_argument("--load-all", metavar="contest_id", type=int, dest="load_all", help="Download test cases from every problem of a contest")
codeforces_parser.add_argument("--load", metavar=("contest_id", "problem"), type=str, nargs=2, dest="load", help="Download test cases from a problem")
codeforces_parser.add_argument("--save", metavar="directory", type=str, default="codeforces", dest="save", help="Directory for saving downloaded files")
codeforces_parser.add_argument("--start-contest", metavar="contest_id", type=int, dest="start_contest", help="Initialize a Codeforces contest")
