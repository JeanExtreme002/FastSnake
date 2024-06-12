from tempfile import _TemporaryFileWrapper
import random
import string

def inject_success_code(temp_module: _TemporaryFileWrapper, language: str = "py"):        
    """
    Inject code to get a specific success code.
    """
    ascii_range = string.ascii_lowercase + string.ascii_uppercase
    success_code = ":success_code" + "".join(random.choice(ascii_range) for _ in range(100)) + ":"

    with open(temp_module.name, mode="a") as file:
        if language == "py": file.write(f"print('{success_code}')\n")
        elif language == "cpp": return ""

    return success_code