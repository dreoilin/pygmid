import numpy as np
from scipy.interpolate import interpn, interp1d, PchipInterpolator

def monotonically_increasing(x):
    return np.all(np.diff(x) > 0)

def interp1(x, y, **ipkwargs):
    """
    Wrapper function for python 1d interpolation
    Combines the functionality of interp1d and PchipInterpolator.

    Checks x for increasing monotonicity. If false, both x and y are reversed

    Args:
        x, y
    Kwargs:
        Interpolation keywords - see interp1d
    """

    METHOD = ipkwargs.get('kind', 'pchip')
    if METHOD == 'pchip':
        if not monotonically_increasing(x):
            # reverse arrays for interpolator
            return PchipInterpolator(x[::-1], y[::-1])
        else:
            return PchipInterpolator(x, y)
    else:
        return interp1d(x, y, **ipkwargs)