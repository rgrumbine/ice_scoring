#!/scratch3/NCEPDEV/climate/rg/env3.13/bin/python3
'''
Scan SFS MOM6 output for points with sst colder than -1.92 and print out column
  information (u,v,t,s)
Robert Grumbine 20 February 2026
'''
import sys
import copy

import numpy as np
from numpy import ma
import netCDF4
#---------------------------------------------------------
def allwet(x, i, j):
    tmp = x[j,i] > -1.e30
    tmp = tmp and (x[j,min(i+1,1039)] > -1.e30)
    tmp = tmp and (x[j,i-1] > -1.e30)
    tmp = tmp and (x[min(j+1,1079),i] > -1.e30)
    tmp = tmp and (x[j-1,i] > -1.e30)
    return tmp

#---------------------------------------------------------
parm2_names = [ 'LW', 'MLD_003', 'MLD_0125', 'SSH', 'SST', 'SSU', 'SSV', \
                'SW', 'ePBL', 'latent', 'sensible', 'taux', 'tauy' ]
parm3_names = [ 'temp', 'uo', 'vo', 'so' ]

fname = sys.argv[1] # all parms in same file
tmp  = netCDF4.Dataset(fname)
lats = tmp.variables['geolat'][:,:]
lons = tmp.variables['geolon'][:,:]
zl   = tmp.variables['z_l'][:]

fname2 = sys.argv[2]
tmp2   = netCDF4.Dataset(fname2)

salt1 = tmp.variables['so'][:,:,:,:]
temp1 = tmp.variables['temp'][:,:,:,:]
uo1   = tmp.variables['uo'][:,:,:,:]
vo1   = tmp.variables['vo'][:,:,:,:]

salt2 = tmp2.variables['so'][:,:,:,:]
temp2 = tmp2.variables['temp'][:,:,:,:]
uo2   = tmp2.variables['uo'][:,:,:,:]
vo2   = tmp2.variables['vo'][:,:,:,:]

delta = copy.deepcopy(temp1)
delta -= temp2

count = 0
for j in range(0,1080):
  #debug: print("j = ",j, flush=True)
  for i in range(0,1440):
    if (-40 < lats[j,i] < 40):
        continue
    if (any(abs(delta[0,:,j,i]) > 2.5e-0) ):
      count += 1
      print("".flush=True)
      for z in range(0,30):
        if (temp1[0,z,j,i] > -1.e30):
          print(f"{z:2d}",f"{j:4d}",f"{i:4d}", \
                f"{temp1[0,z,j,i]:5.2f}", f"{temp2[0,z,j,i]:5.2f}", f"{delta[0,z,j,i]:8.5f}", \
                uo1[0,z,j,i], vo1[0,z,j,i],
                f"{lats[j,i]:7.3f}", f"{lons[j,i]:8.3f}", zl[z], allwet(temp1[0,z],i,j) )

print(count,"points found with large temperature changes in the water column")
