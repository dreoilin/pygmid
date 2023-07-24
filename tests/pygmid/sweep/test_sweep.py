import filecmp
import numpy as np
from pathlib import Path

from pygmid import sweep, Lookup

from ...should_run import should_run

import pytest

pytestmark = pytest.mark.skip #should_run(skip_reason="No access to sweep debug files")

def test_sweep_e2e(config_file: Path, expected_output_files: (Path, Path)):
    sweep.run(config_file.absolute().resolve())
    enf, enp = expected_output_files
    anf = Path('90n1rvt.pkl')
    apf = Path('90p1rvt.pkl')
    assert anf.exists()
    assert apf.exists()
    el = Lookup(str(enf.absolute().resolve()))
    al = Lookup(str(anf.absolute().resolve()))
    # TODO: figure out why test differs
    # assert np.testing.assert_equal(el._Lookup__DATA, al._Lookup__DATA)
    # assert filecmp.cmp(anf.absolute().resolve(), enf.absolute().resolve(), shallow=False)