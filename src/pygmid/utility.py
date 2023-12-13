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
    plot = kwargs.get('plot', False)

    if mode == 1:
        L   =   kwargs.get('L', min(lk['L']))
        VDS =   kwargs.get('VDS', lk['VDS'])
        VSB =   kwargs.get('VSB', 0.0)
        rho =   kwargs.get('rho', 0.6)
        UDS =   kwargs.get('UDS', np.arange(0.025, 1.2+0.025, 0.025))

        UT  =  ( 0.0259 * lk['TEMP']/300 ).item()

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
        n  = interp1(UDS, nn, kind='pchip')(VDS) 
        VT = interp1(UDS, Vth, kind='pchip')(VDS)
        JS = interp1(UDS, Js, kind='pchip')(VDS)

        d1n = interp1(UDS1, diff1n, kind='pchip')(VDS)
        d2n = interp1(UDS2, diff2n, kind='pchip')(VDS)

        d1VT = interp1(UDS1, diff1Vth, kind='pchip')(VDS)
        d2VT = interp1(UDS2, diff2Vth, kind='pchip')(VDS)

        d1logJS = interp1(UDS1, diff1logJs, kind='pchip')(VDS)
        d2logJS = interp1(UDS2, diff2logJs, kind='pchip')(VDS)

        if plot:
            #% FIGURE =============
            # setup mpl
            import matplotlib as mpl
            import matplotlib.pyplot as plt
            mpl.rcParams['axes.spines.right'] = False
            mpl.rcParams['axes.spines.top'] = False
            mpl.rcParams.update({"axes.grid" : True})
            
            plt.figure(1); plt.plot(UDS, nn, VDS, n, '*')
            #plt.ylabel(r"$n$"); plt.xlabel(r"$V_{DS}$ [V]")
            plt.figure(2); plt.plot(UDS1, diff1Vth, VDS, d1VT, '*')
            #plt.ylabel(r"$n$"); plt.xlabel(r"$V_{DS}$ [V]")
            plt.figure(3); plt.plot(UDS2, diff2Vth, VDS, d2VT, '*')
            #plt.ylabel(r"$n$"); plt.xlabel(r"$V_{DS}$ [V]")
            plt.show()
            print("Press enter to continue...")
            input()

            plt.figure(1); plt.plot(UDS, nn, VDS, n, '*')
            #plt.ylabel(r"$n$"); plt.xlabel(r"$V_{DS}$ [V]")
            plt.figure(2); plt.plot(UDS1, diff1n, VDS, d1n, '*')
            #plt.ylabel(r"$n$"); plt.xlabel(r"$V_{DS}$ [V]")
            plt.figure(3); plt.plot(UDS2, diff2n, VDS, d2n, '*')
            #plt.ylabel(r"$n$"); plt.xlabel(r"$V_{DS}$ [V]")
            plt.show()
            print("Press enter to continue...")
            input()

            plt.figure(1); plt.plot(UDS, Js, VDS, JS, '*')
            #plt.ylabel(r"$n$"); plt.xlabel(r"$V_{DS}$ [V]")
            plt.figure(2); plt.plot(UDS1, diff1logJs, VDS, d1logJS, '*')
            #plt.ylabel(r"$n$"); plt.xlabel(r"$V_{DS}$ [V]")
            plt.figure(3); plt.plot(UDS2, diff2logJs, VDS, d2logJS, '*')
            #plt.ylabel(r"$n$"); plt.xlabel(r"$V_{DS}$ [V]")
            plt.show()
            print("Press enter to continue...")
            input()

        return (VDS, n, VT, JS, d1n, d1VT, d1logJS, d2n, d2VT, d2logJS) 
    elif mode ==2:
        print("Mode 2 not implemented")
        return
        #VGS =   kwargs.get('VGS', lk['VGS'])
        #ID =   kwargs.get('ID', lk['ID'])
        #rho =   kwargs.get('rho', 0.6)

        #qFo = 1/rho - 1
        #i = qFo * qFo + qFo

        #UT = .026
        #ID = np.atleast_2d(ID)
        #m1, m2 = ID.shape
        #gm_Id = np.diff(np.log(ID))/np.diff(VGS[])
        #z1, b = max(gm_Id)

        # compute VGSo and IDo -------
        #UGS     = .5*(VGS(1:m1-1) + VGS(2:m1));
        #for k = 1:m2,
        #    VGSo(k,1) = interp1(gm_Id(:,k),UGS,z1(k)*rho,'cubic');
        #    IDo(k,1)  = interp1(VGS,ID(:,k),VGSo(k,1),'cubic');
        #end

        #n  = 1./(UT*z1');
        #VT  = VGSo - UT*n.*(2*(qFo-1)+log(qFo));
        #IS = IDo/i;

        #return n, VT, IS 
    else:
        print("Invalid mode")
        return