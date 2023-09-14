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
"""
plot match up lat-lon pts between rtofs and nic edge
RG: should also plot the original full edge for the valid date

Robert Grumbine
27 July 2023
"""
#-------------------------------------------------------------
def getedge(fin, edgelons, edgelats):
    for line in fin:
        words=line.split(",")
        edgelats.append(float(words[1]))
        edgelons.append(float(words[0]))

    print("found ",len(edgelats), len(edgelons), "pts in edge file", flush=True)

# working with output of cscore_edge
def matchedge(fin, distance, edgelon1, edgelat1, edgelon2, edgelat2):
    for line in fin:
        words=line.split()
        if (words[0] == "rms"): break
        distance.append(float(words[2]))
        edgelon1.append(float(words[3]))
        edgelat1.append(float(words[4]))
        edgelon2.append(float(words[5]))
        edgelat2.append(float(words[6]))

    print("found ",len(edgelat1), "matchup pts in edge file", flush=True)

#-------------------------------------------------------------

#PlateCaree
#LambertConformal
#LambertCylindrical
#NorthPolarStereo

def plot_world_map(lons, lats, data, edgelons, edgelats, edgelons2, edgelats2):
    #for shaded maps of 2d fields: 
    #vmin = np.nanmin(data)
    #vmax = np.nanmax(data)

    #debug: print("establishing projection",flush=True)
    proj = ccrs.LambertConformal(central_longitude=-170, central_latitude=60., cutoff=25.)
    #proj = ccrs.NorthPolarStereo(true_scale_latitude=60.)
    #proj = ccrs.Stereographic(central_longitude=+170, central_latitude=60. )

    ax  = plt.axes(projection = proj)
    fig = plt.figure(figsize=(12, 9))
    ax  = fig.add_subplot(1, 1, 1, projection = proj)
    #debug: print("established initial ax, fig",flush=True)

    #ax.set_extent((-220,-120, 40, 90), crs=ccrs.PlateCarree())

    #Bering/okhotsk/some Beaufort/Chukchi
    ax.set_extent((-220,-145, 50, 70), crs=ccrs.PlateCarree())
    ax.gridlines(crs=ccrs.PlateCarree(), 
                 xlocs=[140., 150., 160., 170., -180, -170, -160, -150], 
                 ylocs=[45, 50, 55, 60, 66.6, 70, 75] )
    #debug: 
    print("specialized to Bering et al",flush=True)


    #'natural earth' -- coast only -- 
    ax.coastlines(resolution='10m')
    #ax.add_feature(cfeature.GSHHSFeature(levels=[1,2,3,4], scale="f") )
    #debug: print("coastlines added ",flush=True)

    plttitle = 'Plot of %s' % ("ice edge")
    plt.title(plttitle)
    #debug: print("title added ",flush=True)

    #Establish the color bar
    #colors=matplotlib.cm.get_cmap('jet')
    #colors=matplotlib.cm.get_cmap('gray')
    colors=matplotlib.cm.get_cmap('terrain')
    #debug: print("color map added ",flush=True)

#for shaded maps of 2d fields: 
    #cs = ax.pcolormesh(lons, lats, data,vmin=vmin,vmax=vmax,cmap=colors, transform=ccrs.PlateCarree() )
    #cs = ax.pcolormesh(lons, lats, data,vmin=30.,vmax=vmax,cmap=colors, transform=ccrs.PlateCarree() )

    #cb = plt.colorbar(cs, extend='both', orientation='horizontal', shrink=0.5, pad=.04)
    #cbarlabel = '%s' % ("hello1")
    #cb.set_label(cbarlabel, fontsize=12)

# For a scatter plot of points:
    #debug: print("about to try scatter plot",flush=True)
    plt.scatter(edgelons, edgelats, transform=ccrs.PlateCarree(), s = 0.5, alpha = 0.5, c='black' )
    plt.scatter(edgelons2, edgelats2, transform=ccrs.PlateCarree(), s = 0.5, alpha = 0.5, c='blue' )
    #debug: print("back from scatter plot",flush=True)

# General

    plt.savefig("hello4.png")

    plt.close('all')

#----------------------------------------------------------------

lons = range(-360,360)
lats = range(-90,90)
data = np.zeros((len(lats),len(lons)))

# Dummy
for i in range(-360,360):
  data[:,i] = lats[:] 

edgelat1 = []
edgelon1 = []
edgelat2 = []
edgelon2 = []
distance = []

fin = open(sys.argv[1],"r")
#getedge(fin, edgelons, edgelats)
matchedge(fin, distance, edgelon1, edgelat1, edgelon2, edgelat2)

print("back from matchedge", flush=True)

plot_world_map(lons, lats, data, edgelon1, edgelat1, edgelon2, edgelat2)
  
