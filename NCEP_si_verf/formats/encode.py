#demonstration framework of writing out a netcdf file from python

#Robert Grumbine
#20 August 2020


import numpy 
from netCDF4 import Dataset

rootgrp = Dataset("test.nc","w", format="NETCDF4")

nx   = int(360*12)
ny   = int(180*12)
dlat = 1./12.
dlon = 1./12.

#skip_hr is the byte file flagging points to skip in computing sea ice metrics
fin = open("skip_hr","rb")
dt = numpy.dtype('ubyte')
x = numpy.zeros((nx,ny),dtype=dt)
x = numpy.fromfile(fin,dtype=dt,count=nx*ny)
x.shape = (ny,nx)
print("x max ",x.max(), x.min())

lat = rootgrp.createDimension("lat", ny)
lon = rootgrp.createDimension("lon", nx)

masks = rootgrp.createVariable("skip","ubyte",("lat","lon")  )
masks.units = "none"

#Seems to be important to initialize at least a single element before
#  assigning from x
masks[:,:] = 0
masks = x
print("max ",masks.max(), masks.min(), masks[5,5])

lats  = rootgrp.createVariable("latitude","f4",("lat"))
lats.units = "Degrees N"
lats[:] = 0.0
lats = numpy.arange(-90+dlat/2., 180., dlat)
print("lats: ",lats.max(), lats )

lons  = rootgrp.createVariable("longitude","f4",("lon"))
lons.units = "Degrees E"
lons[:] = 0.0
lons = numpy.arange(    dlon/2., 360., dlon)
print("lons: ",lons.max(), lons )

