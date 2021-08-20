# -*- coding: utf-8 -*-
"""
@author: Adam Wickenheiser
"""

# Note: to run this file, you must place the beammech.py file in the same folder as this file

import numpy as np
import matplotlib.pyplot as plt
import beammech as bm

# material properties
E = 190000      # elastic modulus [MPa]
G = 73100       # shear modulus [MPa]

# beam geometry
L = np.round(1016)                 # length of beam [mm]
h = np.round(0.75*304.8)               # height of beam [mm]
t = np.round(0.25*304.8)               # thickness of beam [mm]

x = np.arange(L+1)                     # positions to evaluate along beam [mm]
I = np.full_like(x,t*h**3/12)          # second moment of area [mm^4]
A = np.full_like(x,t*h)                # area [mm^2]
top = np.full_like(x,h/2)              # height of top surface
bot = np.full_like(x,-h/2)             # height of bottom surface

# external loads
load1 = bm.Load(force=-8006.799, pos=0*304.8)    # force [N] and location [mm]
load2 = bm.Load(force=-0, pos=14*304.8)   # force [N] and location [mm]
load3 = bm.DistLoad(force=-40033.99, start=254, end=1016) # force [N] and start and end locations [mm]

x_sup = np.round(np.array([254, 1016]))       # location of pinned supports [mm]


# assemble everything into beam object
beam = {}
beam['length'] = int(L)
beam['loads'] = [load1, load2, load3]
beam['supports'] = (int(x_sup[0]), int(x_sup[1]))
beam['EI'] = E*I
beam['GA'] = G*A
beam['top'] = top
beam['bot'] = bot


# solve for beam deflection in xy plane
bm.solve(beam)
Ry = np.asarray([R.size for R in beam['R']])
print('Reaction forces in y-direction:',Ry/4.448,'lb')

Vy = beam['D']/4448            # internal shear force [kip]
plt.figure()
plt.plot(x/304.8,Vy)
plt.ylabel('Internal shear force (xy plane) [kip]')
plt.xlabel('Position [ft]')

Mz = beam['M']/4448/304.8       # internal bending moment [kip-ft]
plt.figure()
plt.plot(x/304.8,Mz)
plt.ylabel('Internal bending moment (xy plane) [kip-ft]')
plt.xlabel('Position [ft]')