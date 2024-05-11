from fastsnake.application.runner import run_test, run_test_generator

import os


os.chdir(os.path.join(os.getcwd(), "tests", "test_application"))


def test_runner():
    for problem in "ABCD":
        assert run_test(problem, case_insensitive=True)
        assert run_test_generator(problem, case_insensitive=True)

    assert not run_test("E", case_insensitive=True)
    assert not run_test_generator("E", case_insensitive=True)