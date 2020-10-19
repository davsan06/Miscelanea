#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 12:33:08 2020

@author: davsan06
"""

from astropy.io import fits
from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt

fits_table_name = '/scratch/davsan06/BAOSampleDATA/DES_Y1A1_LSSBAO_extended_0607.fits'

hdul = fits.open(fits_table_name)

data = hdul[1].data

# Ver la primera fila de la tabla
print(data[0])

# Columnas contenidas en el tablón fits
cols = hdul[1].columns
cols

# Previsualizar el tablon
evt_data = Table(data)
evt_data['Z']

# Calculamos el valor medio del redshift en este bin
z_mean = np.mean(evt_data['Z'])
z_mean

# Calculamos la desviación estaándar en el redshift
z_sigma = np.std(evt_data['Z'])
z_sigma

# Pintamos la distribución de redshift
plt.hist(evt_data['Z'])
