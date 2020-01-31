import os
import sys
from math import *

#---------------------------------------------------
#Develop a class for bounds checking
#Robert Grumbine
#30 January 2020

class bounds:

  def __init__(self, param = "", pmin=0., pmax = 0., pmaxmin = 0., pminmax = 0.):
    self.param = param
    self.pmin = pmin
    self.pmax = pmax
    self.pmaxmin = pmaxmin
    self.pminmax = pminmax

  def scanline(self, dictionary_in):
    print("scanline")

  def findbounds(self, grid):
    self.pmin = grid.min()
    self.pmax = grid.max()
    #do the multiplier to avoid roundoff issues with printout values
    if (self.pmin < 0):
       self.pmin *= 1.001
    else:
       self.pmin *= 0.999
    if (self.pmax < 0):
       self.pmax *= 0.999
    else:
       self.pmax *= 1.001    
    self.pmaxmin = self.pmin + 0.1*(self.pmax - self.pmin)
    self.pminmax = self.pmax - 0.1*(self.pmax - self.pmin)

  def show(self, flying_out_file = sys.stdout):
    #RG: need to do something different in formatting small numbers (fsalt, for ex)
    strpmin   = strprec(self.pmin) 
    strpmax   = strprec(self.pmax)
    strpmaxmin = strprec(self.pmaxmin)
    strpminmax = strprec(self.pminmax)
    print("{:10s}".format(self.param), 
      strpmin, strpmax, strpmaxmin, strpminmax,
      file=flying_out_file)

  def inbounds(self, grid):
    #apply the tests
    gmin = grid.min()
    gmax = grid.max()
    gfail = False
    if (gmin < self.pmin):
      print("{:10s}".format(self.param)," excessively low minimum ",
               gmin," versus ",self.pmin," allowed")
      gfail = True
    if (gmin > self.pmaxmin):
      print("{:10s}".format(self.param)," excessively high minimum ",
               gmin," versus ",self.pmaxmin," allowed")
      gfail = True
    if (gmax > self.pmax):
      print("{:10s}".format(self.param)," excessively high maximum ",
               gmax," versus ",self.pmax," allowed")
      gfail = True
    if (gmax < self.pminmax ):
      print("{:10s}".format(self.param)," excessively low maximum ",
               gmax," versus ",self.pminmax," allowed")
      gfail = True    
    return gfail

  def where(self, grid, lats, lons, mask, area):
    #Show where (and which) test failed:
    ny = grid.shape[0]
    nx = grid.shape[1]
    #print("nx, ny = ",nx, ny)
    #print("pmin, pmax = ",self.pmin, self.pmax)
    print("parameter i j longitude latitude model_value test_checked test_value")
    sys.stdout.flush()
    for j in range (0,ny):
      for i in range (0,nx):
        x = grid[j,i]
        if (x < self.pmin):
          print(self.param,i,j,lons[j,i], lats[j,i], x, " vs pmin ",self.pmin)
        if (x > self.pmax):
          print(self.param,i,j,lons[j,i], lats[j,i], x, " vs pmax ",self.pmax)
      sys.stdout.flush()

def strprec(x):
  if (abs(x) < 1.e-3):
    strpmin = "{:.5e}".format(x)
  else:
    strpmin = "{:.5f}".format(x)
  return strpmin
  
