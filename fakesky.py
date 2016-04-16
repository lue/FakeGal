import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

###
fsky = np.load('temp2.npz')
names= ['IRAC1',
'IRAC2',
'F125W',
'F140W',
'F160W',
'F435W',
'F606W',
'F775W',
'F850LP']
ii_list = [0, 1, 9, 10, 11, 18, 19, 20, 21]


for j in range(len(ii_list)):
    skyx = fsky['test'][j][0]
    ii = ii_list[j]
    from scipy.misc import imresize
    ax = plt.subplot(2,len(ii_list),j+1)
    plt.imshow(skyx, cmap='cubehelix_r')
    # plt.colorbar()
    #plt.subplot(222)
    i = np.argsort(temp[:,0])[ii]
    # noise = 0.0 * np.random.randn(data_f.shape[0]*data_f.shape[1]).reshape([data_f.shape[0], data_f.shape[1]]) * 0.00001
    img = ndimage.gaussian_filter(data_f[:,:,i], sigma=(3, 3), order=0)
    img2 = imresize(img, [82,82], interp='bilinear')/82.**2/1.
    # img.
    #plt.imshow(img2, interpolation='nearest', cmap='cubehelix_r')
    _, name = get_filter_by_id(filters_by_survey(s_id)[i])
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    plt.title(names[j])
    ax = plt.subplot(2,len(ii_list),j+1+len(ii_list))
    plt.imshow(img2+skyx[-82:,:82], interpolation='nearest', cmap='cubehelix_r')
    # plt.colorbar()
    ax.set_yticklabels([])
    ax.set_xticklabels([])

# img = ndimage.gaussian_filter(img, sigma=(5, 5, 0), order=0)
plt.tight_layout(pad=0.0, w_pad=0.0, h_pad=0.0)
plt.show()