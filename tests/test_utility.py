#%%
import matplotlib.pyplot as plt
import numpy as np
from pygmid import Lookup as lk
from pygmid import EKV_param_extraction, XTRACT

NCH = lk('180nch.mat')  # load MATLAB data into pygmid lookup object

#%% Test 1
(VDS, n, VT, JS, d1n, d1VT, d1logJS, d2n, d2VT, d2logJS) = EKV_param_extraction(NCH, 1, L = 0.18, VDS = 0.6, VSB = 0.0)
import IPython; IPython.embed()
#figure(1); plot(UDS,nn,VDS,n,'*'); grid
#figure(2); plot(UDS1,diff1VT,VDS,d1VT,'*'); grid
#figure(3); plot(UDS2,diff2VT,VDS,d2VT,'*'); grid; pause#

#figure(1); plot(UDS,nn,VDS,n,'*'); grid
#figure(2); plot(UDS1,diff1n,VDS,d1n,'*'); grid
#figure(3); plot(UDS2,diff2n,VDS,d2n,'*'); grid; pause

#figure(1); plot(UDS,Js,VDS,JS,'*'); grid
#figure(2); plot(UDS1,diff1logJs,VDS,d1logJS,'*'); grid
#figure(3); plot(UDS2,diff2logJs,VDS,d2logJS,'*'); grid
#%% Test 2
(VDS, n, VT, JS, d1n, d1VT, d1logJS, d2n, d2VT, d2logJS) = XTRACT(NCH, L = 0.18, VDS = 0.6, VSB = 0.0)
import IPython; IPython.embed()
#figure(1); plot(UDS,nn,VDS,n,'*'); grid
#figure(2); plot(UDS1,diff1VT,VDS,d1VT,'*'); grid
#figure(3); plot(UDS2,diff2VT,VDS,d2VT,'*'); grid; pause#

#figure(1); plot(UDS,nn,VDS,n,'*'); grid
#figure(2); plot(UDS1,diff1n,VDS,d1n,'*'); grid
#figure(3); plot(UDS2,diff2n,VDS,d2n,'*'); grid; pause

#figure(1); plot(UDS,Js,VDS,JS,'*'); grid
#figure(2); plot(UDS1,diff1logJs,VDS,d1logJS,'*'); grid
#figure(3); plot(UDS2,diff2logJs,VDS,d2logJS,'*'); grid
