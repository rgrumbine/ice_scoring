'''
Check speeds from dataset with u,v components
Robert Grumbine
'''
import sys
import numpy as np
import netCDF4 as nc

ny = 3298
nx = 4500
u = np.zeros((ny,nx))
v = np.zeros((ny,nx))
sst = np.zeros((ny,nx))

model = nc.Dataset(sys.argv[1],'r')
u[:,:] = model.variables['u_velocity'][0,:,:]
v[:,:] = model.variables['v_velocity'][0,:,:]
sst[:,:] = model.variables['sst'][0,:,:]
lats = model.variables['Latitude'][:,:]
lons = model.variables['Longitude'][:,:]
print(u.shape, v.shape, lats.shape, lons.shape)

tmp1  = u
tmp1 *= u
tmp2  = v
tmp2 *= v

speed = tmp1
speed += tmp2
print(tmp1.shape, tmp2.shape, speed.shape)
speed = np.sqrt(speed)
print("speed max min",speed.max(), speed.min(), speed.shape )

count = 0
for j in range(0,ny):
  for i in range(0, nx):
    #print(i,j,lons[j][i], lats[j][i],end="")
    if (speed[j][i] < 0.002):
      count += 1
      if (lons[j][i] > 360.):
          while lons[j][i] > 360. :
              lons[j][i] -= 360.
      print(i,j, lons[j][i], lats[j][i], 'pm', speed[j][i], sst[j][i] )

print(count, " low speed points")
