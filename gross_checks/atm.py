import netCDF4
import numpy as np


import bounders

#-----------------------------------------------------------------
tmp = bounders.bounds()
fname = "../../phyf006.tile1.nc"

#Perform an initial scan of some file and write out the information 
fout = open("alpha","w")
tmp.scan(fname, fout)

#-----------------------------------------------------------------
# read fout and determine what the name of the latitude and longitude variables are
#  also the mask and cellarea variables, if present
# also need an ncdump t0 determine nx, ny 
# copy and edit alpha to beta
# now look at what the extrema should be
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

dictionary_file = "beta"
bootstrap_file  = "boot_out"
tbound = tmp.bootstrap(dictionary_file, bootstrap_file, orig)
#  The following isn't needed, as the output will besent to bootstrap_file already.
for i in range (0,len(tbound)):
  tbound[i].show()

#note:
#  Nonvalues
