from .fixtures import *

def pytest_addoption(parser):
    parser.addoption(
            "--preload", action="store", default="yes",
            help="If no load files from .tsv (SLOW). If yes loads from preloaded test.sql. (yes/no)")

@pytest.fixture(scope="session")
def preload(pytestconfig):
    val = pytestconfig.getoption("--preload")
    assert val in ["yes", "no"]
    return val == "yes"

