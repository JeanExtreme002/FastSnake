from fastsnake.util.compiler import compile_code
from tempfile import NamedTemporaryFile

import os
import sys


def test_compiler():
    file = NamedTemporaryFile("w", delete = False)
    file.close()

    base_dir = os.path.join(os.path.dirname(__file__), "..", "..")

    filename = os.path.join(os.path.dirname(__file__), "sample.py")
    compile_code(filename, file.name)

    command = "python" if "win" in sys.platform else "python3"

    assert os.system(f"{command} {filename} {base_dir}") == 1
    assert os.system(f"{command} {file.name} {base_dir}") == 0

