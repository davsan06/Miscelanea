
#Script to generate ACF of CMB from Angular Power Spectrum computed with COSMOSIS from a
#certain cosmology

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import legendre

#Import data from Cosmosis, tt modes and multipoles l

ell = np.loadtxt('/scratch/davsan06/CMB-TREECORR/mytest_CMB/cmb_cl/ell.txt')
tt = np.loadtxt('/scratch/davsan06/CMB-TREECORR/mytest_CMB/cmb_cl/tt.txt')

#tt is defines as tt = D_l = C_l*l*(l+1)/2pi, so

Cl = tt*2*np.pi/(ell*(ell+1))

#Unnecesary plot

plt.figure()

plt.plot(ell, tt, marker = 'x')
fluct_plot = plt.plot(ell[202], tt[202], marker = 'o')

plt.savefig('Angular-fluctuation-Power-Spectrum')

#Unnecesary code with Legendre polynomial extension to higer grades

#def legendre_extension(n,theta):
    
    #legendre_ext = ((2*n + 1)*theta*legendre(n)(theta) - n*legendre(n-1)(theta))/(n + 1)
    
    #return legendre_ext

# l_max -> highly dependant variable over computation time

l_max = 2500

#Sum over the multipoles (default l in [2, 2500])

def sum_over_ell(ell, theta):
    
    sum_ell = 0
    i = 0
    
    for l in ell[:l_max]:
        
        a = (2*l + 1)*Cl[i]*legendre(l)(np.cos(np.deg2rad(theta)))
        
        sum_ell = sum_ell + a
        
        i = i + 1
    
    return sum_ell

#Angular correlation function

def omega(ell, theta):
    
    return 1/(4*np.pi)*sum_over_ell(ell, theta)*np.cos(np.deg2rad(theta))

#Saving results in an array

OMEGA = []

for th in np.linspace(0.05, 2.00, 20):

    w = omega(ell, th)
    
    OMEGA = np.append(OMEGA, w)

#Importing TREECORR RESULTS to compare

data = np.loadtxt('/scratch/davsan06/CMB-TREECORR/ACF_CMB_TREECORR.out',dtype=float)

theta_tree = data[0]
xi_tree = data[1]

#Ploting comparison COSMOSIS vs. TREECORR

#Sumando hasta l = l_max

plt.figure()
plt.plot(np.linspace(0.05, 2.00, 20), np.linspace(0.05, 2.00, 20)*OMEGA, marker = 'x',
label='COSMOSIS')

plt.plot(theta_tree, theta_tree*xi_tree*10**(12), marker='o', label = 'TREECORR')

plt.legend()

plt.savefig('ACF-CMB-COMPARISON-lmax={}'.format(l_max))



























