#!/scratch3/NCEPDEV/climate/rg/env3.13/bin/python3
'''
Scan SFS MOM6 output for points with sst colder than -1.92 and print out column
  information (u,v,t,s)
Robert Grumbine 20 February 2026
'''
import sys
import copy

import netCDF4
#---------------------------------------------------------
def allwet(x, fi, fj):
    ''' allwet True if all i,j +- 1 points are unflagged '''
    ftmp = x[fj,fi] > -1.e30
    ftmp = ftmp and (x[fj,min(1439,fi+1)] > -1.e30)
    ftmp = ftmp and (x[fj,fi-1] > -1.e30)
    ftmp = ftmp and (x[min(fj+1,1079),fi] > -1.e30)
    ftmp = ftmp and (x[fj-1,fi] > -1.e30)
    return ftmp

#---------------------------------------------------------
parm2_names = [ 'LW', 'MLD_003', 'MLD_0125', 'SSH', 'SST', 'SSU', 'SSV', \
                'SW', 'ePBL', 'latent', 'sensible', 'taux', 'tauy' ]
parm3_names = [ 'temp', 'uo', 'vo', 'so' ]

fname = sys.argv[1] # all parms in same file
tmp  = netCDF4.Dataset(fname)
nx   = 1440
ny   = 1080
lats = tmp.variables['geolat'][:,:]
lons = tmp.variables['geolon'][:,:]
zl   = tmp.variables['z_l'][:]
zi   = tmp.variables['z_i'][:]
zt = zi[1:] - zi[0:-1]
#debug: print("zl\n",zl)
#debug: print("zi\n",zi,flush=True)
#debug: print("zt\n",zt,flush=True)

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

delta = copy.deepcopy(salt1)
delta -= salt2
#debug: print("salt1 ",salt1.max(), salt1.min() )
#debug: print("salt2 ",salt2.max(), salt2.min() )
#debug: print("delta ",delta.max(), delta.min(), flush=True )

count = 0
for j in range(0,ny):
  #debug: print("j = ",j, flush=True)
  for i in range(0,nx):
    if (-40 < lats[j,i] < 40):
        continue
    if (any(abs(delta[0,:,j,i]) > 0.5e+2) or any(temp1[0,:,j,i] < -1.92) ):
      count += 1
      integral = 0.0
      print("",flush=True)
      for z in range(0,30):
        if (salt1[0,z,j,i] > -1.e30):
          integral += zt[z]*delta[0,z,j,i]
          print(f"{z:2d}",f"{j:4d}",f"{i:4d}", \
                f"{salt1[0,z,j,i]:.5f}", f"{salt2[0,z,j,i]:.5f}", f"{delta[0,z,j,i]:8.5f}", \
                f"{uo1[0,z,j,i]:6.3f}", f"{vo1[0,z,j,i]:6.3f}", \
                f"{uo2[0,z,j,i]:6.3f}", f"{vo2[0,z,j,i]:6.3f}", \
                f"{temp1[0,z,j,i]:6.3f}", f"{temp2[0,z,j,i]:6.3f}", \
                f"{lats[j,i]:7.3f}", f"{lons[j,i]:8.3f}", zl[z], allwet(salt1[0,z],i,j) )
      print("integral change ",integral)

print(count,"points found with large salinity changes in the water column")
