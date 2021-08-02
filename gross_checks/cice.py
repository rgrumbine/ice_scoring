import os
import sys
import datetime
from math import *
#print("importing external modules",flush=True)

import numpy as np
import numpy.ma as ma
#print("imported numpy",flush=True)

import netCDF4
#print("Finished importing external modules",flush=True)

import bounders
#print("Finished importing private  modules",flush=True)

#---------------------------------------------------
# new management of header variable names
headers = {
  'nx' : '',
  'ny' : '',
  'TLON' : '',
  'TLAT' : '',
  'tmask' : '',
  'tarea' : ''
}
fin = open('ctl/cice.header','r')
k = 0
for line in fin:
  #print(k, len(line))
  if (len(line) < 3):
      #print("zero length line",flush=True)
      break
  words = line.split()
  #print(k, words[0])
  headers[words[0]] = words[1]
  k += 1

#print(headers)

#---------------------------------------------------
#Gross bound checks on .nc files, developed primarily from the sea ice (CICE6) output
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
  model = netCDF4.Dataset(sys.argv[1], 'r')
  nx = len(model.dimensions[headers['nx']])
  ny = len(model.dimensions[headers['ny']])
  
  #rg q: is this universal across UFS? -- no.
  tlons = model.variables[headers["TLON"]][:,:]
  tlats = model.variables[headers["TLAT"]][:,:]
  
  #LAND = 0, #Ocean = 1
  try:
    tmask = model.variables[headers["tmask"]][:,:]
  except :
    tmask = np.zeros((ny, nx))
    tmask = 1.
  tarea = model.variables[headers["tarea"]][:,:]

  #Get the dictionary file, perhaps with bounds given
  try:
    fdic = open(sys.argv[2])
  except:
    print("could not find a dictionary file ",sys.argv[2])
    exit(1)

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
print("errcount = ",errcount)
if (errcount == 0):
  exit(0)
else:
  exit(1)
