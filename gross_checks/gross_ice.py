import os
import sys
import datetime
from math import *
import numpy as np

import urllib
import csv
import netCDF4

#---------------------------------------------------
#data file = argv[1]
#control dictionary = argv[2]

if (not os.path.exists(sys.argv[1]) ):
  print("failure to find ",sys.argv[1])
  exit(1)
else:
  model = netCDF4.Dataset(sys.argv[1], 'r')
  nx = len(model.dimensions['ni'])
  ny = len(model.dimensions['nj'])
  #print("nx, ny = ",nx," ",ny)
  #rg q: is this universal across UFS?
  tlons = model.variables["TLON"][:,:]
  tlats = model.variables["TLAT"][:,:]
  #print("max, min lons lats masks ",tlons.max(), tlons.min(), tlats.max(), tlats.min() )
  #LAND = 0, #Ocean = 1
  try:
    tmask = model.variables["tmask"][:,:]
  except :
    tmask = np.zeros((ny, nx))
    tmask = 1.
  tarea = model.variables["tarea"][:,:]
  #print("max min mask area ",tmask.max(), tmask.min(), tarea.max(), tarea.min(), sqrt(tarea.max()), sqrt(tarea.min() )  )

  #bootstrapping -- read in dictionary of names, write back out name/max/min in dictionary format
  #  next round -- estimate minmax and maxmin by 1% end points of histogram
  # want to specify T pts vs. U pts
  fdic = open(sys.argv[2])
  flying_dictionary = open(sys.argv[3],"w")
  k = 0
  for line in fdic:
    words = line.split()
    parm = words[0]
    try: 
      temporary_grid = model.variables[parm][0,:,:]
    except:
      print(parm," not in data file")
      continue

    if (len(words) >= 3):
      pmin = float(words[1])
      pmax = float(words[2])
    else:
      pmin = temporary_grid.min()
      pmax = temporary_grid.max()
      #do the multiplier to avoid roundoff issues
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
    if (len(words) < 5) :
      print("{:10s}".format(parm), 
        "{:.5f}".format(pmin),      
        "{:.5f}".format(pmax),
        "{:.5f}".format(pmaxmin),
        "{:.5f}".format(pminmax),
        file=flying_dictionary)

    #apply the tests
    gmin = temporary_grid.min()
    gmax = temporary_grid.max()
    if (gmin < pmin):
      print("{:10s}".format(parm)," excessively low minimum ",gmin," versus ",pmin," allowed")
    if (gmin > pmaxmin):
      print("{:10s}".format(parm)," excessively high minimum ",gmin," versus ",pmaxmin," allowed")
    if (gmax > pmax):
      print("{:10s}".format(parm)," excessively high maximum ",gmax," versus ",pmax," allowed")
    if (gmax < pminmax ):
      print("{:10s}".format(parm)," excessively low maximum ",gmax," versus ",pminmax," allowed")
  

    k += 1

  
  #ice thick:  [0..5+], max should be > 1.5m arctic, > 1 antarctic
  #ice speed:  [0..0.7],  rough -- Nansen rule equates 0.7 m/s ice motion to winds of 35 m/s 
  #ice conc: [0..1]
