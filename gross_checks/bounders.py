import os
import sys
from math import *
import numpy as np
import numpy.ma as ma

import netCDF4

#---------------------------------------------------
#Develop a class for bounds checking
#Robert Grumbine
#30 January 2020

class bounds:

  def __init__(self, param = "", pmin=0., pmax = 0., pmaxmin = 0., pminmax = 0.):
    self.param = param
    self.pmin = float(pmin)
    self.pmax = float(pmax)
    self.pmaxmin = float(pmaxmin)
    self.pminmax = float(pminmax)

  # RG: improve names, set, set_bounds, bootstrap hard to distinguish
  #def bootstrap(self, dictionary_file, bootstrap_file, model, tbound):
  def bootstrap(self, dictionary_file, bootstrap_file, model ):
    tbound = []
    print("in bootstrap, filenames = ",dictionary_file, " and ",bootstrap_file)

    try:
      fdic = open(dictionary_file)
    except:
      print("could not find a dictionary file ",dictionary_file)
      exit(1)
  
    try:
      flying_dictionary = open(bootstrap_file, "w")
      flyout = True
    except:
      print("cannot write out to bootstrap dictionary file")
      flyout = False

    parmno = 0
    for line in fdic:
      words = line.split()
      parm = words[0]
      tmp = bounds(param=parm)
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

    return tbound


  def set(self, param, pmin, pmax, pmaxmin, pminmax):
    self.param = param
    self.pmin = float(pmin)
    self.pmax = float(pmax)
    self.pmaxmin = float(pmaxmin)
    self.pminmax = float(pminmax)

  def set_bounds(self, temporary_grid, words, flyout, flying_dictionary):
    if (len(words) >= 3):
      self.pmin = float(words[1])
      self.pmax = float(words[2])
    else:
      self.findbounds(temporary_grid)

    if (len(words) >= 5):
      self.pmaxmin = float(words[3])
      self.pminmax = float(words[4])
    else:
      self.findbounds(temporary_grid)

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

  def ptinbounds(self, value):
    return (value >= self.pmin and value <= self.pmax)

  def inbounds(self, grid, fout=sys.stdout):
    #apply the tests
    gmin = grid.min()
    gmax = grid.max()
    gfail = False
    if (gmin < self.pmin):
      print("{:10s}".format(self.param)," excessively low minimum ",
               gmin," versus ",self.pmin," allowed", file=fout)
      gfail = True
    if (gmin > self.pmaxmin):
      print("{:10s}".format(self.param)," excessively high minimum ",
               gmin," versus ",self.pmaxmin," allowed", file=fout)
      gfail = True
    if (gmax > self.pmax):
      print("{:10s}".format(self.param)," excessively high maximum ",
               gmax," versus ",self.pmax," allowed", file=fout)
      gfail = True
    if (gmax < self.pminmax ):
      print("{:10s}".format(self.param)," excessively low maximum ",
               gmax," versus ",self.pminmax," allowed", file=fout)
      gfail = True    
    return gfail

  def whether(self, grid, fname = sys.stdout):
    #Global tests -- test whether the grid, in its entirity, is in bound
    gmin = grid.min()
    gmax = grid.max()
    gfail = False
    if (gmin < self.pmin):
      print("{:10s}".format(self.param)," excessively low minimum ",
                gmin," versus ",self.pmin," allowed", file=fname)
      gfail = True
    if (gmin > self.pmaxmin):
      print("{:10s}".format(self.param)," excessively high minimum ",
                gmin," versus ",self.pmaxmin," allowed", file=fname)
      gfail = True
    if (gmax > self.pmax):
      print("{:10s}".format(self.param)," excessively high maximum ",
                gmax," versus ",self.pmax," allowed", file=fname)
      gfail = True
    if (gmax < self.pminmax ):
      print("{:10s}".format(self.param)," excessively low maximum ",
                gmax," versus ",self.pminmax," allowed", file=fname)
      gfail = True
    return gfail



  def where(self, grid, lats, lons, mask, area, fname=sys.stdout):
    errcount = 0
    #Show where (and which) test failed.  self is the bounds data
    if (grid.min() < self.pmin): 
      print("parameter i j longitude latitude model_value test_checked test_value",
                file=fname)
      mask = ma.masked_array(grid < self.pmin)
      indices = mask.nonzero()
      errcount += len(indices[0])
      
      for k in range(0,len(indices[0])):
        i = indices[1][k]
        j = indices[0][k]
        print(self.param,i,j,lons[j,i], lats[j,i], grid[j,i], " vs pmin ",
                self.pmin,file=fname)

    if (grid.max() > self.pmax):
      print("parameter i j longitude latitude model_value test_checked test_value",
                file=fname)
      mask = ma.masked_array(grid > self.pmax)
      indices = mask.nonzero()
      errcount += len(indices[0])
      
      for k in range(0,len(indices[0])):
        i = indices[1][k]
        j = indices[0][k]
        print(self.param,i,j,lons[j,i], lats[j,i], grid[j,i], " vs pmax ",
                self.pmax,file=fname)

    return errcount


  def where_manual(self, grid, lats, lons, mask, area):
    #Show where (and which) test failed:
    ny = grid.shape[0]
    nx = grid.shape[1]
    xslice = np.array(nx)
    #print("nx, ny = ",nx, ny)
    #print("pmin, pmax = ",self.pmin, self.pmax)
    sys.stdout.flush()

    if (grid.min() < self.pmin): 
      print("parameter i j longitude latitude model_value test_checked test_value")
      xslice = self.pmin
      for j in range (0,ny):
        if ( (grid[j,:] >= xslice).all() ):
          continue 
        #print("scanning along j = ",j, "slice test = ", (grid[j,:] >= xslice).all() )
        for i in range (0,nx):
          if (grid[j,i] < self.pmin):
            print(self.param,i,j,lons[j,i], lats[j,i], grid[j,i], " vs pmin ",self.pmin)
      sys.stdout.flush()

    if (grid.max() > self.pmax):
      print("parameter i j longitude latitude model_value test_checked test_value")
      xslice = self.pmax
      for j in range (0,ny):
        if ( (grid[j,:] <= xslice).all() ):
          continue
        for i in range (0,nx):
          if (grid[j,i] > self.pmax):
            print(self.param,i,j,lons[j,i], lats[j,i], grid[j,i], " vs pmax ",self.pmax)
      sys.stdout.flush()

def strprec(x):
  if (abs(x) < 1.e-3):
    strpmin = "{:.5e}".format(x)
  else:
    strpmin = "{:.5f}".format(x)
  return strpmin
  
