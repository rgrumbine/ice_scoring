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

errcount = int(0)

if (not os.path.exists(sys.argv[1]) ):
  print("failure to find ",sys.argv[1])
  exit(1)
else:
# in ice:   ni, nj, TLON,   TLAT,   tmask (1 = ocean, 0 = land), tarea
# in ocean: xh, yh, geolon, geolat, ???,          no cellarea parm 
  model = netCDF4.Dataset(sys.argv[1], 'r')
  #rg q: is this universal across UFS? -- no. 
  #for CICE:
  #nx = len(model.dimensions['ni'])
  #ny = len(model.dimensions['nj'])
  #tlons = model.variables["TLON"][:,:]
  #tlats = model.variables["TLAT"][:,:]
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

  #bootstrapping -- read in dictionary of names, write back out name/max/min 
  #    in dictionary format 
  #  next round -- estimate minmax and maxmin by 1% end points of histogram 
  #  want to specify T pts vs. U pts
  fdic = open(sys.argv[2])
  try: 
    flying_dictionary = open(sys.argv[3],"w")
    flyout = True
  except:
    print("cannot write out to bootstrap dictionary file")
    flyout = False

  parmno = 0
  for line in fdic:
    words = line.split()
    parm = words[0]
    tmp = bounds(param=parm)
    try: 
      temporary_grid = model.variables[parm][0,:,:]
    except:
      print(parm," not in data file")
      continue

    # Bootstrap the bounds if needed -------------------
    if (len(words) >= 3):
      tmp.pmin = float(words[1])
      tmp.pmax = float(words[2])
    else:
      tmp.findbounds(temporary_grid)
  
    if (len(words) >= 5):
      tmp.pmaxmin = float(words[3])
      tmp.pminmax = float(words[4])
    else:
      tmp.findbounds(temporary_grid)

    #debug: tmp.show()
    if (len(words) < 5 and flyout) :
      tmp.show(flyout)
    elif (len(words) < 5 and not flyout) : 
      tmp.show(sys.stdout)
    # End finding or bootstrapping bounds -----------------

    #Global tests:
    gmin = temporary_grid.min()
    gmax = temporary_grid.max()
    gfail = False
    if (gmin < tmp.pmin):
      print("{:10s}".format(parm)," excessively low minimum ",gmin," versus ",tmp.pmin," allowed")
      gfail = True
    if (gmin > tmp.pmaxmin):
      print("{:10s}".format(parm)," excessively high minimum ",gmin," versus ",tmp.pmaxmin," allowed")
      gfail = True
    if (gmax > tmp.pmax):
      print("{:10s}".format(parm)," excessively high maximum ",gmax," versus ",tmp.pmax," allowed")
      gfail = True
    if (gmax < tmp.pminmax ):
      print("{:10s}".format(parm)," excessively low maximum ",gmax," versus ",tmp.pminmax," allowed")
      gfail = True

    #Pointwise checks -- Show where (and which) test failed:
    #  numpy masked arrays are vastly more efficient than manual iteration over indices
    #  0.5 seconds for masked arrays, 5 minutes for manual
    #where(tmp, tlons, tlats, pmin, pmax)
    if (gfail):
      maskhigh = ma.masked_array(temporary_grid > tmp.pmax)
      high = maskhigh.nonzero()
      #debug print("len(high): ", len(high[0]),len(high) )
      errcount += len(high[0])

      masklow  = ma.masked_array(temporary_grid < tmp.pmin)
      low  = masklow.nonzero()
      #debug print("len(low): ", len(low[0]),len(low) )
      errcount += len(low[0])

      print("parameter i j longitude latitude model_value test_checked test_value")
      for k in range (0,len(high[0])):
        i = high[1][k]
        j = high[0][k]
        print(parm,i,j,tlons[j,i], tlats[j,i], temporary_grid[j,i], " vs pmax ",tmp.pmax)

      for k in range (0,len(low[0])):
        i = low[1][k]
        j = low[0][k]
        print(parm,i,j,tlons[j,i], tlats[j,i], temporary_grid[j,i], " vs pmin ",tmp.pmin)

    parmno += 1

#exit codes are bounded, while error counts are not
print("errcount = ",errcount)
if (errcount == 0):
  exit(0)
else:
  exit(1)
