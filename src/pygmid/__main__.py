import logging
import sys

from .version import __version__
from . import pygmid

def _cli():
    from argparse import ArgumentParser
    description = "CLI for pygmid. Run techsweeps"
    parser = ArgumentParser(description=description)
    parser.add_argument('--version', action='version', version=f"%prog {__version__}")
    parser.add_argument('-c', action='store_const', dest='constant_value',
                        const='value-to-store',
                        help='Store a constant value')

    results = parser.parse_args()
    # assign values from results here
    # val = results.constant_value

    #if opt.backend is not None:
    #    zookeeper.backend = opt.backend
    #if opt.configfile is not None:
    #    zookeeper.configfile = opt.configfile

    #if len(remaining_args) != 0:
    #    print("Usage: python -m zookeeper [settings] \npython -m zookeeper -h for help")
    #    sys.exit(1)
    
    # setup logger    
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    
    pygmid.main()
    sys.exit(0)
        
if __name__ == '__main__':
    # setup logger here
    _cli()
