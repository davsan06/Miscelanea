#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 10:45:03 2020

@author: davsan06
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# %matplotlib inline

from astropy.io import fits
from astropy.utils.data import download_file
from astropy.table import Table, Column
import os

import skymapper as skm

ra = []
dec = []

# for filename in os.listdir('/scratch/davsan06/BAOSampleDATA/'):
#     if filename.endswith('.fits'):
#        data = fits.open(os.path.join('/scratch/davsan06/BAOSampleDATA/', filename), memap = True)[1]
#        ra.append(data.data['ra'])
#        dec.append(data.data['dec'])

list_of_files = ['DES_Y1A1_LSSBAO_extended_0607.fits', 'DES_Y1A1_LSSBAO_extended_0708.fits',
                 'DES_Y1A1_LSSBAO_extended_0809.fits', 'DES_Y1A1_LSSBAO_extended_0910.fits']

for filename in list_of_files:
    print(filename)
    data = fits.open(os.path.join('/scratch/davsan06/BAOSampleDATA/', filename), memap = True)[1]
    ra.append(data.data['ra'])
    dec.append(data.data['dec'])
       
ra = np.array(ra)
dec = np.array(dec)

ra_def = np.array([])
dec_def = np.array([])

for i in np.arange(0,len(ra),1):
    # i = 1
    ra_def = np.hstack([ra[i][:], ra_def])
    dec_def = np.hstack([dec[i][:], dec_def])
    
from matplotlib.font_manager import FontProperties
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
from matplotlib.colors import LogNorm
# plt.rcParams[\"font.family\"] = \"Times New Roman\"

fig = plt.figure(figsize=(13,13))
ax = fig.add_subplot(111, aspect='equal')

bc, ra_new, dec_new, vertices = skm.getCountAtLocations(ra_def, dec_def, nside=512, return_vertices=True)
cmap = cm.magma

proj = skm.createConicMap(ax, ra_new, dec_new, proj_class=skm.LambertConformalProjection, ra0=0, dec0=-30); ### map rotation
meridians = np.arange(-50, 10, 10)
parallels = np.array([180, 150, 120, 90, 60, 30, 0, 330, 300, 270])

skm.setMeridianPatches(ax, proj, meridians, linestyle='-', lw=0.5, alpha=0.3, zorder=2)
skm.setParallelPatches(ax, proj, parallels, linestyle='-', lw=0.5, alpha=0.3, zorder=2)
skm.setMeridianLabels(ax, proj, meridians, loc='left', fmt=skm.pmDegFormatter)
skm.setParallelLabels(ax, proj, parallels, loc='bottom', fmt=skm.pmDegFormatter)

vmin, vmax = np.percentile(bc,[10,90])
poly = skm.addPolygons(vertices, proj, ax, color=bc, vmin=vmin, vmax=vmax, cmap=cmap, zorder=3, rasterized=True)

from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='2%', pad=0.0)
cb = fig.colorbar(poly, cax=cax)
cb.set_label('\\nn$_{ g}$ [arcmin$^{-2}$]', fontsize=16)
cb.solids.set_edgecolor('face')
cax.tick_params(labelsize = 14, axis = 'y', which='major', pad=10, direction='in', length = 6, width = 1)

for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1)


ax.set_xlabel('\\n RA', fontsize = 18)
ax.set_ylabel('\\n DEC', fontsize = 18)
ax.tick_params(labelsize = 16, axis = 'x', which='major', pad=10, direction='in', length = 8, width = 1)
ax.tick_params(labelsize = 16, axis = 'y', which='major', pad=10, direction='in', length = 8, width = 1)
ax.set_title('DES Galaxy Sample for BAO measurement \\n', fontsize = 22)
fig.tight_layout()
fig.savefig('Galaxy_Sample_BAO_Measurement.png', bbox_inches = 'tight')
