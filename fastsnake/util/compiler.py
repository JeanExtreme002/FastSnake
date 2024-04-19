import os


path = os.path.join(os.path.dirname(__file__), "..")


def compile_code(input_filename: str, output_filename: str) -> None:
    
    string = ""

    valid_imports = [
        "from fastsnake.algorithms",
        "from fastsnake.structures",
        "from fastsnake.external",
        "from fastsnake.entries"
    ]
    
    with open(input_filename) as file:
        for line in file:
            # Check if the line contains an import statement for algorithms or structures.
            if not any([line.startswith(x) for x in valid_imports]):
                string += line
                continue

            # Clean the line and get the module name.
            line = line.replace("\n", "").replace(" ", "")
            importing = line.replace("from", "", 1).replace("import*", "").replace("import", ".", 1).split(".")[1:]
            
            # Get the absolute path to the module name.
            filename = os.path.join(path, *importing[:-1], importing[-1] + ".py")
            
            # Inject the code of the module.
            with open(filename) as module:
                string += module.read()
            string += "\n"

    # Write the compiled code.
    with open(output_filename, "w") as file:
        file.write(string)
