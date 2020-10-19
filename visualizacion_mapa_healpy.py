#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 13:50:22 2020

@author: davsan06
"""

import matplotlib.pyplot as plt
import numpy as np
import healpy as hp

# Leemos el mapa
map_name = '/scratch/davsan06/radec_healpy_density_map.fits'
map_des = hp.read_map(map_name)
