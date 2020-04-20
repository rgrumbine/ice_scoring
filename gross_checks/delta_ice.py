import os
import sys
import datetime
from math import *
import numpy as np

import netCDF4

#---------------------------------------------------
#Delta bound checks on .nc files, developed primarily from the sea ice (CICE5) output
#Robert Grumbine
#1 April 2020
#
#model file 1 = argv[1]
#model file 2 = argv[2]
#delta bounds = argv[3]
#ratio = argv[4] -- the bounds in arg3 are for 1 day changes. As the
#    forecast lead increases, acceptable differences do as well. This the
#    argument is for your control of that.

#---------------------------------------------------

if (not os.path.exists(sys.argv[1]) ):
  print("failure to find ",sys.argv[1])
  exit(1)
if (not os.path.exists(sys.argv[2]) ):
  print("failure to find ",sys.argv[2])
  exit(1)

model1 = netCDF4.Dataset(sys.argv[1], 'r')
model2 = netCDF4.Dataset(sys.argv[2], 'r')
nx = len(model1.dimensions['ni'])
ny = len(model1.dimensions['nj'])
tlons = model1.variables["TLON"][:,:]
tlats = model1.variables["TLAT"][:,:]
#LAND = 0, #Ocean = 1
try:
  tmask = model1.variables["tmask"][:,:]
except :
  tmask = np.zeros((ny, nx))
  tmask = 1.

tarea = model1.variables["tarea"][:,:]

fdic = open(sys.argv[3])
ratio = float(sys.argv[4])

k = 0
for line in fdic:
  words = line.split()
  parm = words[0]
  pmin = float(words[1])*ratio
  pmax = float(words[2])*ratio
  try: 
    tgrid1 = model1.variables[parm][0,:,:]
    tgrid2 = model2.variables[parm][0,:,:]
  except:
    print(parm," not in data file")
    continue

  delta = (tgrid1 - tgrid2)
  print("delta max min for parm {:10s}".format(parm), "{:.5e}".format(delta.max()), "{:.5e}".format(delta.min()) )
  print("tgrid1 max min for parm {:10s}".format(parm), "{:.5e}".format(tgrid1.max()), "{:.5e}".format(tgrid1.min()) )
  print("tgrid2 max min for parm {:10s}".format(parm), "{:.5e}".format(tgrid2.max()), "{:.5e}".format(tgrid2.min()) )
  sys.stdout.flush()

  if (delta.max() > pmax or delta.min() < pmin):
     print("parameter i j longitude latitude model_value test_checked test_value")
     for j in range (0,ny):
       sys.stdout.flush()
       for i in range (0,nx):
         if (delta[j,i] < pmin):
           print(parm,"{:4d}".format(i),"{:4d}".format(j),"{:7.3f}".format(tlons[j,i]), 
              "{:7.3f}".format(tlats[j,i]), delta[j,i], " vs pmin ",pmin, 
              "{:7.3f}".format(tgrid1[j,i]), 
              "{:7.3f}".format(tgrid2[j,i]) )
         if (delta[j,i] > pmax):
           print(parm,"{:4d}".format(i),"{:4d}".format(j),"{:7.3f}".format(tlons[j,i]), 
              "{:7.3f}".format(tlats[j,i]), delta[j,i], " vs pmax ",pmax, 
              "{:7.3f}".format(tgrid1[j,i]), 
              "{:7.3f}".format(tgrid2[j,i]) )

  k += 1
