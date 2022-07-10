import numpy as np
from .Spectre import Spectre

class Sweep:
    def __init__(self):
        # may need args here for command to run
        self.__simulator = Spectre()

    def run(self, **kwargs):
        pass