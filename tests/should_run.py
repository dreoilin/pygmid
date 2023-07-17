import pathlib

import pytest


def have_test_files() -> bool:
    return pathlib.Path('tests/files/90n1rvt.ascii.pkl').exists
def should_run(skip_reason: str) :
    return pytest.mark.skipif(not have_test_files(), reason=skip_reason)
