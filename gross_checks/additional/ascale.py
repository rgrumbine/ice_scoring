import sys
import os
import copy
import numpy as np
import numpy.ma as ma
import netCDF4 as nc

#----------------------------------------------------------------
# Get model output file
if (not os.path.exists(sys.argv[1]) ):
  print("failure to find ",sys.argv[1])
  exit(1)
else:
  model = nc.Dataset(sys.argv[1], 'r')

#----------------------------------------------------------------
# Read in header definition file:
if (os.path.exists(os.environ['MODDEF']+'/'+sys.argv[2])):
  fin = open(os.environ['MODDEF']+'/'+sys.argv[2],'r')
else:
  print("could not open definition file ",os.environ['MODDEF']+'/'+sys.argv[2])
  exit(1)
headers = {
  'nx' : '',
  'ny' : '',
  'nz' : '',
  'TLON' : '',
  'TLAT' : '',
  'tarea' : '',
  'tmask' : '',
  'Depth' : ''
}
k = 0
for line in fin:
  words = line.split()
  if (len(line) < 3):
      print("zero length line",flush=True)
      break
  if (len(words) < 2):
      break
  headers[words[0]] = words[1]
  print(words[0] , words[1])
  k += 1
#----------------------------------------------------------------

model = nc.Dataset(sys.argv[1],'r')
nx = len(model.dimensions[headers['nx']])
ny = len(model.dimensions[headers['ny']])
lats = model.variables[headers['TLAT']][:,:]
lons = model.variables[headers['TLON']][:,:]

a = model.variables['aice_h'][0,:,:]
pname = sys.argv[3]
x = model.variables[pname][0,:,:]
unscale = x*a

xmax = float(sys.argv[4])
xmin = float(sys.argv[5])

print("Beginning check")
count = 0
for j in range(0,ny):
  for i in range(0, nx):
    #if (unscale[j,i] > xmax or unscale[j,i] < xmin):
    if (x[j,i] > xmax or x[j,i] < xmin):
      count += 1
      if (lons[j][i] > 360.):
          while lons[j][i] > 360. :
              lons[j][i] -= 360.
      print(i,j, lons[j][i], lats[j][i], 'pm',a[j,i], x[j,i], unscale[j,i])

