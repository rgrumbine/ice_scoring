import os
import sys

import numpy as np

try:
  title_tag = sys.argv[2]
except:
  title_tag = "ref"

fin = open(sys.argv[1],"r")
parm = []
i = []
j = []
lon = []
lat = []

for line in fin:
  if ("pm" in line):
    words = line.split()
    try:
      tp = (words[0].split(":"))[1]
    except:
      tp = words[0]
    parm.append(tp)
    i.append(int(words[1]))
    j.append(int(words[2]))
    lon.append(float(words[3]))
    tll = float(words[4])
    lat.append(tll)

print("found ",len(i)," error points")
#debug print(max(lat), min(lat), max(lon), min(lon) )
latmax = max(lat)
latmin = min(lat)
lonmax = max(lon)
lonmin = min(lon)


# i-j plot of error points ----------------------------------
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg') #batch mode

#Elaborations:
#  title
#  axis labels
#  separate color/symbol per parameter
fig,ax = plt.subplots()
ax.scatter(i,j)
ax.grid() 
plt.savefig("ij_errs_"+title_tag+".png")
plt.close()


# lat-lon plot of error points ---------------------------------
import cartopy.crs as ccrs
import cartopy.feature as cfeature

#proj = ccrs.LambertConformal(central_longitude=-170., central_latitude = 60., cutoff=25.)
proj = ccrs.PlateCarree()

ax = plt.axes(projection = proj)
fig = plt.figure(figsize = (8,6))
ax = fig.add_subplot(1,1,1,projection = proj)

xlocs = list(range(-180,181,30))
#xlocs = list(range(10*int(lonmin/10), 10*int(lonmax/10), 10))

if ((latmax - latmin) < 30):
  mean = (latmax + latmin)/2.
  ax.set_extent((-180, 180, mean + 30, mean - 30), crs=ccrs.PlateCarree() )
  ylocs = list(range(int(mean-30), int(mean + 30), 5))
else:
  ylocs = list(range(-90, 91, 15))

ax.gridlines(crs=ccrs.PlateCarree(), xlocs=xlocs, ylocs=ylocs )
# not on hera: ax.coastlines()
ax.add_feature(cfeature.GSHHSFeature(levels=[1,2,3,4], scale="c") )
plt.scatter(lon, lat, transform=ccrs.PlateCarree())
plt.savefig("ll_errs_"+title_tag+".png")
plt.close()


#ice.20110815:uvel_h 428 187 167.125 -61.725048 1.5127246  vs pmax  1.5
#ice.20110815:uvel_h 429 187 167.375 -61.725048 1.5152752  vs pmax  1.5
#ice.20110815:uvel_h 430 187 167.625 -61.725048 1.5041997  vs pmax  1.5
