from pathlib import Path


from pygmid import sweep

from ...should_run import should_run

pytestmark = should_run(skip_reason="No access to sweep debug files")

def test_sweep_e2e(config_file: Path):
    sweep.run(config_file.absolute().resolve())