#!/scratch3/NCEPDEV/climate/rg/env3.13/bin/python3
'''
Scan SFS MOM6 output for points with sst colder than -1.92 and print out column
  information (u,v,t,s)
Robert Grumbine 20 February 2026
'''
import sys

import numpy as np
from numpy import ma
import netCDF4
#---------------------------------------------------------
def allwet(x, i, j):
    tmp = x[j,i] > -1.e30
    tmp = tmp and (x[j,i+1] > -1.e30)
    tmp = tmp and (x[j,i-1] > -1.e30)
    tmp = tmp and (x[min(j+1,1079),i] > -1.e30)
    tmp = tmp and (x[j-1,i] > -1.e30)
    return tmp

#---------------------------------------------------------
parm2_names = [ 'LW', 'MLD_003', 'MLD_0125', 'SSH', 'SST', 'SSU', 'SSV', \
                'SW', 'ePBL', 'latent', 'sensible', 'taux', 'tauy' ]
parm3_names = [ 'temp', 'uo', 'vo', 'so' ]

fname = sys.argv[1] # all parms in same file
tmp = netCDF4.Dataset(fname)

nx = 1440
ny = 1080
parm2 = np.zeros((len(parm2_names),1,ny,nx))

i = 0
for p in parm2_names:
    print(p,flush=True)
    tmp = netCDF4.Dataset(fname)
    parm2[i] = tmp.variables[p][:,:,:]
    if i == 0:
        lats = tmp.variables['geolat'][:,:]
        lons = tmp.variables['geolon'][:,:]
    print(parm2[i].max(), (parm2[i])[parm2[i] > -1.e30].min() )
    i += 1

sst = parm2_names.index('SST')
print("sst index = ",sst)
mask = ma.masked_array(parm2[sst] > -1.e30)
mask = ma.logical_and(mask, parm2[sst] < -1.92)
print('points below -1.92 ',mask.sum() )

parm3 = np.zeros((len(parm3_names),1,30,ny,nx))
i = 0
for p in parm3_names:
    print(p,flush=True)
    if i == 0:
        zl = tmp.variables['z_l'][:]
        #debug: print('zl ',len(zl),zl, flush=True)
    parm3[i] = tmp.variables[p][:,:,:,:]
    print(parm3[i].max(), (parm3[i])[parm3[i] > -1.e30].min() )
    i += 1

tmp.close()

for p in range(0,len(parm3_names)):
  for j in range(0,ny):
    for i in range(0,nx):
      if (mask[0,j,i]):
        for z in range(0,30):
          if (parm3[p][0,z,j,i] > -1.e30):
            print(z,j,i,parm3_names[p],parm3[p][0,z,j,i],parm2[sst][0,j,i], \
                      lats[j,i], lons[j,i], zl[z], allwet(parm3[p][0,z],i,j) )
