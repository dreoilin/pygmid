import subprocess
import logging
class SpectreSimulator:
    def __init__(self, *args):
        self.__args = args
    
    def run(self, filename: str):
        infile = filename
        try:
            cmd_args = ['spectre', filename] + [*self.__args]
            cp = subprocess.run(cmd_args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            logging.info(f"Error executing process\n\n{e}")
            return
        logging.info(cp.stdout)