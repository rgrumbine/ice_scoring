import os
import sys
import datetime

#Arguments:
#   start_date verification_date forecast_dir_path
#   or
#   start_date number_days_forward time_delta_days forecast_dir_path


from platforms import *

from verf_files import *
from scores import *


##################### ------------- 
#--------------- Utility Functions --------------------------------

#------------------------------------------------------------------
def get_obs(initial_date, valid_date, imsverf, ncepverf, nsidcverf, 
             imsdir, ncepdir, nsidcdir):
  retcode = int(0)
  initial    = int(initial_date.strftime("%Y%m%d"))
  valid      = int(valid_date.strftime("%Y%m%d"))
  moninitial = int(initial_date.strftime("%Y%m"))
  monvalid   = int(valid_date.strftime("%Y%m"))
  yearinitial = int(initial_date.strftime("%Y"))
  yearvalid   = int(valid_date.strftime("%Y"))
  return retcode

def score_nsidc(fcst_dir, nsidcdir, fdate, obsdate):
  retcode = int(0)
  vyear = int(obsdate.strftime("%Y"))

  #isolate forecast file name references to fcst_name:
  valid_fname = fcst_name(obsdate, fdate, fcst_dir)

  #UFS style:

  #CICE consortium name:
  #valid_fname = fcst_dir+'iceh.'+obsdate.strftime("%Y")+'-'+obsdate.strftime("%m")+'-'+obsdate.strftime("%d")+".nc"

  if (not os.path.exists(valid_fname)):
    print("setup_verf_ice.py cannot find forecast file for "+fdate.strftime("%Y%m%d"),obsdate.strftime("%Y%m%d"), flush=True )
    retcode = int(1)
    return retcode
  
  exname = 'generic'
  exname = 'score_nsidc'
  if (os.path.exists(exdir + exname)):
    #debug print("setup_verf Have the fcst vs. nsidc scoring executable", flush=True)
    sys.stdout.flush()
    pole="north"
    ptag="n"
    #obsname = (nsidcdir + pole + str(vyear) + "/seaice_conc_daily_"+ptag+"h_f17_"+
    #                    obsdate.strftime("%Y%m%d")+"_v03r01.nc" )
    obsname = nsidc_name(pole, obsdate, nsidcdir)

    cmd = (exdir+exname+" "+valid_fname+" "+obsname+ " "+fixdir+"skip_hr " + 
                exdir+"runtime.def "+ " > score."+
                ptag+"."+obsdate.strftime("%Y%m%d")+"f"+fdate.strftime("%Y%m%d")+".csv")
    x = os.system(cmd)
    if (x != 0):
      print("command ",cmd," returned error code ",x, flush=True)
      retcode += x

#    pole="south"
#    ptag="s"
#    obsname = nsidc_name(pole, obsdate, nsidcdir)

  else:
    print("No executable to score vs. nsidc", flush=True)
    sys.stdout.flush()
    retcode += 1

  return retcode

#---------------------------- Begin program ---------------------


# dates, times -- initial date/time, verification date-time, or initial, 
#     lead range, and delta

#the +1 is for the command name itself, which is sys.argv[0]
if (len(sys.argv) >= 3+1):
  #debug print("setup_verf Initial date and verification time", flush=True)
  initial_date = parse_8digits(sys.argv[1])
  valid_date   = parse_8digits(sys.argv[2])
  #fcst_dir     = sys.argv[3] + "/" + sys.argv[4]
  fcst_dir     = sys.argv[3] 
  single = True
  #debug
  print("setup_verf initial_date", valid_date, flush=True)
  sys.stdout.flush()

#===============================================================================
#If a single verification, then one thing, else, create many single verifications:
if (single):
#IMS:
  if (imsverf): 
    x = get_ims(initial_date, dirs['imsdir'])
    if (x != 0):
      print("could not get file for ims verification, turning off imsverf\n", flush=True)
      imsverf = False
    x = get_ims(valid_date, dirs['imsdir'])
    if (x != 0):
      print("could not get file for ims verification, turning off imsverf\n", flush=True)
      imsverf = False
#NCEP -- grib/grib2
  if (ncepverf):
    x = get_ncep(initial_date, valid_date, dirs['ncepdir'])
    if (x != 0):
      print("could not get file for ncep verification, turning off ncepverf\n",flush=True)
      ncepverf = False
#NSIDC -- netcdf
  if (nsidcverf):
    x = get_nsidc(initial_date, valid_date, dirs['nsidcdir'])
    if (x != 0):
      print("could not get file for nsidc verification, turning off nsidcverf\n",flush=True)
      nsidcverf = False

  x = get_obs(initial_date, valid_date,
         imsverf, ncepverf, nsidcverf, dirs['imsdir'], dirs['ncepdir'], 
               dirs['nsidcdir'])
  if (x != 0):
    print("get_obs failed for ",initial_date.strftime("%Y%m%d")," ", valid_date.strftime("%Y%m%d")," ",x, flush=True)
    obs = False
  else:
    obs = True

#Model Forecast
  x = get_fcst(initial_date, valid_date, fcst_dir)
  if (x != 0):
    print("get_fcst failed for ",initial_date.strftime("%Y%m%d")," ", valid_date.strftime("%Y%m%d")," ",x, flush=True)
    fcst = False
  else:
    #debug print("setup_verf have forecast ",initial_date.strftime("%Y%m%d")," ", valid_date.strftime("%Y%m%d")," ",x, flush=True)
    fcst = True

  print(flush=True)

  #now call verification with dirs, fcst, verf logicals
  #debug print("setup_verf working with observed data \n", flush=True)
  if (imsverf):
    solo_score("ims", valid_date)
    ims_edge(initial_date.strftime("%Y%m%d"))
    ims_edge(valid_date.strftime("%Y%m%d"))
    edge_score("ims", initial_date, "ims", valid_date)
  if (ncepverf):
    solo_score("ncep", valid_date)
    ncep_edge(initial_date.strftime("%Y%m%d"))
    ncep_edge(valid_date.strftime("%Y%m%d"))
    edge_score("ncep", initial_date, "ncep", valid_date)
    if (imsverf): 
      edge_score("ncep", valid_date, "ims", valid_date)
      edge_score("ims", valid_date, "ncep", valid_date)
  if (nsidcverf):
    solo_score("nsidc", valid_date) #-- still to work out NH/SH vs. single input
    nsidc_edge(initial_date.strftime("%Y%m%d"), 0.40, dirs['nsidcdir'] )
    nsidc_edge(valid_date.strftime("%Y%m%d"), 0.40, dirs['nsidcdir'] )
    edge_score("nsidc_north", initial_date, "nsidc_north", valid_date)
    if(imsverf): edge_score("nsidc_north", valid_date, "ims", valid_date)
    if(ncepverf): edge_score("nsidc_north", valid_date, "ncep", valid_date)
  if (fcst):
    #solo_score("fcst", valid_date) -- to be developed

    fcst_edge(initial_date.strftime("%Y%m%d"), valid_date.strftime("%Y%m%d"), fcst_dir)
    if (imsverf):   edge_score("fcst", valid_date, "ims", valid_date)
    if (ncepverf):  edge_score("fcst", valid_date, "ncep", valid_date)
    if (nsidcverf): edge_score("fcst", valid_date, "nsidc_north", valid_date)

    if (nsidcverf): 
      score_nsidc(fcst_dir, dirs['nsidcdir'], initial_date, valid_date)
    else:
      print("could not score concentration for ",fcst_dir, dirs['nsidcdir'], initial_date, valid_date, flush=True)
    

    print("\n")
    sys.stdout.flush()

else:
  print("in elses branch of setup-verf",flush=True)
  for d in range (1,lead+1):
    valid_date = initial_date + d*dt
    x = get_obs(initial_date, valid_date,
           imsverf, ncepverf, nsidcverf, dirs['imsdir'], dirs['ncepdir'], dirs['nsidcdir'])
    if (x != 0):
      print("get_obs failed for ",initial_date.strftime("%Y%m%d")," ",
             valid_date.strftime("%Y%m%d")," ",x)
      obs = False
    else:
      obs = True

    x = get_fcst(initial_date, valid_date, fcst_dir)
    if (x != 0):
      print("get_fcst failed for ",initial_date.strftime("%Y%m%d")," ",
             valid_date.strftime("%Y%m%d")," ",x)
      fcst = False
    else:
      fcst = True

    #now call verification with dirs, fcst, verf logicals
    if (imsverf):
      ims_edge(initial_date.strftime("%Y%m%d"))
      ims_edge(valid_date.strftime("%Y%m%d"))
      edge_score("ims", initial_date, "ims", valid_date)
    if (ncepverf):
      ncep_edge(initial_date.strftime("%Y%m%d"))
      ncep_edge(valid_date.strftime("%Y%m%d"))
    if (nsidcverf):
      nsidc_edge(initial_date.strftime("%Y%m%d"))
      nsidc_edge(valid_date.strftime("%Y%m%d"))
    if (fcst):
      print("\n")

