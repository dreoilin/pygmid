import pytest
from pygmid import Lookup


@pytest.fixture(scope="session")
def empty_filename():
    return 'tests/files/empty.mat'
@pytest.fixture(scope="session")
def nch_filename():
    return 'tests/files/180nch.mat'
@pytest.fixture(scope="session")
def pch_filename():
    return 'tests/files/180pch.mat'

@pytest.fixture(scope="session")
def nch(nch_filename):
    return Lookup(filename=nch_filename)
@pytest.fixture(scope="session")
def pch(pch_filename):
    return Lookup(filename=pch_filename)
