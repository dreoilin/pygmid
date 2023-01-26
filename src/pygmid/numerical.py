import numpy as np
from scipy.interpolate import interp1d, PchipInterpolator

def monotonic_interp1(x, y, **ipkwargs):
    # check for maximum monotonic subarray here
    # ...
    # placeholder
    xsub = x
    ysub = y
    # ...

    return interp1(xsub, ysub, **ipkwargs)

def interp1(x, y, **ipkwargs):
    """
    Wrapper function for python 1d interpolation
    Combines the functionality of interp1d and PchipInterpolator.

    Reorders x and y for increasing monotonicity in x

    Args:
        x, y
    Kwargs:
        Interpolation keywords - see interp1d
    """

    METHOD = ipkwargs.get('kind', 'pchip')
    if METHOD == 'pchip':
        # need to convert ipkwargs
        pchipkwargs = {
            'axis'          :   ipkwargs.get('axis', 0),
            'extrapolate'   :   ipkwargs.get('extrapolate', True)
        }
        # enforce increasing monotonicity
        ind = np.argsort(x)
        x = x[ind]
        y = np.take(y, ind, axis=-1)

        return PchipInterpolator(x, y, **pchipkwargs)
    else:
        return interp1d(x, y, **ipkwargs)