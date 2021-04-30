import netCDF4
import numpy as np


import bounders

#-----------------------------------------------------------------
tmp = bounders.bounds()
fname = "../../phyf006.tile1.nc"

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
name_of_x_direction = "grid_xt" #longitudes, nx
name_of_y_direction = "grid_yt" #latitudes, ny
# Names of special grids:
name_of_latitudes  = "grid_xt"
name_of_longitudes = "grid_yt"
name_of_landmask   = "land"     # can run without one
name_of_cellarea   = ""         # can run without one
# ------------- below here should be generic to all systems -------------------


#nx = orig.dimensions[name_of_x_direction].name
nx = orig.dimensions[name_of_x_direction].size
ny = orig.dimensions[name_of_y_direction].size
lats = orig.variables[name_of_latitudes][:,:]
lons = orig.variables["grid_xt"][:,:]
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

dictionary_file = "beta"
bootstrap_file  = "boot_out"
tbound = tmp.bootstrap(dictionary_file, bootstrap_file, orig)
#  The following isn't needed, as the output will be sent to bootstrap_file already.
#for i in range (0,len(tbound)):
#  tbound[i].show()

orig.close()

exit(0)

#note:
#  Nonvalues might actually be printed to the bootstrap_file, need to edit.

#third iteration of the program is to just read in a boostrap file for all values:
orig = netCDF4.Dataset(fname, "r") 
lats = orig.variables["grid_xt"][:,:]
lons = orig.variables["grid_yt"][:,:]
nx = 384
ny = 384
try:
  tmask = orig.variables["land"][:,:]
except:
  tmask = np.zeros((ny, nx))

try:
  tarea = orig.variables["tarea"][:,:]
except:
  tarea = np.zeros((ny, nx))
  tarea = 1.0

tbound = tmp.readin(dictionary_file, orig)
