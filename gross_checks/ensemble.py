'''
Gross bound checks on .nc files, developed primarily from the sea ice (CICE6) output
Robert Grumbine
30 January 2020
3 March 2025

data directory base = argv[1] (input)
model definition    = argv[2] (input)
control dictionary  = argv[3] (input)
bootstrapped dictionary = argv[4] (optional, may be written to if needed and present)
Requires environment to have MODDEF defined
'''

import os
import sys
#import datetime
#from math import *

#import netCDF4

#from gross import bounders
from core2d import *


base = sys.argv[1]
moddef = os.environ['MODDEF']+'/'+sys.argv[2]
ctl_dictionary = sys.argv[3]
flying = sys.argv[4]
errcount = 0

for memno in range(0,11):
  # SFS: for hh in range(24, 24*124, 24):
  # GEFS v13: 48 days:
  for hh in range(24, 24*48, 24):
    #ice:
    #fname = base + '00/mem' + "{:03d}".format(memno) + \
    #        '/model/ice/history/gefs.ice.t00z.24hr_avg.f' + "{:03d}".format(hh) + '.nc'

    #ocean:
    fname = base + '00/mem' + "{:03d}".format(memno) + \
            '/products/ocean/netcdf/0p25/gefs.ocean.t00z.0p25.f' + "{:03d}".format(hh) + '.nc'

    if (os.path.exists(fname)):
        print(fname)
        foutname = "grossout_" + "{:03d}".format(memno)+"_"+"{:03d}".format(hh)
        fout = open(foutname, "w", encoding='utf-8')
        errcount += core_check(fname, moddef, ctl_dictionary, flying, fout = fout)
        fout.close()
    else:
        print('not ',fname)
