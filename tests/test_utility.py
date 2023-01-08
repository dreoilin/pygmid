#%%
import matplotlib.pyplot as plt
import numpy as np
from pygmid import Lookup as lk
from pygmid import EKV_param_extraction, XTRACT

NCH = lk('180nch.mat')  # load MATLAB data into pygmid lookup object

#%% Test 1
ret = EKV_param_extraction(NCH, 1, L = 0.18, VDS = 0.6, VSB = 0.0)
print(f'Return is: {ret}')

#%% Test 2
ret = XTRACT(NCH, L = 0.18, VDS = 0.6, VSB = 0.0)
print(f'Return is: {ret}')
