import os
import sys
import datetime

from math import *
import numpy as np
import numpy.ma as ma

import netCDF4

#---------------------------------------------------
# Compute what can be computed, descriptively from gridded information in a 
#    single pass through a set of data files 
# For each variable:
#    gridded: max, min, sumx, sumx2 (thence mean, sqrt(var))
#    global: each day's max, min, 
#        (thence maximum max, minimum max, maximum min, minimum min)

class scanner:

  def __init__(self, nx = 0, ny = 0, nt = 0):
    self.nx = nx
    self.ny = ny
    self.nt = nt
    self.sumx  = np.zeros((ny, nx))
    self.sumx2 = np.zeros((ny, nx))
# not so nicely griddable    self.xmax  = np.zeros((ny, nx))
# not so nicely griddable    self.xmin  = np.zeros((ny, nx))
    self.dmax = np.zeros((nt))
    self.dmin = np.zeros((nt))

  def finish(self, label):
# need something for masked/flagged points
    #debug print("in finish ",flush=True)
    self.mean    = self.sumx / float(self.nt) 
    #sqrtvar = np.sqrt( self.sumx2-self.sumx*self.sumx )
    self.maxmax  = self.dmax.max()
    self.minmax  = self.dmax.min()
    self.maxmin  = self.dmin.max()
    self.minmin  = self.dmin.min()
    print(label, self.mean.max(), self.mean.min())
    # Print out in order of the gross checker:
    print(label, self.minmin, self.maxmax, self.maxmin, self.minmax, flush=True)

  def add(self, x, tau):
    self.sumx  += x
    #self.sumx2 += x*x
    self.dmax[tau] = x.max()
    self.dmin[tau] = x.min()

#---------------------------------------------------
#  Info for a particular data set to process:
refyear = 1990
span = 1
ymd = datetime.date(refyear, 1, 1)
dt = datetime.timedelta(1)
daydt = datetime.timedelta(1)
base="/work/noaa/ng-godas/marineda/experiment/ufs100_baseline_1979_2000_kitd_0_BL99/bkg/"
tau = 0
nx = 360
ny = 320
nt = 365

# Variable to hold the progressive scan information:
x = scanner(nx, ny, nt)
#parm = "SSU"
parm = sys.argv[1]

#---------------------------------------------------
while (ymd < datetime.date(refyear+span, 1, 1)):
  year = ymd.strftime("%Y")
  mon  = ymd.strftime("%m")
  day  = ymd.strftime("%d")
  dayp1 = (ymd+daydt).strftime("%d")
  monp1 = (ymd+daydt).strftime("%m")
  yearp1 = (ymd+daydt).strftime("%Y")
  tag = ymd.strftime("%Y%m%d")
# Note that ocn_diag is for the next day:
# 19672 -rw-r----- 1 jongkim marine  20141680 Feb  9 10:25 ocn.bkg.1979010112.nc
#281212 -rw-r----- 1 jongkim marine 287956316 Feb  9 10:25 ocn_diag_1979_01_02.nc
  fname = base+year+"/"+tag+"12/ctrl/ocn_diag_"+yearp1+"_"+monp1+"_"+dayp1+".nc"

  if (not os.path.exists(fname)):
    print("failed on: ",fname)
    exit(1)
  else:
    #print("have ",fname)
    model = netCDF4.Dataset(fname, 'r')
    filenx = len(model.dimensions['xh'])
    fileny = len(model.dimensions['yh'])
    #tlons = model.variables["geolon"][:,:]
    #tlats = model.variables["geolat"][:,:]
    if (filenx != nx or fileny != ny):
      print("file data of wrong size ",filenx, fileny, "versus", nx, ny)
    tmpx = model.variables[parm][0,:,:]
    #debug print("tmpx ",tmpx.max(), tmpx.min() )
    x.add(tmpx, tau)
    

  ymd += dt
  tau += 1


#debug print(ymd, tau, x.nx, x.ny)
x.finish(parm)
#---------------------------------------------------

