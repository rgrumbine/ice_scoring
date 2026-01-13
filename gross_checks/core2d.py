'''
Redefined as a function
Gross bound checks on .nc files, developed primarily from the sea ice (CICE6) output
Robert Grumbine
30 January 2020
3 March 2025

data file = argv[1] (input)
model definition = argv[2] (input)
control dictionary = argv[3] (input)
bootstrapped dictionary = argv[4] (optional, may be written to if needed and present)
'''

import os
import sys
import numpy as np

import netCDF4

#-----------------------------------------------------------------------------

def core_check(fname, moddef, ctl_dictionary, flying, fout = sys.stdout ):
  errcount = int(0)
  # Get model output file
  if (not os.path.exists(fname) ):
    print("failure to find ",fname)
    sys.exit(1)
  else:
    model = netCDF4.Dataset(fname, 'r')

  # Read in header definition file:
  if (os.path.exists(moddef)):
    fin = open(moddef, encoding='utf-8')
  else:
    print("could not open definition file ",moddef)
    sys.exit(1)
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
    #debug: print(words[0] , words[1], flush=True)
    k += 1

  # Acquire descriptive (e.g. nx, tlons) or support (e.g. tmask) variables
  nx = len(model.dimensions[headers['nx']])
  ny = len(model.dimensions[headers['ny']])
#RG: need to handle case of regular lat-lon grid, 1 d specifications
  try:
    tlons = model.variables[headers['TLON']][:,:]
  except:
    print("error getting TLON. maybe 1d instead of 2d?")
    tlons = np.zeros((ny,nx))
    tmp = model.variables[headers['TLON']][:]
    tlons[:,:] = tmp[:]
    print("tried to work with 1d",tlons[ny-1, nx-1], tlons[1,1])

  try:
    tlats = model.variables[headers['TLAT']][:,:]
  except:
    print("error getting TLAT. maybe 1d instead of 2d?")
    tlats = np.zeros((ny, nx))
    tmp = model.variables[headers['TLAT']][:]
    for tmpindex in range(0,nx):
      tlats[:,tmpindex] = tmp[:]
    print("tried to work with 1d",tlats[ny-1, nx-1], tlats[1,1])

  #LAND = 0, #Ocean = 1
  try:
    tmask = model.variables[headers['tmask']][:,:]
  except :
    tmask = np.zeros((ny, nx))
    tmask = 1.

  try:
    tarea = model.variables["tarea"][:,:]
  except:
    tarea = np.zeros((ny, nx))
    tarea = 1.

  #Get the dictionary file, perhaps with bounds given
  try:
    fdic = open(ctl_dictionary, encoding='utf-8')
  except:
    print("could not find a dictionary file ",ctl_dictionary)
    sys.exit(1)

  try:
    flying_dictionary = open(flying,"w", encoding='utf-8')
    flyout = True
  except:
    #debug
    print("cannot write out to bootstrap dictionary file", flush=True)
    flyout = False

  # Now loop over all variables in the dictionary file looking for out of bounds values
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
    gfail = tmp.whether(temporary_grid, fout = fout)

    #Pointwise checks -- Show where (and which) test failed:
    if (gfail):
      errcount += tmp.where(temporary_grid, tlats, tlons, tmask, tarea, fout = fout)

    parmno += 1

  # Done with checking
  return errcount
