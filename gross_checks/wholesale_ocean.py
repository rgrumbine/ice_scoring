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

tbound = []

#---------------------------------------------------

if (not os.path.exists(sys.argv[1]) ):
  print("failure to find ",sys.argv[1])
  exit(1)
else:
  model = netCDF4.Dataset(sys.argv[1], 'r')
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

  try:
    fdic = open(sys.argv[2])
  except:
    print("could not find a dictionary file ",sys.argv[2])
    exit(1)

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
    tmp = bounders.bounds(param=parm)
    try: 
      temporary_grid = model.variables[parm][0,:,:]
    except:
      print(parm," not in data file")
      continue

    # find or bootstrap bounds -----------------
    tmp.set_bounds(temporary_grid, words, flyout, flying_dictionary)

    tbound.append(tmp)
    if (flyout):
      tbound[parmno].show(flying_dictionary)
    else:
      tbound[parmno].show(sys.stdout)

    parmno += 1

#-------------------------- Finished with bootstrap and/or first pass
#Now carry on for the forecasts

dt     = datetime.timedelta(seconds=6*3600)
length = datetime.timedelta(days=35)

for yy in (2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018):
  for mm in range (1,13):
    for dd in (1,15):
      from_date  = datetime.datetime(int(yy),int(mm),int(dd), int(0) )
      valid_date = from_date + dt
      tag  = from_date.strftime("%Y%m%d")

      base = "modelout/gfs."+tag+"/00"
      while ( (valid_date - from_date) <= length):
        fout  = open("ocn."+tag,"w")
        fname = base+"/ocn_2D_"+valid_date.strftime("%Y%m%d%H")+".01."+
                               from_date.strftime("%Y%m%d%H")+".nc"
        if (not os.path.exists(fname)):
          print("couldn't get ",fname, file=fout)
          valid_date += dt
          continue
      
        model = netCDF4.Dataset(fname, 'r')
        print("valid date = ",valid_date.strftime("%Y%m%d%H"), file=fout)
        sys.stdout.flush()
        for k in range(0,len(tbound)):
          temporary_grid = model.variables[tbound[k].param][0,:,:]
          gfail = tbound[k].inbounds(temporary_grid, fout)
          if (gfail):
            tbound[k].where(temporary_grid, tlats, tlons, tmask, tarea, fout)
          
        valid_date += dt
      fout.close()
