import sys

from .sweep import Sweep

def run(config_file_path: str) -> (str, str):
    swp = Sweep(config_file_path)
    return swp.run()

if __name__ == '__main__':
    run(str(sys.argv[1]))