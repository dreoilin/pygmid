import logging
import subprocess
import os.path

from subprocess import CalledProcessError

class Spectre:
    def __init__(self, *args):
        self.__args = ['spectre', *args]

    def run(self, filename):
        infile = filename
        try:
            cp = subprocess.run(self.__args + [infile], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except CalledProcessError as e:
            logging.info(f"Error executing process\n\n{e}")
            return
        logging.info(cp.stdout)