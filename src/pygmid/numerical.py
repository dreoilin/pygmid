import numpy as np
from scipy.interpolate import interp1d, PchipInterpolator

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
        # need to convert ipkwargs
        pchipkwargs = {
            'axis'          :   ipkwargs.get('axis', 0),
            'extrapolate'   :   ipkwargs.get('extrapolate', True)
        }
        ind = np.argsort(x)
        x = x[ind]
        y = np.take(y, ind, axis=-1)

        # check for increasing monotonicity
        return PchipInterpolator(x, y, **pchipkwargs)
    else:
        return interp1d(x, y, **ipkwargs)