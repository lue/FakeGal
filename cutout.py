import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import pyfits as pf


surveys = ['AEGIS', 'COSMOS', 'GOODS-N', 'GOODS-S', 'UDS']
super_catalog = np.load("super_catalog.npz")

filt = (super_catalog['z_survey'] == 2) & (super_catalog['z_spec'] > 0)

test = get_cutout(super_catalog['ra'][filt],
                  super_catalog['dec'][filt],
                  3.0,
                  surveys[2],
                  savepng=True,
                  ids=super_catalog['s_id'][filt],
                  results=False)


# plt.imshow(test[0][15], interpolation='nearest', cmap='gray_r')
# plt.show()
#
#
# test = get_cutout(cat[filt,3], cat[filt,4], 50, 'GOODSN')
#
# x,y = from_cat_to_img(cat[filt,3],cat[filt,4],w)
# plt.figure(2)
# plt.imshow(np.log10(data2[0].data[::5,::5]), interpolation='nearest')
# plt.plot(x/5.,y/5., '.k')