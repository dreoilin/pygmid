import numpy as np
import ast
import configparser
import logging
from psf_utils import PSF
import subprocess
import sys
import shutil
import os
from subprocess import CalledProcessError
import pickle

import os
import glob
import re
import json

from .sweep import Sweep

def matrange(start, step, stop):
    num = round((stop - start) / step + 1)
    
    return np.linspace(start, stop, num)

if __name__ == '__main__':
    configfile = str(sys.argv[1])
    swp = Sweep(configfile)
    swp.run()
