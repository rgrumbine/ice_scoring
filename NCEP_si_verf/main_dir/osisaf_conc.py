import sys
import datetime

#-----------------------------------------------------------------------
#Evaluate the unix environment
import eval_unix_env
env = eval_unix_env.runtime_environment("", "", "")
if (env.ok_env() != 0 ):
  print("something wrong in unix environment",flush=True)
  exit(1)
else:
  print("valid unix environment", flush=True)
#debug: print("exbase, exdir, fixdir:",x.exbase, flush=True)


#Evaluate the platform ------ this creates some utility variables 
#                             specialized to this environment ------------
import platforms

x = platforms.machine.dirs
#debug: print(x['imsdir'], flush=True)
#debug: print(platforms.imsverf, flush=True)
if not (platforms.imsverf or platforms.nsidcverf or platforms.ncepverf or platforms.osisafverf) : 
  raise Exception ("no valid verification sources, exiting")

  
#Check for verification data and import the 'gridded' class ----------
import verf_files

ims   = verf_files.ims()
#nsidc = verf_files.nsidc_nh()
osisaf = verf_files.osisaf()
ncep   = verf_files.ncep()

#Find the forecast model -- specialized 'gridded' member -------------

import forecast_files

#fcst = forecast_files.hr3b()
#fcst = forecast_files.rtofs()
#fcst = forecast_files.ufs_gdas()
fcst = forecast_files.ufs_gfs()

#----------------------------------------------------------------------
# Import scoring tools
from scores import *

#----------------------------------------------------------------------
# Now ready to loop over forecasts

# HR3b, HR4, HR5 all using a winter and a summer season's forecasts
#Winter
#start = datetime.datetime(2019,12,3)
#end   = datetime.datetime(2020,2,25)
#Retros:
start = datetime.datetime(2024,12,10)
end   = datetime.datetime(2024,12,30)
dt = datetime.timedelta(1)
dt1 = datetime.timedelta(1)

tag = start
exdir = env.exdir
fixdir = env.fixdir

while (tag <= end):
  print(tag)
  #fcstdir = "/home/Robert.Grumbine/clim_data/hr3b/gfs." + tag.strftime("%Y%m%d") + "/00/model_data/ice/history/"
  #fcstdir = "/home/Robert.Grumbine/clim_data/hr4/gfs." + tag.strftime("%Y%m%d") + "/00/model/ice/history/"
  #fcstdir = "/home/Robert.Grumbine/clim_data/hr5/gfs." + tag.strftime("%Y%m%d") + "/00/model/ice/history/"
  #fcstdir = "/u/robert.grumbine/noscrub/model_intercompare/rtofs_cice/rtofs." + tag.strftime("%Y%m%d") + "/"
  #fcstdir = "/u/robert.grumbine/noscrub/retros/gdas."+tag.strftime("%Y%m%d")+"/00/model/ice/history/"
  fcstdir = "/u/robert.grumbine/noscrub/retros/gfs."+tag.strftime("%Y%m%d")+"/00/model/ice/history/"

  ptag="nh"

  valid = tag
  valid += dt1 # for gfs, where no 000 file
  #for hr in range(0,192+1,24): # rtofs
  #for hr in range(3,3+1,3): # gdas
  for hr in range(24,240+1,24): # gfs
    #debug: print(hr, valid, flush=True)

    tmp = fcst.get_grid(hr, fcstdir)
    if (tmp != 0):
      valid += dt1
      continue

    obs = 0
#    if (platforms.ncepverf):
#      obs += ncep.get_grid(tag, x['ncepdir'])
#
#    if (platforms.imsverf):
#      obs += imsverf.get_grid(tag, x['imsdir'])
#
#   if (platforms.nsidcverf):
#     obs += nsidc.get_grid(tag, x['nsidcdir'])

    if (platforms.osisafverf):
      obs += osisaf.get_grid(tag, x['osisafdir'], ptag=ptag)

    #debug: print("obs retcode sum", obs, flush=True)

# Now tailor to concentration verification:
    #if (platforms.nsidcverf):
    #  score_nsidc(fcst, nsidc, fcstdir, x['nsidcdir'], tag, valid, hr, exdir, fixdir)
    #else:
    #  print("could not score concentration for ",fcstdir,
    #         x['nsidcdir'], tag, flush=True)

    if (platforms.osisafverf):
      #debug: print("osisaf_conc calling score_osisaf")
      #score_osisaf(fcst, osisaf, fcstdir, x['osisafdir'], tag, valid, hr, exdir, fixdir)
      score_osisaf(fcst, osisaf, fcstdir, x['osisafdir'], tag, valid, hr, exdir, fixdir, ptag=ptag)
    else:
      print("could not score concentration for ",fcstdir,
             x['osisafdir'], tag, flush=True)

    
# For edges  RG: tripole cice currently bonkers
    #fcst.make_edge(tag, hr, fcstdir, x['edgedir'], exdir, fixdir)

    valid += dt1

  tag += dt
