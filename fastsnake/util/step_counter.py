import random
import string


def get_indent(line: str, plus: int = 0):   
    c = 0

    for char in line:
        if char in " ":
            c += 1
        else:
            break

    return " " * c + (" " * 4 * plus)


def inject_step_counter(input_filename: str, output_filename: str) -> str:
    """
    Inject a variable for counting the number of steps of a python code running.
    """
    code_lines = list()

    # Read the Python code.
    with open(input_filename) as file:
        for line in file:
            code_lines.append(line)

    # Create counter variable.
    variable = "step_counter_" + "".join(random.choice(string.ascii_lowercase) for _ in range(50))

    # Inject a counter to the code.
    with open(output_filename, "w") as file:
        file.write(f"{variable} = 0\n")

        wait_for_method = False
        wait_for_closing = False
        wait_for_closing_from_def = False
        wait_for_closing_indent_level = 0

        for line in code_lines:
            cleaned_line = line.replace("\r", "").replace("\t", "").strip().replace("\n", "")

            if not line.endswith("\n"):
                line += "\n"

            line = line.replace("\t", " " * 4)

            # Set the start of the counter if a special annotation was found.
            if "#" in cleaned_line and cleaned_line.replace("#", "").strip().lower().startswith("[start step counter]"):
                file.write(get_indent(line) + f"{variable} = 0\n")
                continue

            # Count statements for flow control, inserting the counting before the line.
            if cleaned_line.startswith("return") or cleaned_line.startswith("continue") or cleaned_line.startswith("break"):
                file.write(get_indent(line) + f"{variable} += 1\n")
                file.write(line)
                continue
            
            # Count first checking of condicionals, for and while loops.
            if cleaned_line.startswith("if ") or cleaned_line.startswith("while ") or cleaned_line.startswith("for "):
                file.write(get_indent(line) + f"{variable} += 1\n")
            
                # Count the code that is in-line.
                if cleaned_line.split(":")[-1]:
                    parts = line.split(":")

                    part_1 = ":".join(parts[:-1])
                    part_2 = parts[-1]

                    if "lambda" not in parts[-2]:
                        indent = get_indent(line, 1)

                        file.write(part_1 + ":\n")
                        file.write(indent + f"{variable} += 1\n")
                        file.write(indent + part_2.strip() + "\n")
                        continue
                    
            # Write the original line.
            file.write(line)

            # Remove whitespaces from the line for a better approach.
            original_cleaned_line = cleaned_line
            cleaned_line = cleaned_line.replace(" ", "")

            # Ignore blanck lines or lines which does not start with a letter or closing.
            if not cleaned_line or cleaned_line[0] not in (string.ascii_uppercase + string.ascii_lowercase + ")]}"):
                continue

            # Ignore if it's constructing a structure or invoking something.
            if cleaned_line[-1] in "([{,":
                if wait_for_closing:
                    continue

                wait_for_closing = True
                wait_for_closing_indent_level = len(get_indent(line))
                wait_for_closing_from_def = original_cleaned_line.startswith("def ")
                continue
            
            # Check if the previous construction got to an end.
            if cleaned_line[-1] in ")]}" or (wait_for_closing and cleaned_line[-1] == ":"):
                if len(get_indent(line)) == wait_for_closing_indent_level:

                    if wait_for_closing and wait_for_closing_from_def:
                        file.write(get_indent(line, int(cleaned_line.endswith(":"))) + f"global {variable}\n")

                    wait_for_closing = False
                    wait_for_closing_from_def = False
            
            # Ignore if the previous line did not have an end.
            if wait_for_closing:
                continue
            
            # Ignore class statement and ignore the next lines, until find a method.
            if cleaned_line.startswith("def"):
                file.write(get_indent(line, int(cleaned_line.endswith(":"))) + f"global {variable}\n")
                wait_for_method = False

            if wait_for_method:
                continue

            if cleaned_line.startswith("class"):
                wait_for_method = True
                continue
            
            # Insert the counter after the line.
            file.write(get_indent(line, int(cleaned_line.endswith(":"))) + f"{variable} += 1\n")

        # Prints the number of steps.
        file.write(f"print('{variable}:' + str({variable}) + ':{variable}')\n")

        return variable
