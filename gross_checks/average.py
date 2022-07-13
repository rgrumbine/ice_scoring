import numpy as np
import netCDF4 as nc

nj = int(384)
ni = int(320)
nstep = int(365*8)

tmp     = np.zeros((nj, ni))
average = np.zeros((nj, ni))
rms     = np.zeros((nj, ni))
tmpmax    = np.zeros((nj, ni))
tmpmin    = np.zeros((nj, ni))
# not more efficient to read in at one go vs. piecemeal
# bigtmp  = np.zeros((nstep, nj, ni))

datafile = nc.Dataset('JRA55_03hr_forcing_2005.nc', 'r', format='NETCDF4')

parms = [ 'airtmp', 'dlwsfc', 'glbrad', 'spchmd', 'ttlpcp', 'wndewd', 'wndnwd' ] 
 
for p in parms:
  print(p)
  average = 0.
  rms     = 0.
  tmpmax  = -1.e5
  tmpmin  = +1.e5

  for i in range (0,nstep):
    #if (i%292 == 0):
    #  print("i = ",i,flush=True)
    tmp = datafile.variables[p][i,:,:]
    average += tmp
    rms     += tmp*tmp
    tmpmax = np.maximum(tmp, tmpmax)
    tmpmin = np.minimum(tmp, tmpmin)

  average /= nstep
  rms     /= nstep
  rms = np.sqrt(rms)
  tmp = rms*rms - average*average
  tmp = np.sqrt(tmp)
  print(p, 'average max min: ',average.max(), average.min() ) 
  print(p, 'rms     max min: ',rms    .max(), rms    .min() ) 
  print(p, 'var     max min: ',tmp    .max(), tmp    .min() ) 
  print(p, 'max max min: ',tmpmax.max(), tmpmax.min() )
  print(p, 'min max min: ',tmpmin.max(), tmpmin.min() )
