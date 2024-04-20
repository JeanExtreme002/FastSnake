from fastsnake.util.step_counter import inject_step_counter
from tempfile import NamedTemporaryFile
import os
import subprocess
import sys


def test_get_step_counter():
    filename = os.path.join(os.path.dirname(__file__), "sample.py")

    # Inject the step counter.
    with NamedTemporaryFile("w", delete=False) as file:
        pass

    variable = inject_step_counter(filename, file.name)

    # Run the solution.
    command = "python" if "win32" in sys.platform else "python3"

    process = subprocess.Popen(
        [command, file.name], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        shell=False,
    )
    result, error = process.communicate()

    result = result.decode("utf-8").strip().rstrip("\n").replace("\r", "")
    error = error.decode("utf-8")

    assert 190 <= int(result.replace(":", "").replace(variable, "")) <= 210

    