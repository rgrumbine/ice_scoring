import os
import sys

import netCDF4
import numpy as np


import bounders

#-----------------------------------------------------------------
tmp = bounders.bounds()
#fname = "../../phyf006.tile1.nc"
fname = sys.argv[1]

#Perform an initial scan of some file and write out the information 
fout = open("alpha","w")
tmp.scan(fname, fout)
#exit(0)

#-----------------------------------------------------------------
# read fout and determine what the name of the latitude and longitude variables are
#  also the mask and cellarea variables, if present
# also need an ncdump t0 determine nx, ny 
# copy and edit alpha to beta
# now look at what the extrema should be
orig = netCDF4.Dataset(fname, "r") 

#  This stage takes some manual inspection of the above output file
#Dimensions:
name_of_x_direction = "ni" #longitudes, nx
name_of_y_direction = "nj" #latitudes, ny
# Names of special grids:
name_of_latitudes  = "TLAT"
name_of_longitudes = "TLON"
name_of_landmask   = "tmask"     # can run without one
name_of_cellarea   = "tarea"     # can run without one
# ------------- below here should be generic to all systems -------------------


nx = orig.dimensions[name_of_x_direction].size
ny = orig.dimensions[name_of_y_direction].size
lats = orig.variables[name_of_latitudes][:,:]
lons = orig.variables[name_of_longitudes][:,:]
print(nx , "nx")
print(ny , "ny")

try:
  tmask = orig.variables[name_of_landmask][:,:]
except:
  tmask = np.zeros((ny, nx))

try:
  tarea = orig.variables[name_of_cellarea][:,:]
except:
  tarea = np.zeros((ny, nx))
  tarea = 1.0


print("now trying dictionary and bootstrap files")

dictionary_file = "beta"
bootstrap_file  = "boot_out"
tbound = tmp.bootstrap(dictionary_file, bootstrap_file, orig)
#  The following isn't needed, as the output will be sent to bootstrap_file already.
#for i in range (0,len(tbound)):
#  tbound[i].show()

orig.close()

#exit(0)

#note:
#  Nonvalues might actually be printed to the bootstrap_file, need to edit.

#third iteration of the program is to just read in a boostrap file for all values:
print("third iteration")
orig = netCDF4.Dataset(fname, "r") 
lats = orig.variables[name_of_latitudes][:,:]
lons = orig.variables[name_of_longitudes][:,:]

try:
  tmask = orig.variables[name_of_landmask][:,:]
except:
  tmask = np.zeros((ny, nx))

try:
  tarea = orig.variables[name_of_cellarea][:,:]
except:
  tarea = np.zeros((ny, nx))
  tarea = 1.0

tbound = tmp.readin(dictionary_file, orig)
