import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import pyfits as pf

cat = np.genfromtxt('data/goodsn_3dhst.v4.1.cat')
filt = cat[:,45]>200.

test = get_cutout(cat[:,3], cat[:,4], 3.0, 'GOODSN', savepng=True, ids=cat[:,0], results=False)


plt.imshow(test[0][15], interpolation='nearest', cmap='gray_r')
plt.show()


test = get_cutout(cat[filt,3], cat[filt,4], 50, 'GOODSN')

x,y = from_cat_to_img(cat[filt,3],cat[filt,4],w)
plt.figure(2)
plt.imshow(np.log10(data2[0].data[::5,::5]), interpolation='nearest')
plt.plot(x/5.,y/5., '.k')