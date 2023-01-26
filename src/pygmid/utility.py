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
        # get max value from each column
        M = np.amax(gm_ID.T, axis=1)
        nn = 1/(M*UT)
        # find VT(UDS)
        q = 1/rho -1
        i = q**2 + q
        VP = UT * (2 * (q-1) + np.log(q))
        gm_IDref = rho * M
        # have to use linear interpolation here. gm_ID is not monotonic
        VGS = [float(interp1(gm_ID[:,k], lk['VGS'], kind='pchip')(gm_IDref[k])) for k in range(len(UDS))]
        
        Vth = VGS - nn*VP
        #find JS(UDS) ===============
        Js = lk.lookup('ID_W',GM_ID=gm_IDref, VDS=UDS, VSB=VSB, L=L).diagonal()/i 
        import IPython; IPython.embed()
        # DERIVATIVES ===============
        UDS1 = .5*(UDS[:-1] + UDS[1:])
        UDS2 = .5*(UDS1[:-1] + UDS1[1:])
        
        diffUDS = np.diff(UDS)
        diffUDS1 = np.diff(UDS1)

        # subthreshold slope ============
        diff1n = np.diff(nn)/diffUDS
        diff2n = np.diff(diff1n)/diffUDS1

        # threshold voltage =============
        diff1Vth = np.diff(Vth)/diffUDS
        diff2Vth = np.diff(diff1Vth)/diffUDS1

        # log specific current ============
        diff1logJs = np.diff(np.log(Js))/diffUDS
        diff2logJs = np.diff(diff1logJs)/diffUDS1

        # n(VDS), VT(VDS) , JS(VDS) ===========
        #n  = interp1(UDS,nn,VDS,'pchip') 
        #VT = interp1(UDS,Vth,VDS,'pchip')
        #JS = interp1(UDS,Js,VDS,'pchip')

        #d1n = interp1(UDS1,diff1n,VDS,'pchip')
        #d2n = interp1(UDS2,diff2n,VDS,'pchip')

        #d1VT = interp1(UDS1,diff1Vth,VDS,'pchip')
        #d2VT = interp1(UDS2,diff2Vth,VDS,'pchip')

        #d1logJS = interp1(UDS1,diff1logJs,VDS,'pchip')
        #d2logJS = interp1(UDS2,diff2logJs,VDS,'pchip')

        # OUTPUT ========
        return (VDS, n, VT, JS, d1n, d1VT, d1logJS, d2n, d2VT, d2logJS) 

        #% FIGURE =============
        #figure(1); plot(UDS,nn,VDS,n,'*'); grid
        #figure(2); plot(UDS1,diff1VT,VDS,d1VT,'*'); grid
        #figure(3); plot(UDS2,diff2VT,VDS,d2VT,'*'); grid; pause#

        #figure(1); plot(UDS,nn,VDS,n,'*'); grid
        #figure(2); plot(UDS1,diff1n,VDS,d1n,'*'); grid
        #figure(3); plot(UDS2,diff2n,VDS,d2n,'*'); grid; pause

        #figure(1); plot(UDS,Js,VDS,JS,'*'); grid
        #figure(2); plot(UDS1,diff1logJs,VDS,d1logJS,'*'); grid
        #figure(3); plot(UDS2,diff2logJs,VDS,d2logJS,'*'); grid

        #% y = [VDS n VT JS d1n d1VT d1logJS d2n d2VT d2logJS];
