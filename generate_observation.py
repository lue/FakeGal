import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pyfits as pf
from galroutines.filters import *
from multiprocessing import Pool


# Image preview
A7 = pf.open('data/C7_0_0.fits')
x = np.genfromtxt('data/C7_0_0.zm')
data = np.zeros([109, 109, len(A7)])
for i in range(len(A7)):
    data[:, :, i] = A7[i].data
plt.figure(1)
plt.imshow(np.log10(np.sum(data[:, :, :], 2)), interpolation='nearest')
plt.show()

# generate SED
plt.figure(2)
lam, flam = get_SED()
plt.plot(lam, flam)
plt.xscale('log')
plt.show()

# Check
c = 3e10
print(np.trapz(x[:, 1], x[:, 0]))  # *1e-23/(6000e6/0.7/10)**2
print(np.trapz(x[:, 1] * x[:, 0] ** 2 / c, c / x[:, 0]))

# See filter
filt, _ = get_filter_by_id(28)
plt.figure(6)
plt.plot(filt[:, 1], filt[:, 2])
plt.show()

# See many filters
# plt.figure(7)
# for i in filters_by_survey(3):
#     filt, _ = get_filter_by_id(i)
#     plt.plot(filt[:, 1], filt[:, 2])
# plt.xscale('log')
# plt.show()

# Generate measurement
lam, flam = get_SED()
lam = lam[::-1]
flam = flam[::-1]
res = get_measurements(lam, flam, 4)
plt.figure(9)
plt.plot(res[:, 0], res[:, 1], 'or', ms=15)
plt.plot(lam, flam, lw=3)
plt.xscale('log')
plt.show()

# # Start generating an observation
# s_id = 4
# z = 7.
# n_filts = filters_by_survey(s_id)
# data_f = np.zeros([int(data.shape[0]), int(data.shape[1]), len(n_filts)])
# inputs = []
# print('Assemble inputs for multithreading')
# for j in range(data.shape[0]):
#     print(j)
#     for k in range(data.shape[1]):
#         lam = (1 + z) * c / x[:, 0] / 1e-8
#         flam = data[j, k, :] * x[:, 0] / (1 + z) / c / (6000e6 / 0.7 / 10) ** 2
#         lam = lam[::-1]
#         flam = flam[::-1]
#         temp = get_measurements(lam, flam, s_id)
#         data_f[j, k, :] = temp[:, 1]

# Start generating an observation
s_id = 4
z = 7.
n_filts = filters_by_survey(s_id)
data_f = np.zeros([int(data.shape[0]), int(data.shape[1]), len(n_filts)])
inputs = []
print('Assemble inputs for multithreading')
for j in range(data.shape[0]):
    for k in range(data.shape[1]):
        lam = (1 + z) * c / x[:, 0] / 1e-8
        flam = data[j, k, :] * x[:, 0] / (1 + z) / c / (6000e6 / 0.7 / 10) ** 2
        lam = lam[::-1]
        flam = flam[::-1]
        inputs.append([lam, flam, s_id])
print("Run...")
p = Pool(7)
res = (p.map(get_measurements_m, inputs))
l = 0
print('Disassembling...')
for j in range(data.shape[0]):
    for k in range(data.shape[1]):
        temp = res[l]
        data_f[j, k, :] = temp[:, 1]
        l = l+1
print('Done')

# Plot
import scipy.ndimage as ndimage
print(data_f.shape)

plt.figure(10)

for ii in range(18):
    ax = plt.subplot(3,6,ii+1)
    i = np.argsort(temp[:,0])[ii]
    noise = 0.0 * np.random.randn(data_f.shape[0]*data_f.shape[1]).reshape([data_f.shape[0], data_f.shape[1]]) * 0.00001
    plt.imshow(noise + ndimage.gaussian_filter(data_f[:,:,i], sigma=(2, 2), order=0), interpolation='nearest', cmap='gray_r')
    _, name = get_filter_by_id(filters_by_survey(s_id)[i])
    # plt.title(name.split('.')[0], size=8)
    ax.set_yticklabels([])
    ax.set_xticklabels([])

# img = ndimage.gaussian_filter(img, sigma=(5, 5, 0), order=0)
plt.tight_layout(pad=0.0, w_pad=0.0, h_pad=0.0)
