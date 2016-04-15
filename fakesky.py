
###
fsky = np.load('test2.npz')
skyx = fsky['data'][4][0]
ii = 11

from scipy.misc import imresize
plt.figure(14)
plt.subplot(221)
plt.imshow(skyx, cmap='cubehelix_r')
plt.colorbar()
plt.subplot(222)
i = np.argsort(temp[:,0])[ii]
noise = 0.0 * np.random.randn(data_f.shape[0]*data_f.shape[1]).reshape([data_f.shape[0], data_f.shape[1]]) * 0.00001
img = noise + ndimage.gaussian_filter(data_f[:,:,i], sigma=(3, 3), order=0)
img2 = imresize(img, [82,82], interp='bilinear')/82.**2/1.
# img.
plt.imshow(img2, interpolation='nearest', cmap='cubehelix_r')
plt.colorbar()
_, name = get_filter_by_id(filters_by_survey(s_id)[i])
plt.subplot(223)
plt.imshow(img2+skyx[-82:,:82], interpolation='nearest', cmap='cubehelix_r')


plt.show()