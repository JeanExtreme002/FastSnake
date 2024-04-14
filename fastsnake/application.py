from fastsnake.compiler import compile_code

import sys

def main():
    if sys.argv[1] in ["help", "-h", "--help"]:
        print("- compile filename.py")

    if sys.argv[1] == "compile":
        compile_code(sys.argv[2], "compiled_" + sys.argv[2])
    

if __name__ == "__main__":
    main()
