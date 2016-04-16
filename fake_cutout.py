import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import pyfits as pf

from galroutines.cutout import *

surveys = ['AEGIS', 'COSMOS', 'GOODS-N', 'GOODS-S', 'UDS']
super_catalog = np.load("super_catalog.npz")

for i in range(5):
    filt = (super_catalog['z_survey'] == i) & (super_catalog['z_spec'] > 0)
    ra = super_catalog['ra'][filt].mean()
    dec = super_catalog['dec'][filt].mean()
    test = get_cutout([ra],[dec],
                  25.0,
                  surveys[i],
                  savepng=False,
                  ids=[0],
                  results=True)
    np.savez('temp'+str(i)+'.npz', test=test)

### FAKE GAL ###