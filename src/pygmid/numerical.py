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
        try:
            return PchipInterpolator(x, y, **pchipkwargs)
        except ValueError:
            # x is not monotonicallly increasing. Try reversing order
            return PchipInterpolator(x[::-1], y[::-1], **pchipkwargs)
    else:
        return interp1d(x, y, **ipkwargs)