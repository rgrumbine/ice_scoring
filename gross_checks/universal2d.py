'''
Gross bound checks on .nc files, developed primarily from the sea ice (CICE6) output
Robert Grumbine
30 January 2020
3 March 2025

data file = argv[1] (input)
model definition = argv[2] (input)
control dictionary = argv[3] (input)
bootstrapped dictionary = argv[4] (optional, may be written to if needed and present)
Requires environment to have MODDEF defined
'''

import os
import sys
import numpy as np

import netCDF4

from gross import bounders

#--------------------------------------------------------------------
errcount = int(0)

# Get model output file
if (not os.path.exists(sys.argv[1]) ):
  print("failure to find ",sys.argv[1])
  sys.exit(1)
else:
  model = netCDF4.Dataset(sys.argv[1], 'r')

# Read in header definition file:
if (os.path.exists(os.environ['MODDEF']+'/'+sys.argv[2])):
  fin = open(os.environ['MODDEF']+'/'+sys.argv[2],'r', encoding='utf-8')
else:
  print("could not open definition file ",os.environ['MODDEF']+'/'+sys.argv[2])
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
  print(words[0] , words[1])
  k += 1

# Acquire descriptive (e.g. nx, tlons) or support (e.g. tmask) variables
nx = len(model.dimensions[headers['nx']])
ny = len(model.dimensions[headers['ny']])
tlons = model.variables[headers['TLON']][:,:]
tlats = model.variables[headers['TLAT']][:,:]

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
  fdic = open(sys.argv[3], encoding='utf-8')
except:
  print("could not find a dictionary file ",sys.argv[3])
  sys.exit(1)

try:
  flying_dictionary = open(sys.argv[4],"w", encoding='utf-8')
  flyout = True
except:
  #debug print("cannot write out to bootstrap dictionary file", flush=True)
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
  gfail = tmp.whether(temporary_grid)

  #Pointwise checks -- Show where (and which) test failed:
  if (gfail):
    errcount += tmp.where(temporary_grid, tlats, tlons, tmask, tarea)

  parmno += 1

# Done with checking
#exit codes are bounded, while error counts are not
if (errcount == 0):
  print("found no errors")
else:
  print("errcount = ",errcount)
