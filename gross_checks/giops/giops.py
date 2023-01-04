import os
import datetime

import netCDF4

surface_parms = [ "iiceconc", "iicedivergence", "iicepressure", "iiceshear", 
                 "iicestrength", "iicesurftemp", "iicevol", "isnowvol", 
                 "itmecrty", "itzocrtx", "sokaraml", "somixhgt",  "sossheig" ]
level = "sfc_0"
grid="ps5km60N"
span="3h-mean"
ymd = datetime.datetime(2022,12,12).strftime("%Y%m%d")
cyc = "00"
base="/u/robert.grumbine/noscrub/model_intercompare/giops/giops."+ymd+"/"

for hr in range(3, 241, 3):
  hhh = "{:03d}".format(hr)
  for parm in surface_parms:
    fname = "CMC_giops_"+parm+"_"+level+"_"+grid+"_"+span+"_"+ymd+cyc+"_P"+hhh+".nc"
    if (not os.path.exists(base+fname)):
        print("problem with "+base+fname)
        continue
    else:
        print("ok")
    #print(fname)


