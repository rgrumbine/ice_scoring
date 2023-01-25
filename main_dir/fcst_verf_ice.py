import os
import sys
import datetime

#Arguments:
#   start_date verification_date forecast_dir_path

from verf_files import *
from platforms import *

##################### ------------- 
#--------------- Utility Functions --------------------------------

#------------------------------------------------------------------

def solo_score(fcst, fdate):
  if (fcst == "nsidc"): return 0
  fname = fcst+"."+fdate.strftime("%Y%m%d")
  if (os.path.exists(fname)):
    cmd = (exdir + "solo_" +fcst+" "+fixdir+"seaice_gland5min "+fname)
    print("integrals for ",fcst, flush=True)
    sys.stdout.flush()
    x = os.system(cmd)
    if (x != 0):
      print("command ",cmd," returned error code ",x, flush=True)
    return x 
  else:
    print("could not find ",fname, flush=True)
    return 1

def edge_score(fcst, fdate, obs, obsdate):
  retcode = int(0)
  fname   = fcst+"_edge."+fdate.strftime("%Y%m%d")
  obsname = obs +"_edge."+obsdate.strftime("%Y%m%d")
  outfile = ("edge." + fcst + "." + obs + "." +fdate.strftime("%Y%m%d") 
                + "."+obsdate.strftime("%Y%m%d") )

  if (os.path.exists(fname) and os.path.exists(obsname) and not 
      os.path.exists(outfile) ):
    cmd = (exdir + "cscore_edge "+fixdir+"seaice_alldist.bin "+fname+" "+obsname +
           " 50.0 > " + outfile )
    #debug
    print("edge_score: ",cmd,flush=True)
    x = os.system(cmd)
    if (x != 0):
      print("command ",cmd," returned error code ",x, flush=True)
      sys.stdout.flush()
      retcode += x

  return retcode

def score_nsidc(fcst_dir, nsidcdir, fdate, obsdate):
  retcode = int(0)
  vyear = int(obsdate.strftime("%Y"))

  #isolate forecast file name references to fcst_name:
  valid_fname = fcst_name(obsdate, fdate, fcst_dir)
  #UFS style:
  #valid_fname = fcst_dir+'ice'+obsdate.strftime("%Y%m%d")+'00.01.'+fdate.strftime("%Y%m%d")+'00.subset.nc'
  #CICE consortium name:
  #valid_fname = fcst_dir+'iceh.'+obsdate.strftime("%Y")+'-'+obsdate.strftime("%m")+'-'+obsdate.strftime("%d")+".nc"

  if (not os.path.exists(valid_fname)):
    print("cannot find forecast file for "+fdate.strftime("%Y%m%d"),obsdate.strftime("%Y%m%d"), flush=True )
    retcode = int(1)
    return retcode
  
  exname = 'generic'
  exname = 'score_nsidc'
  if (os.path.exists(exdir + exname)):
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
initial_date = parse_8digits(sys.argv[1])
valid_date   = parse_8digits(sys.argv[2])
fcst_dir     = sys.argv[3] 
fcst_dir     += "/"+sys.argv[1]
single       = True
#debug
print("setup_verf initial_date", valid_date, flush=True)

imsverf   = True
nsidcverf = False
ncepverf  = True
osiverf   = False

#===============================================================================
if (single):
#IMS:
  if (imsverf): 
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

  obs = (nsidcverf or ncepverf or imsverf or osiverf)

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

  if (fcst):
    print("fcst = True, try scoring",flush=True)
    #solo_score("fcst", valid_date) -- to be developed

    fcst_edge(initial_date.strftime("%Y%m%d"), valid_date.strftime("%Y%m%d"), fcst_dir)
    if (imsverf):   
      print("trying imsverf edge",flush=True)
      edge_score("fcst", valid_date, "ims", valid_date)
    if (ncepverf):  
      print("trying ncepverf edge",flush=True)
      edge_score("fcst", valid_date, "ncep", valid_date)
    if (nsidcverf): 
      print("trying nsidcverf edge",flush=True)
      edge_score("fcst", valid_date, "nsidc_north", valid_date)

    if (nsidcverf): 
      score_nsidc(fcst_dir, dirs['nsidcdir'], initial_date, valid_date)
    else:
      print("could not score concentration for ",fcst_dir, dirs['nsidcdir'], initial_date, valid_date, flush=True)
    

    print("\n", flush=True)

