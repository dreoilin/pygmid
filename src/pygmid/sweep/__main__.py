import sys

from .sweep import Sweep

def run(config_file_path: str, skip_sweep: bool = False) -> (str, str):
    swp = Sweep(config_file_path)
    if skip_sweep:
        return ('','')
    return swp.run()

if __name__ == '__main__':
    run(str(sys.argv[1]))