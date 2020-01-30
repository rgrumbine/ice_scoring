import os
import sys
import datetime
from math import *
import numpy as np

import netCDF4

#import urllib
#import csv

#---------------------------------------------------
#Gross bound checks on .nc files, developed primarily from the sea ice (CICE5) output
#Robert Grumbine
#30 January 2020
#
#data file = argv[1] (input)
#control dictionary = argv[2] (input)
#bootstrapped dictionary = argv[3] (optional, may be written to if needed and present)


#---------------------------------------------------

if (not os.path.exists(sys.argv[1]) ):
  print("failure to find ",sys.argv[1])
  exit(1)
else:
# in ice:   ni, nj, TLON,   TLAT,   tmask (1 = ocean, 0 = land), tarea
# in ocean: xh, yh, geolon, geolat, ???,                         no cellarea parm 
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

  #bootstrapping -- read in dictionary of names, write back out name/max/min in dictionary format
  #  next round -- estimate minmax and maxmin by 1% end points of histogram
  # want to specify T pts vs. U pts
  fdic = open(sys.argv[2])
  try: 
    flying_dictionary = open(sys.argv[3],"w")
    flyout = True
  except:
    print("cannot write out to bootstrap dictionary file")
    flyout = False

  k = 0
  for line in fdic:
    words = line.split()
    parm = words[0]
    try: 
      temporary_grid = model.variables[parm][0,:,:]
    except:
      print(parm," not in data file")
      continue

    # Bootstrap the bounds if needed -------------------
    if (len(words) >= 3):
      pmin = float(words[1])
      pmax = float(words[2])
    else:
      pmin = temporary_grid.min()
      pmax = temporary_grid.max()
      #do the multiplier to avoid roundoff issues with printout values
      if (pmin < 0):
         pmin *= 1.001
      else:
         pmin *= 0.999
      if (pmax < 0):
         pmax *= 0.999
      else:
         pmax *= 1.001
  
    if (len(words) >= 5):
      pmaxmin = float(words[3])
      pminmax = float(words[4])
    else:
      pmaxmin = pmin + 0.1*(pmax - pmin)
      pminmax = pmax - 0.1*(pmax - pmin)

    #print("k = ",k,parm, pmin, pmax, pmaxmin, pminmax)
    #RG: need to do something different in formatting small numbers (fsalt, for ex)
    if (len(words) < 5 and flyout) :
      print("{:10s}".format(parm), 
        "{:.5f}".format(pmin),      
        "{:.5f}".format(pmax),
        "{:.5f}".format(pmaxmin),
        "{:.5f}".format(pminmax),
        file=flying_dictionary)
    if (len(words) < 5 and not flyout) : #if no flying dictionary file, write to stdout
      print("bootstrap ","{:10s}".format(parm), 
        "{:.5f}".format(pmin),      
        "{:.5f}".format(pmax),
        "{:.5f}".format(pmaxmin),
        "{:.5f}".format(pminmax) )
    # End finding or bootstrapping bounds -----------------

    #apply the tests
    gmin = temporary_grid.min()
    gmax = temporary_grid.max()
    gfail = False
    if (gmin < pmin):
      print("{:10s}".format(parm)," excessively low minimum ",gmin," versus ",pmin," allowed")
      gfail = True
    if (gmin > pmaxmin):
      print("{:10s}".format(parm)," excessively high minimum ",gmin," versus ",pmaxmin," allowed")
      gfail = True
    if (gmax > pmax):
      print("{:10s}".format(parm)," excessively high maximum ",gmax," versus ",pmax," allowed")
      gfail = True
    if (gmax < pminmax ):
      print("{:10s}".format(parm)," excessively low maximum ",gmax," versus ",pminmax," allowed")
      gfail = True

    #Show where (and which) test failed:
    #where(tmp, tlons, tlats, pmin, pmaxmin, pmax, pminmax)
    if (gfail):
      print("parameter i j longitude latitude model_value test_checked test_value")
      for j in range (0,ny):
        for i in range (0,nx):
          if (temporary_grid[j,i] < pmin):
            print(parm,i,j,tlons[j,i], tlats[j,i], temporary_grid[j,i], " vs pmin ",pmin)
          if (temporary_grid[j,i] > pmax):
            print(parm,i,j,tlons[j,i], tlats[j,i], temporary_grid[j,i], " vs pmax ",pmax)


  

    k += 1
