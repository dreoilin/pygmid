#%%
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pygmid import Lookup as lk
from time import time

# setup mpl
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams.update({"axes.grid" : True})
#%%
# Slide 1
NCH = lk('90n1rvt.pkl')  # load MATLAB data into pygmid lookup object

VDSs = [0.4, 0.5, 0.6, 0.7]
VGSs = [0.4, 0.5, 0.6]

gms = NCH.look_up('GM', vds=VDSs, vgs=VGSs)
print(f"VGSs={VGSs}")
print(f"VDSs={VDSs}")
print(gms*1e6)

gm = NCH.look_up('GM', vds=0.5, vgs=0.6)
print(f"gm is: {gm}")
# %%
