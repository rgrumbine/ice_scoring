import sys
import os
import datetime


#ptag="sh"
#pole="south"
ptag="nh"
pole="north"
lead = 16
start = datetime.datetime(2025,1,2)

while (start <= datetime.datetime(2025,1,6) ):
  ncepdir="/u/robert.grumbine/noscrub/com/seaice_analysis/seaice_analysis."+start.strftime("%Y%m%d")
  fname = ncepdir+"/seaice.t00z.5min.grb.grib2"
  cmd = "wgrib2 "+ fname +" | wgrib2 -i "+ fname +" -order we:ns -bin iceout."+start.strftime("%Y%m%d")
  x = os.system(cmd)


  tag = start
  for lead in range (0,lead+1):
    tag = start + datetime.timedelta(lead)
    osidir="/u/robert.grumbine/noscrub/verification/osisaf.met.no/archive/ice/conc/"+tag.strftime("%Y")+"/"+tag.strftime("%m")+"/"
    cmd = "./twelfth_osisaf_"+pole+" iceout."+start.strftime("%Y%m%d")+ \
            " " +osidir+"ice_conc_"+ptag+"_polstere-100_multi_"+tag.strftime("%Y%m%d")+ \
            "1200.nc skip_hr > score.ps."+tag.strftime("%Y%m%d")+"f"+ \
            start.strftime("%Y%m%d")+".csv"
    x = os.system(cmd)

  start += datetime.timedelta(1)

