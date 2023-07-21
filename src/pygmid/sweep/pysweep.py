import sys

from .sweep import Sweep

if __name__ == '__main__':
    configfile = str(sys.argv[1])
    swp = Sweep(configfile)
    swp.run()
