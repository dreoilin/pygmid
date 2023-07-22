import logging
import sys

from .version import __version__
from . import pygmid
from . import sweep

def _cli():
    from argparse import ArgumentParser
    description = "CLI for pygmid. Run techsweeps"
    parser = ArgumentParser(description=description)
    parser.add_argument('--version', action='version', version=f"%prog {__version__}")
    parser.add_argument('--mode', choices=['lookup', 'sweep'], default='lookup')
    parser.add_argument('--config', type=str)

    args = parser.parse_args()
    if args.mode == 'sweep':
        if args.config is None:
            logging.error('Please provide a config file with --config if using the sweep mode')
            sys.exit(-1)
        sweep.run(args.config)
        sys.exit(0)
    elif args.mode == 'lookup':
        pygmid.main()
        sys.exit(0)
    sys.exit(-1)
        
if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    _cli()
