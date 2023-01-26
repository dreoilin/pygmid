#%%
import matplotlib.pyplot as plt
import numpy as np
from pygmid import Lookup as lk
from pygmid import EKV_param_extraction, XTRACT

NCH = lk('180nch.mat')  # load MATLAB data into pygmid lookup object

#%% Test 1
(VDS, n, VT, JS, d1n, d1VT, d1logJS, d2n, d2VT, d2logJS) = EKV_param_extraction(NCH, 1, L = 0.18, VDS = 0.6, VSB = 0.0)

#%% Test 2
(VDS, n, VT, JS, d1n, d1VT, d1logJS, d2n, d2VT, d2logJS) = XTRACT(NCH, L = 0.18, VDS = 0.6, VSB = 0.0)

