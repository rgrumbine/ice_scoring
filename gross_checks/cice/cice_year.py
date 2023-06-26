import os
import sys
import datetime

ICE_BASE='/ncrc/home1/Robert.Grumbine/scratch/CICE_RUNS/gaea_intel_smoke_gx3_4x1_'
#exp = 'yr_out'
#exp = 'no_dyn_yr_out'
#exp = 'no_therm_yr_out'
exp = 'no_dyn_no_therm_yr_out'

ICE_RUNDIR=ICE_BASE+exp+'.try5/history'


dt    = datetime.timedelta(1)
start = datetime.datetime(2005,1,1)
end   = datetime.datetime(2005,12,31)
tag   = start

while (tag <= end):
  yy = tag.strftime("%Y")
  mm = tag.strftime("%m")
  dd = tag.strftime("%d")
  fname = ICE_RUNDIR+"/iceh."+yy+'-'+mm+'-'+dd+'.nc'
  if (os.path.exists(fname)):
    print("python3 retry.py ",fname," ./cice.extremes alpha > out."+tag.strftime("%Y%m%d") )

  tag += dt

