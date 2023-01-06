#%%
import matplotlib.pyplot as plt
import numpy as np
from pygmid import Lookup as lk

NCH = lk('180nch.mat')  # load MATLAB data into pygmid lookup object

#%% Test 1
VGS = NCH.look_upVGS(GM_ID = 10, VDS = 0.6, VSB = 0.1, L = 0.18)
print(f'VGS is: {VGS}')
#%% Test 2
VGS = NCH.look_upVGS(GM_ID = np.arange(10, 16, 1), VDS = 0.6, VSB = 0.1, L = 0.18)
print(f'VGS is: {VGS}')
#%% Test 3
VGS = NCH.look_upVGS(ID_W = 1e-4, VDS = 0.6, VSB = 0.1, L = 0.18)
print(f'VGS is: {VGS}')
#%% Test 4
VGS = NCH.look_upVGS(ID_W = 1e-4, VDS = 0.6, VSB = 0.1, L = np.arange(0.18, 0.5, 0.1))
print(f'VGS is: {VGS}')
#%% Test 5
VGS = NCH.look_upVGS(GM_ID = 10, VDB = 0.6, VGB = 1, L = 0.18)
print(f'VGS is: {VGS}')
#%% Test 6
VGS = NCH.look_upVGS(ID_W = 1e-4, VDB = 0.6, VGB = 1, L = 0.18)
print(f'VGS is: {VGS}')

# %%
