import os

path = os.path.dirname(__file__)


def compile_code(input_filename, output_filename):
    string = ""
    
    with open(input_filename) as file:
        for line in file:
            if not line.startswith("from fastsnake"):
                string += line
                continue

            line = line.replace("\n", "").replace(" ", "")
            importing = line.replace("from", "").replace("import*", "").split(".")[1:]
            
            filename = os.path.join(path, *importing[:-1], importing[-1] + ".py")

            if filename == __file__:
                string += "\n"
                continue
            
            with open(filename) as module:
                string += module.read()
            string += "\n"

    with open(output_filename, "w") as file:
        file.write(string)
