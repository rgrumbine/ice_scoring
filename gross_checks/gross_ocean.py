import os
import sys
import datetime
from math import *
import numpy as np
import numpy.ma as ma

import netCDF4

#---------------------------------------------------
#Gross bound checks on .nc files, developed primarily from the ocean (MOM6) output
#Robert Grumbine
#30 January 2020
#
#data file = argv[1] (input)
#control dictionary = argv[2] (input)
#bootstrapped dictionary = argv[3] (optional, may be written to if needed and present)

#---------------------------------------------------
import bounders

errcount = int(0)

if (not os.path.exists(sys.argv[1]) ):
  print("failure to find ",sys.argv[1])
  exit(1)
else:
# in ice:   ni, nj, TLON,   TLAT,   tmask (1 = ocean, 0 = land), tarea
# in ocean: xh, yh, geolon, geolat, ???,          no cellarea parm 
  model = netCDF4.Dataset(sys.argv[1], 'r')
  #rg q: is this universal across UFS? -- no. 
  #for MOM6
  nx = len(model.dimensions['xh'])
  ny = len(model.dimensions['yh'])
  tlons = model.variables["geolon"][:,:]
  tlats = model.variables["geolat"][:,:]

  try:
    tmask = model.variables["tmask"][:,:]
  except :
    tmask = np.zeros((ny, nx))
    tmask = 1.
  try:
    tarea = model.variables["tarea"][:,:]
  except : 
    tarea = np.zeros((ny, nx))
    tarea = 1.

  try:
    fdic = open(sys.argv[2])
  except:
    print("could not find a dictionary file ",sys.argv[2])
    exit(1)

  #for bootstrapping -- read in dictionary of names, write back out name/max/min 
  try: 
    flying_dictionary = open(sys.argv[3],"w")
    flyout = True
  except:
    #debug print("cannot write out to bootstrap dictionary file")
    flyout = False

  parmno = 0
  for line in fdic:
    words = line.split()
    parm = words[0]
    tmp = bounders.bounds(param=parm)
    try: 
      temporary_grid = model.variables[parm][0,:,:]
    except:
      print(parm," not in data file")
      continue

    # find or bootstrap bounds -----------------
    tmp.set_bounds(temporary_grid, words, flyout, flying_dictionary)

    #Global tests -- test whether the test fails anywhere
    gfail = tmp.whether(temporary_grid)

    #Pointwise checks -- Show where (and which) test failed:
    if (gfail):
      errcount += tmp.where(temporary_grid, tlats, tlons, tmask, tarea)

    parmno += 1

#exit codes are bounded, while error counts are not
if (errcount > 0):
  print("errcount = ",errcount)
  exit(1)
if (errcount == 0):
  exit(0)
