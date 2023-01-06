import numpy as np
from scipy.interpolate import interpn, interp1d, PchipInterpolator

def ensure_monotonically_increasing(x):
    return np.all(np.diff(x) > 0)

def interp1(x, y, **ipkwargs):
    """
    Wrapper function for the 1d interpolation
    at end of lookup mode 3.

    Python does not support pchip as a 1d interpolation method.
    Have to use a wrapper function to access both

    Args:
        filename
    """

    METHOD = ipkwargs.pop('METHOD')
    if METHOD == 'pchip':
        if not ensure_monotonically_increasing(x):
            # reverse arrays for interpolator
            return PchipInterpolator(x[::-1], y[::-1])
        else:
            return PchipInterpolator(x, y)
    else:
        return interp1d(x, y, **ipkwargs)