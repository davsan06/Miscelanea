#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 11:22:33 2020

@author: davsan06
"""

###########################################
#####           CREACION            #######
###########################################

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
%matplotlib inline

from astropy.io import fits
from astropy.utils.data import download_file
from astropy.table import Table, Column
import os

import healpy as hp

# Función para pasar las coordenadas ra, dec de grados a radiantes, unica forma con la que trabaja healpy
def deg2rad(ra, dec):
    PHI = np.radians(ra);
    THETA = np.radians(90. - dec);
    return PHI, THETA

PHI = []
THETA = []

# Recorremos todos todos los ficheros .fits con los que queremos genrar el mapa
# for filename in os.listdir('/scratch/davsan06'):
#     if filename.endswith('.fits'):
#         data = fits.open(os.path.join('/scratch/davsan06', filename), memap = True)[1]
#         phi, theta = deg2rad(data.data['ra'], data.data['dec'])
#         PHI.append(phi)
#         THETA.append(theta)

area_pix = hp.nside2pixarea(512, degrees=True)
print(area_pix)
n_pix = hp.nside2npix(512)

ipix_array = hp.ang2pix(512, THETA, PHI, nest = True, lonlat = False)[0]

ipix_array_def = np.zeros(n_pix)

for pixel in ipix_array:
    index = np.int(pixel)
    ipix_array_def[index] += 1
    
ipix_array_def = ipix_array_def/area_pix
ipix_array_def[ipix_array_def == 0] = hp.UNSEEN

# Guardamos el mapa
hp.write_map('radec_healpy_density_map.fits', ipix_array_def, nest = True, overwrite = True, partial = True, fits_IDL = False, column_names = ['object surface density'])

###########################################
#####        VISUALIZACION          #######
###########################################

from matplotlib.font_manager import FontProperties
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
from matplotlib.colors import LogNorm
plt.rcParams[\"font.family\"] = \"Times New Roman\"

density_map = hp.read_map('/scratch/davsan06/radec_healpy_density_map.fits', nest = True, memmap = True)

hp.cartview(density_map,
            coord=['G'],
            unit = '$n_g[deg^{2}]$', 
            norm = 'hist',
            flip = 'astro', 
            min = 0, 
            max = np.max(density_map),
            lonra = [-70,110], 
            latra = [-80, 20],
            title = 'BAO SAMPLE DES-Y1 FOOTPRINT \n' ,
            nest = True, 
            cbar = True)
hp.graticule()


# Get the power spectrum
Cl = hp.anafast(density_map)
plt.figure()
plt.loglog(Cl)















