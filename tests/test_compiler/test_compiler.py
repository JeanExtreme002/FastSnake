from fastsnake.util.compiler import compile_code
from tempfile import NamedTemporaryFile

import os
import sys


def test_compiler():
    file = NamedTemporaryFile("w", delete = False)
    file.close()

    filename = os.path.join(os.path.dirname(__file__), "sample.py")
    compile_code(filename, file.name)

    command = "python" if "win" in sys.platform else "python3"

    assert os.system(f"{command} {filename}") == 1
    assert os.system(f"{command} {file.name}") == 0

