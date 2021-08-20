# -*- coding: utf-8 -*-
"""
@author: Adam Wickenheiser

Uses beammech library:
https://github.com/rsmith-nl/beammech
"""

import numpy as np
import matplotlib.pyplot as plt
import beammech as bm

# material properties (Table A-5)
E = 207000      # elastic modulus [MPa]
G = 79300       # shear modulus [MPa]

# shaft geometry
D_array = np.array([90,95,72,35])            # diameters [mm]
D_locs = np.round(np.array([3.0, 9.0, 11.0, 11.0])*25.4)      # locations of diameter change [mm]
x_sup = np.round(np.array([0.0, 11.0])*25.4)                 # location of pinned supports (bearings) [mm]
x_gear = np.round(np.array([3.0, 9.0])*25.4)               # location of gears [mm]


F23 = 1330*4.448       # gear 3 force [N]
F45 = 3326*4.448       # gear 4 force [N]
# y loads

load1y = bm.Load(force=F23*np.cos(20*np.pi/180), pos=x_gear[1])   # force [N] and location [mm]
load2y = bm.Load(force=-F45*np.sin(20*np.pi/180), pos=x_gear[0])   # force [N] and location [mm]

# z loads
load1z = bm.Load(force=-F23*np.sin(20*np.pi/180), pos=x_gear[1])   # force [N] and location [mm]
load2z = bm.Load(force=-F45*np.cos(20*np.pi/180), pos=x_gear[0])   # force [N] and location [mm]

# derived parameters
L = D_locs[-1]         # length of shaft [mm]
x = np.arange(L+1)
D = np.full_like(x,D_array[0])
I = np.full_like(x,np.pi*D_array[0]**4/64)
A = np.full_like(x,np.pi*D_array[0]**2/4)
for i in range(1,D_array.size):
    D[(x > D_locs[i-1]) & (x <= D_locs[i])] = D_array[i]
    I[(x > D_locs[i-1]) & (x <= D_locs[i])] = np.pi*D_array[i]**4/64
    A[(x > D_locs[i-1]) & (x <= D_locs[i])] = np.pi*D_array[i]**2/4
plt.figure(figsize=(12,10))
plt.plot(x/25.4,D/25.4)
plt.gca().tick_params(labelsize=16)
plt.ylabel('Diameter [in]',fontsize=24)
plt.xlabel('Position [in]',fontsize=24)
beam = {}
beam['length'] = int(L)
beam['supports'] = (int(x_sup[0]), int(x_sup[1]))
beam['EI'] = E*I
beam['GA'] = G*A
beam['top'] = D/2
beam['bot'] = -D/2

# solve for beam deflection in xy plane
beam['loads'] = [load1y]
bm.solve(beam)
Ry = np.asarray([R.size for R in beam['R']])
print('Reaction forces in y-direction:',Ry/4.448,'lb')

Vy = beam['D']/4.448            # internal shear force [lb]
plt.figure(figsize=(12,10))
plt.plot(x/25.4,Vy)
plt.gca().tick_params(labelsize=16)
plt.ylabel('Internal shear force (xy plane) [lb]',fontsize=24)
plt.xlabel('Position [in]',fontsize=24)

Mz = beam['M']/4.448/25.4       # internal bending moment [lb-in]
plt.figure(figsize=(12,10))
plt.plot(x/25.4,Mz)
plt.gca().tick_params(labelsize=16)
plt.ylabel('Internal bending moment (xy plane) [lb-in]',fontsize=24)
plt.xlabel('Position [in]',fontsize=24)

theta_y = beam['a']   # slope [rad]
print('Slope at supports (xy plane):',theta_y[x==x_sup[0]],theta_y[x==x_sup[1]],'rad')
print('Slope at gears (xy plane):',theta_y[x==x_gear[0]],theta_y[x==x_gear[1]],'rad')

y = beam['y']/25.4              # deflection [in]
print('Deflection at gears (xy plane):',y[x==x_gear[0]],y[x==x_gear[1]],'in')

# solve for beam deflection in xy plane
beam['loads'] = [load1z, load2z]
bm.solve(beam)
Rz = np.asarray([R.size for R in beam['R']])
print('Reaction forces in z-direction:',Rz/4.448,'lb')

Vz = beam['D']/4.448            # internal shear force [lb]
plt.figure(figsize=(12,10))
plt.plot(x/25.4,Vz)
plt.gca().tick_params(labelsize=16)
plt.ylabel('Internal shear force (xz plane) [lb]',fontsize=24)
plt.xlabel('Position [in]',fontsize=24)

My = beam['M']/4.448/25.4       # internal bending moment [lb-in]
plt.figure(figsize=(12,10))
plt.plot(x/25.4,My)
plt.gca().tick_params(labelsize=16)
plt.ylabel('Internal bending moment (xz plane) [lb-in]',fontsize=24)
plt.xlabel('Position [in]',fontsize=24)

theta_z = beam['a']   # slope [rad]
print('Slope at supports (xz plane):',theta_z[x==x_sup[0]],theta_z[x==x_sup[1]],'rad')
print('Slope at gears (xz plane):',theta_z[x==x_gear[0]],theta_z[x==x_gear[1]],'rad')

z = beam['y']/25.4              # deflection [in]
print('Deflection at gears (xz plane):',z[x==x_gear[0]],z[x==x_gear[1]],'in')