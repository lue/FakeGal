import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pyfits as pf
from astropy.wcs import WCS
import glob

def get_cutout(ra, dec, angsize, survey, savepng=False, results=True, ids=[], filter=-1, path='./'):
    '''
    This function plots and retruns a cut-out
    :param ra: RA coordinate
    :param dec: DEC coordinate
    :param angsize: angular size of the image in arcsec
    :param survey: survey name
    :param savepng: True/False -- save a png image
    :param results: True/False -- return the images
    :param ids: ids of the sources (necessary to name an output file)
    :param filter: if -1 all filters are processed, if [...] -- only selected filters
    :param path: a path where data is stored
    :return: list of 2D images
    '''
    # for each survey, we define a list of files
    if survey=='AEGIS':
        prefix = path+'data/aegis/'
        files = [['IRAC1', 'AEGIS_CH1_SEDS_sci_reg.fits'],
                 ['IRAC2', 'AEGIS_CH2_SEDS_sci_reg.fits'],
                 ['F125W', 'aegis_3dhst.v4.0.F125W_orig_sci.fits.gz'],
                 ['F140W', 'aegis_3dhst.v4.0.F140W_orig_sci.fits.gz'],
                 ['F160W', 'aegis_3dhst.v4.0.F160W_orig_sci.fits.gz'],
                 ['F606W', 'aegis_3dhst.v4.0.F606W_orig_sci.fits.gz'],
                 ['F814W', 'aegis_3dhst.v4.0.F814W_orig_sci.fits.gz']]
    elif survey == 'COSMOS':
        prefix = path+'data/cosmos/'
        files = [['IRAC1', 'COSMOS_CH1_SEDS_sci_reg.fits'],
                 ['IRAC2', 'COSMOS_CH2_SEDS_sci_reg.fits'],
                 ['F125W', 'cosmos_3dhst.v4.0.F125W_orig_sci.fits.gz'],
                 ['F140W', 'cosmos_3dhst.v4.0.F140W_orig_sci.fits.gz'],
                 ['F160W', 'cosmos_3dhst.v4.0.F160W_orig_sci.fits.gz'],
                 ['F606W', 'cosmos_3dhst.v4.0.F606W_orig_sci.fits.gz'],
                 ['F814W', 'cosmos_3dhst.v4.0.F814W_orig_sci.fits.gz']]
    elif survey == 'GOODS-N':
        prefix = path+'data/goodsn/'
        files = [['IRAC1', 'GOODS-N_SEDS1_sci_sub_reg.fits'],
                 ['IRAC2', 'GOODS-N_SEDS2_sci_sub_reg.fits'],
                 ['F125W', 'goodsn_3dhst.v4.0.F125W_orig_sci.fits.gz'],
                 ['F140W', 'goodsn_3dhst.v4.0.F140W_orig_sci.fits.gz'],
                 ['F160W', 'goodsn_3dhst.v4.0.F160W_orig_sci.fits.gz'],
                 ['F435W', 'goodsn_3dhst.v4.0.F435W_orig_sci.fits.gz'],
                 ['F606W', 'goodsn_3dhst.v4.0.F606W_orig_sci.fits.gz'],
                 ['F775W', 'goodsn_3dhst.v4.0.F775W_orig_sci.fits.gz'],
                 ['F850LP', 'goodsn_3dhst.v4.0.F850LP_orig_sci.fits.gz']]
    elif survey=='GOODS-S':
        prefix = path+'data/goodss/'
        files = [['IRAC1', 'GOODS-S_SEDS1_sci_sub_reg.fits'],
                 ['IRAC2', 'GOODS-S_SEDS2_sci_sub_reg.fits'],
                 ['F125W', 'goodss_3dhst.v4.0.F125W_orig_sci.fits.gz'],
                 ['F140W', 'goodss_3dhst.v4.0.F140W_orig_sci.fits.gz'],
                 ['F160W', 'goodss_3dhst.v4.0.F160W_orig_sci.fits.gz'],
                 ['F435W', 'goodss_3dhst.v4.0.F435W_orig_sci.fits.gz'],
                 ['F606W', 'goodss_3dhst.v4.0.F606W_orig_sci.fits.gz'],
                 ['F775W', 'goodss_3dhst.v4.0.F775W_orig_sci.fits.gz'],
                 ['F850LP', 'goodss_3dhst.v4.0.F850LP_orig_sci.fits.gz']]
    elif survey == 'UDS':
        prefix = path+'data/uds/'
        files = [['IRAC1', 'UDS_SEDS1_sci_sub_reg.fits'],
                 ['IRAC2', 'UDS_SEDS2_sci_sub_reg.fits'],
                 ['F125W', 'uds_3dhst.v4.0.F125W_orig_sci.fits.gz'],
                 ['F140W', 'uds_3dhst.v4.0.F140W_orig_sci.fits.gz'],
                 ['F160W', 'uds_3dhst.v4.0.F160W_orig_sci.fits.gz'],
                 ['F606W', 'uds_3dhst.v4.0.F606W_orig_sci.fits.gz'],
                 ['F814W', 'uds_3dhst.v4.0.F814W_orig_sci.fits.gz']]
    else:
        print('ERROR!')
    res = []
    # if the picture is requested, initialize a figure
    if savepng:
        fig = plt.figure(0, figsize=(1, 1), dpi=200, frameon=False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
    # loop through all files
    if filter==-1:
        filters = range(len(files))
    else:
        filters = filter
    for i in filters:
        print(files[i][0])
        w = WCS(prefix + files[i][1])
        data = pf.open(prefix + files[i][1])
        sizex = np.abs(1.0 * angsize / 3600 / data[0].header['CD2_2'])/2.0
        sizey = np.abs(1.0 * angsize / 3600 / data[0].header['CD1_1'])/2.0
        output = []
        # loop through all pointings
        for j in range(len(ra)):
            # converts the sky coordinates into pixel position
            temp = w.all_world2pix(ra[j], dec[j], 1, quiet=True)
            x = temp[1]  # [0]
            y = temp[0]  # [0]
            img = data[0].data[np.round(x)-sizex:np.round(x)+sizex, np.round(y)-sizey:np.round(y)+sizey]
            if results:
                output.append(img)
            # if the picture is requested, generate an image
            if savepng:
                vmax = img[sizex-5:sizex+5, sizey-5:sizey+5].max()
                plt.clf()
                ax = plt.Axes(fig, [0., 0., 1., 1.])
                ax.set_axis_off()
                fig.add_axes(ax)
                ax.imshow(img, interpolation='nearest', cmap='gray_r', aspect='normal', vmax=vmax)
                plt.savefig('output/'+survey+'/%06d_%2.2f_'%(ids[j], angsize)+files[i][0]+'.png')
        if results:
            res.append(output)
    return res



