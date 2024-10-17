import os
import sys
import random
import pytest

current_dir = os.getcwd()
sys.path.append(current_dir)


@pytest.fixture(scope="session", autouse=True)
def set_random_seed():
    # define a random seed for the test session
    random_seed = random.randint(0, 1000)
    random.seed(random_seed)
    print(f"Random seed used in this test session: {random_seed}")
