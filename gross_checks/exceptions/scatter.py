#!/usr/bin/env python3
import argparse
import glob
import os
import sys
import csv

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import netCDF4 as nc

import cartopy.crs as ccrs
import cartopy.feature as cfeature

matplotlib.use('agg')

#-------------------------------------------------------------
def getedge(fin, edgelons, edgelats):
    print("entered getedge",flush=True) 
    for line in fin:
        words=line.split(",")
        edgelats.append(float(words[1]))
        edgelons.append(float(words[0]))

    print("found ",len(edgelats), len(edgelons), "pts in edge file", flush=True)

def getpts(fin, lons, lats):
  print("entered getpts",flush=True) 
  for line in fin:
     words = line.split()
     lons.append(float(words[3]))
     lats.append(float(words[4]))
     #parmname = words[0]
     # i = words[1]
     # j = words[2]
     # value = words[5]
     # reference = words[8]
     #print(float(words[8]),flush=True)
  print("number of pts: ",len(lons),flush=True )
#uvel_h 621 964 220.44373 70.0494 -1.6497943  vs pmin  -1.5
#hs_h 1111 907 338.3247 71.291794 1.1579523  vs pmax  1.15
    
#-------------------------------------------------------------
#PlateCaree
#LambertConformal
#LambertCylindrical
#NorthPolarStereo

def plot_world_map(lons, lats, data, edgelons, edgelats):
    vmin = np.nanmin(data)
    vmax = np.nanmax(data)

    proj = ccrs.LambertConformal(central_longitude=-170, central_latitude=60., cutoff=25.)
    #proj = ccrs.NorthPolarStereo(true_scale_latitude=60.)
    #proj = ccrs.Stereographic(central_longitude=+170, central_latitude=60. )

    ax  = plt.axes(projection = proj)
    fig = plt.figure(figsize=(12, 9))
    ax  = fig.add_subplot(1, 1, 1, projection = proj)

    #Bering/okhotsk/some Beaufort/Chukchi
    #ax.set_extent((-220,-145, 50, 70), crs=ccrs.PlateCarree())
    #ax.gridlines(crs=ccrs.PlateCarree(), 
    #             xlocs=[140., 150., 160., 170., -180, -170, -160, -150], 
    #             ylocs=[45, 50, 55, 60, 66.6, 70, 75] )
    #ax.set_extent((-180,0, 50, 90), crs=ccrs.PlateCarree())
    ax.set_extent((0,179, 50, 90), crs=ccrs.PlateCarree())
    #ax.gridlines(crs=ccrs.PlateCarree(), 
    #             xlocs=[140., 150., 160., 170., -180, -170, -160, -150], 
    #             ylocs=[45, 50, 55, 60, 66.6, 70, 75] )

    #'natural earth' -- coast only -- 
    # not on hera
    #ax.coastlines(resolution='10m')
    #ax.coastlines()
    # GSHHS: c, l, i, h, f (order of increasing precision)
    # on hera, c is present. l is present only for 2-4. i,h,f not present
    ax.add_feature(cfeature.GSHHSFeature(levels=[1], scale="c") )
    ax.add_feature(cfeature.GSHHSFeature(levels=[2,3,4], scale="l") )

    plttitle = 'Plot with coarse coast'
    plt.title(plttitle)

    #Establish the color bar
    #colors=matplotlib.cm.get_cmap('terrain')

# For a scatter plot of points:
    plt.scatter(edgelons, edgelats, transform=ccrs.PlateCarree(), s = 0.5, alpha = 0.5 )

# General
    plt.savefig("hello5.png")
    plt.close('all')

#----------------------------------------------------------------
print("starting program",flush=True)

edgelats = []
edgelons = []
fin = open(sys.argv[1],"r")
getpts(fin, edgelons, edgelats)

lons = range(-360,360)
lats = range(-90,90)
data = np.zeros((len(lats),len(lons)))

for i in range(-360,360):
  data[:,i] = lats[:] 

plot_world_map(lons, lats, data, edgelons, edgelats)
