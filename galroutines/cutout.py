import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pyfits as pf
from astropy.wcs import WCS
import glob

def get_cutout(ra, dec, angsize, survey, savepng=False, results=True, ids=[], filter=0):
    '''

    '''
    if survey=='AEGIS':
        prefix = 'data/aegis/'
        files = [['IRAC1', 'AEGIS_CH1_SEDS/AEGIS_CH1_SEDS_sci.fits.gz'],
                 ['IRAC2', 'AEGIS_CH2_SEDS/AEGIS_CH2_SEDS_sci.fits.gz'],
                 ['F125W', 'aegis_3dhst.v4.0.F125W_orig_sci.fits.gz'],
                 ['F140W', 'aegis_3dhst.v4.0.F140W_orig_sci.fits.gz'],
                 ['F160W', 'aegis_3dhst.v4.0.F160W_orig_sci.fits.gz'],
                 ['F606W', 'aegis_3dhst.v4.0.F606W_orig_sci.fits.gz'],
                 ['F814W', 'aegis_3dhst.v4.0.F814W_orig_sci.fits.gz']]
    elif survey == 'COSMOS':
        prefix = 'data/cosmos/'
        files = [['IRAC1', 'COSMOS_CH1_SEDS/COSMOS_CH1_SEDS_sci.fits.gz'],
                 ['IRAC2', 'COSMOS_CH2_SEDS/COSMOS_CH2_SEDS_sci.fits.gz'],
                 ['F125W', 'cosmos_3dhst.v4.0.F125W_orig_sci.fits.gz'],
                 ['F140W', 'cosmos_3dhst.v4.0.F140W_orig_sci.fits.gz'],
                 ['F160W', 'cosmos_3dhst.v4.0.F160W_orig_sci.fits.gz'],
                 ['F606W', 'cosmos_3dhst.v4.0.F606W_orig_sci.fits.gz'],
                 ['F814W', 'cosmos_3dhst.v4.0.F814W_orig_sci.fits.gz']]
    elif survey == 'GOODS-N':
        prefix = 'data/goodsn/'
        files = [['IRAC1', 'GOODS-N_SEDS1/GOODS-N_SEDS1_sci.fits.gz'],
                 ['IRAC2', 'GOODS-N_SEDS2/GOODS-N_SEDS2_sci.fits.gz'],
                 ['F125W', 'goodsn_3dhst.v4.0.F125W_orig_sci.fits.gz'],
                 ['F140W', 'goodsn_3dhst.v4.0.F140W_orig_sci.fits.gz'],
                 ['F160W', 'goodsn_3dhst.v4.0.F160W_orig_sci.fits.gz'],
                 ['F435W', 'goodsn_3dhst.v4.0.F435W_orig_sci.fits.gz'],
                 ['F606W', 'goodsn_3dhst.v4.0.F606W_orig_sci.fits.gz'],
                 ['F775W', 'goodsn_3dhst.v4.0.F775W_orig_sci.fits.gz'],
                 ['F850LP', 'goodsn_3dhst.v4.0.F850LP_orig_sci.fits.gz']]
    elif survey=='GOODS-S':
        prefix = 'data/goodss/'
        files = [['IRAC1', 'GOODS-S_SEDS1/GOODS-S_SEDS1_sci_sub.fits.gz'],
                 ['IRAC2', 'GOODS-S_SEDS2/GOODS-S_SEDS2_sci_sub.fits.gz'],
                 ['F125W', 'goodss_3dhst.v4.0.F125W_orig_sci.fits.gz'],
                 ['F140W', 'goodss_3dhst.v4.0.F140W_orig_sci.fits.gz'],
                 ['F160W', 'goodss_3dhst.v4.0.F160W_orig_sci.fits.gz'],
                 ['F435W', 'goodss_3dhst.v4.0.F435W_orig_sci.fits.gz'],
                 ['F606W', 'goodss_3dhst.v4.0.F606W_orig_sci.fits.gz'],
                 ['F775W', 'goodss_3dhst.v4.0.F775W_orig_sci.fits.gz'],
                 ['F850LP', 'goodss_3dhst.v4.0.F850LP_orig_sci.fits.gz']]
    elif survey == 'UDS':
        prefix = 'data/uds/'
        files = [['IRAC1', 'UDS_SEDS1/UDS_SEDS1_sci.fits.gz'],
                 ['IRAC2', 'UDS_SEDS2/UDS_SEDS2_sci.fits.gz'],
                 ['F125W', 'uds_3dhst.v4.0.F125W_orig_sci.fits.gz'],
                 ['F140W', 'uds_3dhst.v4.0.F140W_orig_sci.fits.gz'],
                 ['F160W', 'uds_3dhst.v4.0.F160W_orig_sci.fits.gz'],
                 ['F606W', 'uds_3dhst.v4.0.F606W_orig_sci.fits.gz'],
                 ['F814W', 'uds_3dhst.v4.0.F775W_orig_sci.fits.gz']]
    else:
        print('ERROR!')
    res = []
    if savepng:
        fig = plt.figure(0, figsize=(1, 1), dpi=200, frameon=False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
    for i in range(len(files)):
        print(files[i][0])
        w = WCS(prefix + files[i][1])
        data = pf.open(prefix + files[i][1])
        sizex = np.abs(1.0 * angsize / 3600 / data[0].header['CD2_2'])/2.0
        sizey = np.abs(1.0 * angsize / 3600 / data[0].header['CD1_1'])/2.0
        output = []
        for j in range(len(ra)):
            temp = w.all_world2pix(ra[j], dec[j], 1)
            x = temp[1]  # [0]
            y = temp[0]  # [0]
            img = data[0].data[np.round(x)-sizex:np.round(x)+sizex, np.round(y)-sizey:np.round(y)+sizey]
            if results:
                output.append(img)
            if savepng:
                plt.clf()
                ax = plt.Axes(fig, [0., 0., 1., 1.])
                ax.set_axis_off()
                fig.add_axes(ax)
                ax.imshow(img, interpolation='nearest', cmap='cubehelix_r', aspect='normal')
                plt.savefig('output/'+survey+'/%06d_%2.2f_'%(ids[j], angsize)+files[i][0]+'.png')
        if results:
            res.append(output)
    return res



