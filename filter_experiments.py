import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pyfits as pf


from galroutines.cutout import *

#################


super_catalog = np.load("super_catalog.npz")

filt = (super_catalog['z_survey'] == 2) & (super_catalog['z_spec'] > 0) & (super_catalog['z_phot'] > 7) & (super_catalog['z_phot'] > 8)
print(super_catalog['ra'][filt])
print(super_catalog['dec'][filt])
print(super_catalog['s_id'][filt])

ra = (super_catalog['ra'][filt])[0]
dec = (super_catalog['dec'][filt])[0]
test = get_cutout([ra],[dec],
              0.35,
              'GOODS-N',
              savepng=False,
              ids=[0],
              results=True)

plt.imshow(test[4][0], interpolation='nearest')
plt.colorbar()
[test[i][0].sum() for i in range(9)]

id      x               y           ra          dec       faper_F160W eaper_F160W faper_F140W eaper_F140W f_F160W   e_F160W   w_F160W  f_U        e_U       w_U      f_F435W    e_F435W    w_F435W  f_B         e_B     w_B       f_G       e_G         w_G     f_V       e_V       w_V       f_F606W   e_F606W    w_F606W f_R e_R w_R f_Rs e_Rs w_Rs f_I e_I w_I f_F775W e_F775W w_F775W f_Z e_Z w_Z f_F850LP e_F850LP w_F850LP f_F125W e_F125W w_F125W f_J e_J w_J f_F140W e_F140W w_F140W f_H e_H w_H f_Ks e_Ks w_Ks f_IRAC1 e_IRAC1 w_IRAC1 f_IRAC2 e_IRAC2 w_IRAC2 f_IRAC3 e_IRAC3 w_IRAC3 f_IRAC4 e_IRAC4 w_IRAC4 tot_cor wmin_ground wmin_hst wmin_wfc3 wmin_irac z_spec star_flag kron_radius a_image b_image theta_J2000 class_star flux_radius fwhm_image flags IRAC1_contam IRAC2_contam IRAC3_contam IRAC4_contam contam_flag f140w_flag use_phot near_star nexp_f125w nexp_f140w nexp_f160w
32031  12312.867000  14069.563000  189.157897  62.302372  0.435701      0.025325  0.412407      0.050478  0.642202  0.064527  1.000000 -0.072453  0.046501  1.000000 -0.001356  0.027281  0.903542 -0.014277  0.042668  0.394436  0.042418  0.065412  1.000000 -0.012985  0.022811  0.767741 -0.009116  0.020883  0.897895 -0.024979  0.051052  0.809844  0.102682  0.109466  1.000000  0.031359  0.080142  0.806243  0.055461  0.032724  0.884200 -0.037085  0.109461  0.856880  0.002374  0.042352  0.829078  0.555046  0.028187  1.000000 -99.000000 -99.000000  0.000000  0.615709  0.074402  1.000000 -99.000000 -99.000000  0.000000 -99.000000 -99.000000  0.000000  0.740638  0.275089  0.474001  1.820654  0.216056  0.598079  0.150556  1.494974  0.839011 -0.303523  1.413945  0.828375  1.098241  0.000000  0.829078  1.000000  0.474001 -1.000000     2  3.900000  3.771000  2.422000  23.800000  0.340000  3.905000  0.000000     0  0.521886  0.211085  2.086870  0.119268     1     0     1 0  16.0  10.0  16.0

# plt.plot(super_catalog['z_spec'][filt],super_catalog['z_phot'][filt],'.')

#################


















#zm = pf.open('zimu/C7_0_0.fits')
zm = np.genfromtxt('zimu/C7_0_0.zm')

plt.plot(zm[:,0], zm[:,1])
plt.xscale('log')

np.trapz(zm[:,0]*)


def get_measurements(lam, flam, s_id):
    filters_list = filters_by_survey(s_id)
#     print filters_list
    res = np.zeros([len(filters_list),2])
    j=0
    for i in filters_list:
#         print i
        filt, _ = get_filter_by_id(i)
        flam_temp = np.interp(filt[:,1], lam, flam, left=0, right=0)
        f_flam = np.trapz(flam_temp*filt[:, 2], filt[:,1])
        f_lam = np.trapz(filt[:,1]*filt[:, 2], filt[:,1]) / np.trapz(filt[:, 2], filt[:,1])
        res[j,:] = f_lam, f_flam
        j+=1
#         print f_lam, f_flam
    return res

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
