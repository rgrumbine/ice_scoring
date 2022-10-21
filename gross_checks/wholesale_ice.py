import os
import sys
import datetime
from math import *
import numpy as np

import netCDF4
#---------------------------------------------------
import bounders

#---------------------------------------------------
#Gross bound checks on .nc files, developed primarily from the sea ice (CICE6) output
#Robert Grumbine
#30 January 2020
#
#data file = argv[1] (input)
#control dictionary = argv[2] (input)
#control dictionary -- reprint argv[3] (output)

#---------------------------------------------------

if (not os.path.exists(sys.argv[1]) ):
  print("failure to find ",sys.argv[1])
  exit(1)

model = netCDF4.Dataset(sys.argv[1]+"/20120101/ice20120202.01.2012010100.subset.nc", 'r')
#                                     "20120101/ice20120202.01.2012010100.subset.nc",'r')
nx = len(model.dimensions['ni'])
ny = len(model.dimensions['nj'])
tlons = model.variables["TLON"][:,:]
tlats = model.variables["TLAT"][:,:]
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

tmp    = bounders.bounds()
tbound = tmp.bootstrap(sys.argv[2], sys.argv[3], model)
parmno = len(tbound)

#-------------------------- Finished with bootstrap and/or first pass

#dt     = datetime.timedelta(seconds=6*3600)
dt     = datetime.timedelta(seconds=24*3600)
length = datetime.timedelta(days=35)
  
#Now carry on for the forecasts
for yy in (2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018):
  for mm in range (1,13):
    for dd in ( 1, 15):
      from_date = datetime.datetime(int(yy),int(mm),int(dd), int(0) )
      valid_date = from_date + dt
      tag = from_date.strftime("%Y%m%d")

      #ice 
      #base="/scratch2/NCEPDEV/climate/Robert.Grumbine/modelout/ufs_p6/gfs."+from_date.strftime("%Y%m%d")+"/00/"
      #base=system(basename sys.argv[1])
      base = sys.argv[1] + "/" + from_date.strftime("%Y%m%d") + "/"

      print("base = ",base,flush=True)
      fout  = open("ice."+tag,"w")
      fout_global  = open("ice.global."+tag,"w")
      while ( (valid_date - from_date) <= length):

        fname=base+"/ice"+valid_date.strftime("%Y%m%d")+".01."+from_date.strftime("%Y%m%d%H")+".subset.nc"
       #fname=base+"/ice"+valid_date.strftime("%Y%m%d%H")+".01."+from_date.strftime("%Y%m%d%H")+".nc"
        if (not os.path.exists(fname)):
          print("couldn't get ",fname, file = fout)
          valid_date += dt
          continue
      
        model = netCDF4.Dataset(fname, 'r')
        print("valid date = ",valid_date.strftime("%Y%m%d%H"), file = fout)
        sys.stdout.flush()
        for k in range(0,len(tbound)):
          temporary_grid = model.variables[tbound[k].param][0,:,:]
          gfail = tbound[k].inbounds(temporary_grid, fout_global)
          if (gfail):
            #debug print("calling where", flush=True)
            tbound[k].where(temporary_grid, tlats, tlons, tmask, tarea, fout)
          #debug else:
            #debug print("gfail should be false: ",gfail, flush=True)
        
        valid_date += dt

      fout.close()
      fout_global.close()
