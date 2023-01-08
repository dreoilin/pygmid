import numpy as np

from .numerical import interp1

def EKV_param_extraction(lk, mode, **kwargs):
    return XTRACT(lk, mode, **kwargs)

def XTRACT(lk, mode, **kwargs):
    """
    EKV param extraction algorithm.

    Two modes of operation:
    1)  L, VSB are scalars. VDS scalar or column vector.
        rho is an optional scalar

    2)
    """

    if mode == 1:
        L   =   kwargs.get('L', min(lk['L']))
        VDS =   kwargs.get('VDS', lk['VDS'])
        VSB =   kwargs.get('VSB', 0.0)
        rho =   kwargs.get('rho', 0.6)
        UDS =   kwargs.get('UDS', np.arange(0.025, 1.2+0.025, 0.025))

        UT  =   0.0259 * np.asscalar(lk['TEMP'])/300

        # find n(UDS)
        gm_ID = lk.look_up('GM_ID', VDS=UDS.T, VSB=VSB, L=L)
        # max function not operating correctly. Array from look_up is correct
        M = gm_ID.max(axis=1)
        nn = 1/(M*UT)

        # find VT(UDS)
        q = 1/rho -1
        i = q**2 + q
        VP = UT * (2 * (q-1) + np.log(q))
        import IPython; IPython.embed()
        gm_IDref = rho * M
        #VGS = [interp1(gm_ID[:,k])]