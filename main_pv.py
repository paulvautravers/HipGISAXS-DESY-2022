import json
import sys

from common import xp
from common import array_type
import numpy as np
from collections import OrderedDict

import math as m
import matplotlib.pyplot as plt
from ff.cylinder import cylinder
from fresnel import propagation_coeffs
from structure_factor import structure_factor
from qspace import generate_qspace
from common import memcopy_to_device
import matplotlib.colors as colors

from PIL import Image

if __name__ == '__main__':
    
    # load input parameters
    with open('../json/config.json') as fp:
        cfg = json.load(fp)

    alphai = xp.single(cfg['incident'] * xp.pi / 180)
    alpha = xp.array(cfg['alpha'], dtype=np.single)
    theta = xp.array(cfg['theta'], dtype=np.single)
    wavelength = cfg['wavelen']
    reflectivity_index = complex(cfg['delta'], cfg['beta'])
    
    N = 300
    sample = sys.argv[1]
    path_npy = '/home/vautravp/Documents/hipgisaxs/hipgisaxs-2.0/npy_files_2/agnw_2360/'
    file_npy = 'agnw_2360_s{}.npy'.format(int(sample))
    
    #-----------------------
    temp = xp.array(np.load(path_npy+file_npy), dtype=np.single)
    temp = temp.transpose()
    #-----------------------
    # split work
    Ntotal = temp.shape[1]

    qx, qy, qz = generate_qspace(alphai, alpha, theta, wavelength)
    propagation = propagation_coeffs(alphai, alpha.ravel(), reflectivity_index)

    scat = xp.zeros((Ntotal, qx.size), dtype=np.csingle)
    for ibeg in range(0, Ntotal, N):

        # partition orientation and shifts
        iend = min(ibeg+N, Ntotal)
        shifts = temp[0:3,ibeg:iend]
        orientations = OrderedDict({'x': temp[3,ibeg:iend]*1000, 'y': temp[4,ibeg:iend]*1000, 'z': temp[5,ibeg:iend]*1000})
        radius = temp[6,ibeg:iend]*1000
        height = temp[7,ibeg:iend]*1000

        # DWBA
        for j in range(4):
            ff = cylinder(qx, qy, qz[j], radius, height, orientation = orientations, shift = shifts)
            scat[ibeg:iend] += propagation[j] * ff

    img = scat.sum(axis=0)
    img = xp.abs(img)**2
    img = img.reshape(qx.shape)

    if "cupy" in  array_type:
        img = img.get().astype(float)

    fig,ax1 = plt.subplots(figsize=(12,12))
    qp = xp.sqrt(qx**2 + qy**2)
    qv = qz[0]
    qrange = [-qp.max(),qp.max(),qv.min(),qv.max()]

    plot = ax1.imshow(xp.log(img+1), cmap='jet',origin='lower',extent=qrange)
    plt.xlabel('$Q_{xy}$ (${\AA}^{-1})$')
    plt.ylabel('$Q_z$ (${\AA}^{-1})$')
    fig.colorbar(plot,ax=ax1)

    path_img = '/home/vautravp/Documents/hipgisaxs/hipgisaxs-2.0/agnw_2360_imgs/0.4_deg/28.09.22/'
    file_img = file_npy[:-3]+'png'
    plt.savefig(path_img+file_img,bbox_inches='tight')
    
    #im_to_tiff = Image.fromarray(img)
    #print(np.shape(im_to_tiff))
    #im_to_tiff.save(path_img+'tiff/'+file_npy[:-3]+"tiff")
    #plt.show()
