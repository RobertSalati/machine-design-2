# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:56:50 2021

@author: Adam Wickenheiser
"""

import numpy as np

# stress components at the given point [kpsi]
sigma_x = 83.9
sigma_y = 0
sigma_z = 0
tau_xy = 0
tau_xz = 0
tau_yz = 0

S_y = 490          # yield strength [kpsi]
S_t = 45          # yield strength in tension [kpsi]
S_c = 45          # yield strength in compression [kpsi]

sigma = np.array([[sigma_x, tau_xy, tau_xz],
                  [tau_xy, sigma_y, tau_yz],
                  [tau_xz, tau_yz, sigma_z]])   # stress tensor
principal_stresses = np.linalg.eigh(sigma)[0]   # outputs eigenvalues in ascending order

# reverse order for principal stresses
sigma_1 = principal_stresses[2]
sigma_2 = principal_stresses[1]
sigma_3 = principal_stresses[0]

print('Principal stresses:',principal_stresses)

# MSS test
max_stress = sigma_1 - sigma_3
if max_stress >= S_y:
    print('MSS theory predicts failure')
else:
    n = S_y/max_stress
    print('MSS factor of safety = ',n)
    
# DE test
von_Mises_stress = np.sqrt(((sigma_1-sigma_2)**2+(sigma_2-sigma_3)**2+(sigma_3-sigma_1)**2)/2)
if von_Mises_stress >= S_y:
    print('DE theory predicts failure')
else:
    n = S_y/von_Mises_stress
    print('DE factor of safety = ',n)
    
# DCM test
DCM_criterion = sigma_1/S_t - sigma_3/S_c
if DCM_criterion >= 1:
    print('DCM theory predicts failure')
else:
    n = 1/DCM_criterion
    print('DCM factor of safety = ',n)