#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 15:55:49 2020

@author: davsan06
"""

import astropy.io.fits as pf
import numpy as np
import matplotlib.pyplot as plt
import healpy as hp
import seaborn as sns
import skymapper as skm
%matplotlib inline

#Extraemos los datos de magnitudes 'auto' de los ficheros fits
path = '/afs/ciemat.es/user/d/davsan06/WWW/Catalogos/DES_Y1A1_LSSBAO_extended.fits'
table = pf.open(path)[1]

data_ = table.data

# Previsualizamos el catálogo
from astropy.table import Table
Table(data_)

mag_auto_g = data_['mag_auto_g']
mag_auto_r = data_['mag_auto_r']
mag_auto_i = data_['mag_auto_i']
mag_auto_z = data_['mag_auto_z']

#Colores (sin aplicar mascara)
color_gr = mag_auto_g - mag_auto_r
color_ri = mag_auto_r - mag_auto_i
color_iz = mag_auto_i - mag_auto_z

#El numero total de galaxias con las que trabajamos antes de hacer la criba es num_total_gal, posteriormente pasaremos a\n",
#estudiar que porcentaje de estas supone las que cumplen las condiciones que queremos
num_tot_gal = len(color_gr)

#Creamos los diagramas color color
# ax = sns.kdeplot(color_ri, color_gr, shade=True)

# sns.kdeplot(color_iz, color_ri, shade=True)

mask = (color_gr > -5)*(color_gr < 5)*(color_ri > -5)*(color_ri < 5)*(color_iz > -5)*(color_iz < 5)

#Aplicamos la mascara a todos los colores de forma que seleccionemos solo aquellas galaxias que se encuentren en el locus
new_color_gr = color_gr[mask]
new_color_ri = color_ri[mask]
new_color_iz = color_iz[mask]

plt.scatter(new_color_gr, new_color_ri)
sns.kdeplot(new_color_gr[:10000],  new_color_ri[:10000], shade=True)

#Comprobacion
mag_mof_g = data_['mag_mof_g']
mag_mof_r = data_['mag_mof_r']
mag_mof_i = data_['mag_mof_i']
mag_mof_z = data_['mag_mof_z']

color_mof_gr = mag_mof_g - mag_mof_r
color_mof_ri = mag_mof_r - mag_mof_i
color_mof_iz = mag_mof_i - mag_mof_z

sns.kdeplot(color_mof_gr[:1000], color_mof_ri[:1000], shade=True)

mask_mof = (color_mof_gr > -1)*(color_gr < 3)*(color_ri > -1)*(color_ri < 2.5)*(color_iz > -1)*(color_iz < 2)

new_color_mof_gr = color_mof_gr[mask_mof]

num_part_gal = len(new_color_mof_gr[new_color_mof_gr != 0])
num_part_gal = float(num_part_gal)
num_tot_gal = float(num_tot_gal)
part = (num_part_gal/num_tot_gal)*100
