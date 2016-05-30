import numpy as np
import pyfits as pf


def get_SED(coords='all', z=7):
    A7 = pf.open('data/C7_0_0.fits')
    x = np.genfromtxt('data/C7_0_0.zm')
    data = np.zeros([109, 109, len(A7)])
    for i in range(len(A7)):
        data[:, :, i] = A7[i].data
    c = 3e10
    if coords == 'all':
        lam = (1+z)*c/x[:,0]/1e-8
        flam = x[:,1]*x[:,0]/(1+z)/c/(6000e6/0.7/10)**2
    else:
        lam  = (1+z)*c/x[:,0]/1e-8
        flam = data[coords[0], coords[1], :]*x[:,0]/(1+z)/c/(6000e6/0.7/10)**2
    flam[lam<(1.+z)*1215] = 0
    return lam, flam


def filters_by_survey(s):
    if s==0:
        fname = 'data/aegis_3dhst.v4.1.translate'
    elif s==1:
        fname = 'data/cosmos_3dhst.v4.1.translate'
    elif s==2:
        fname = 'data/goodsn_3dhst.v4.1.translate'
    elif s==3:
        fname = 'data/goodss_3dhst.v4.1.translate'
    elif s==4:
        fname = 'data/uds_3dhst.v4.2.translate'
    filt_list = np.genfromtxt(fname, dtype=None)
    return np.unique(np.array([a[1:] for a in filt_list[:,1]]).astype(int))


filters_info = []
for line in open('data/FILTER.RES.latest.info', 'r'):
    filters_info.append(np.array(line.split()))
filters_info = np.array(filters_info)

temp_filters = open('data/FILTER.RES.latest', 'r')
filters = []
filters_names = []
first = True

for line in temp_filters:
    if line[0] == ' ':
        if not first:
            filters.append(np.array(temp))
        first = False
        filters_names.append(line.split())
        temp = []
        # print            line
    else:
        temp.append(np.array(line.split()).astype('float'))

filters = np.array(filters)
filters_names = np.array(filters_names)
filters_names[np.array([a[0] for a in filters_names]).astype(int) == 236]

def get_filter_by_id(id):
    temp = np.array([a[0] for a in filters_info]).astype(int)
    name = filters_info[np.where(temp==id)[0][0]][1]
    names = np.array([a[1] for a in filters_names])
#     print name
    return filters[np.where(name == names)[0][0]], name


def get_measurements(lam, flam, s_id):
    filters_list = filters_by_survey(s_id)
#     print filters_list
    res = np.zeros([len(filters_list),2])
    j=0
    for i in filters_list:
#         print i
        filt, _ = get_filter_by_id(i)
        flam_temp = np.interp(filt[:,1], lam, flam, left=0, right=0)
        f_flam = np.trapz(flam_temp*filt[:, 2], filt[:,1]) / np.trapz(filt[:, 2], filt[:,1])
        f_lam = np.trapz(filt[:,1]*filt[:, 2], filt[:,1]) / np.trapz(filt[:, 2], filt[:,1])
        res[j,:] = f_lam, f_flam
        j+=1
#         print f_lam, f_flam
    return res

def get_measurements_m(inp):
    lam, flam, s_id = inp[0], inp[1], inp[2]
    filters_list = filters_by_survey(s_id)
    #     print filters_list
    res = np.zeros([len(filters_list),2])
    j=0
    for i in filters_list:
        #         print i
        filt, _ = get_filter_by_id(i)
        flam_temp = np.interp(filt[:,1], lam, flam, left=0, right=0)
        f_flam = np.trapz(flam_temp*filt[:, 2], filt[:,1]) / np.trapz(filt[:, 2], filt[:,1])
        f_lam = np.trapz(filt[:,1]*filt[:, 2], filt[:,1]) / np.trapz(filt[:, 2], filt[:,1])
        res[j,:] = f_lam, f_flam
        j+=1
        #         print f_lam, f_flam
    return res


def get_measurements_m2(inp):
    lam, flam, s_id = inp[0], inp[1], inp[2]
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