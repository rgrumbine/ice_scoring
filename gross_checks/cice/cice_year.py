import os
import sys
import datetime

ICE_RUNDIR='/ncrc/home1/Robert.Grumbine/scratch/CICE_RUNS/gaea_intel_smoke_gx1_8x1_gx1_run_std.beta8'

dt    = datetime.timedelta(1)
start = datetime.datetime(2005,1,1)
end   = datetime.datetime(2005,12,31)
tag   = start

while (tag <= end):
  yy = tag.strftime("%Y")
  mm = tag.strftime("%m")
  dd = tag.strftime("%d")
  fname = ICE_RUNDIR+"/history/iceh."+yy+'-'+mm+'-'+dd+'.nc'
  if (os.path.exists(fname)):
    print("python3 cice.py ",fname," ctl/cice.extremes alpha > out."+tag.strftime("%Y%m%d") )

  tag += dt

