import os
import numpy as np
import matplotlib.pyplot as plt
import sys
import importlib
from numpy import random

sys.path.append('/scratch2/NCEPDEV/marine/Dmitry.Dukhovskoy/python/MyPython')
sys.path.append('/scratch2/NCEPDEV/marine/Dmitry.Dukhovskoy/python/MyPython/draw_map')

from mod_misc1 import dist_sphcrd as dstgeo
from mod_utils_fig import bottom_text

import mod_hausdorff_distance as mhsdrf
importlib.reload(mhsdrf)

plt.ion()

#P  = np.array([[0,1],[1,1],[1.5,0.4],[1,0],[0.65,-0.4]])
#Q  = np.array([[0,1],[1,1.2],[1.5,0.5],[1,0],[0.8,0.75],[0.67,-0.41]])

flnm = 'shape1.dat'
P = []
with open(flnm, 'r') as finp:
  for line in finp:
    if line:
      line = line.strip()
      dmm = [float(x) for x in line.split(maxsplit=2)]
      P.append(dmm)

P = np.array(P)
d1 = P.shape[0]
d2 = P.shape[1]

f_geo = True


# Test identical lines:
mhd0 = mhsdrf.modifHD(P,P)

# Add random noise to the original shape and 
# compare the contours
Anoise = 0.02
MHD    = []
MHDg   = []
iaE    = 10
for ia in range(iaE):
  RR = random.rand(d1,d2)-0.5
  if ia == 0:
    Q = P
  else:
    Q = P+RR*Anoise*float(ia) 

  mhd1 = mhsdrf.modifHD(P,Q)
  print('Anoise={0:8.4f}  mhd={1:8.4f}'.format(Anoise*float(ia),mhd1))
  MHD.append(mhd1)

# Test geograph. coordinate:
  if f_geo:
# Create geogr coordinates to test spherical distances
# Geogr coord:
    lon0 = 176.1
    lat0 = 80.2
    Pg = P.copy()
    Qg = Q.copy()
    Pg[:,0] = P[:,0]+lon0
    Pg[:,1] = P[:,1]+lat0
    Qg[:,0] = Q[:,0]+lon0
    Qg[:,1] = Q[:,1]+lat0
    mhd2 = mhsdrf.modifHD(Pg,Qg,geo2cart=True)
    MHDg.append(mhd2)


plt.figure(1, figsize=(7,7))
plt.clf()
plt.plot(P[:,0],P[:,1],'.-')
plt.plot(Q[:,0],Q[:,1],'.-')
stl = 'Anoise={0:8.4f}  mhd={1:8.4f}'.format(Anoise*float(ia),mhd1)
plt.title(stl)

plt.figure(2, figsize=(9,7))
plt.clf()
ax1 = plt.axes([0.1, 0.5, 0.8, 0.3])
plt.plot(MHD,'.-')
ax1.set_xticks(np.arange(0,iaE))
ax1.grid(True)
plt.title('MHD score for shape 1 with added random noise')

ax2 = plt.axes([0.1, 0.1, 0.8, 0.3])
Ans = Anoise*np.array(list(range(iaE)))
ax2.plot(Ans,'.-')
ax2.set_xticks(np.arange(0,iaE))
ax2.grid(True)
ax2.set_title('Noise amplitude')

btx = 'test.py'
bottom_text(btx)

if f_geo:
  plt.figure(3, figsize=(9,7))
  plt.clf()
  ax3 = plt.axes([0.1, 0.5, 0.8, 0.3])
  plt.plot(MHDg,'.-')
  ax3.set_xticks(np.arange(0,iaE))
  ax3.grid(True)
  plt.title('MHD GeogrCoord for shape 1 with added random noise')

