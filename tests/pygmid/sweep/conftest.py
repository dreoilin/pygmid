import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def expected_output_files():
    n_file = Path('tests/files/90n1rvt.ascii.pkl')
    p_file = Path('tests/files/90p1rvt.ascii.pkl')
    if n_file.exists and p_file.exists:
        return (n_file, p_file)

@pytest.fixture(scope="session")
def config_file():
    return Path('tests/pygmid/sweep/config_IHP130.cfg') 