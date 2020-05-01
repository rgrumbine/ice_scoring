import os
import sys
import datetime

#Arguments:
#   start_date verification_date forecast_dir_path
#   or
#   start_date number_days_forward time_delta_days forecast_dir_path

from verf_files import *

##################### ------------- 
#--------------- Utility Functions --------------------------------

from platforms import *
exbase=os.environ['EXDIR']
exdir = exbase+"/exec/"
fixdir = exbase+"/fix/"
#print("exbase, exdir, fixdir = ",exbase, exdir, fixdir)

#fixed files:
#  seaice_alldist.bin
#  seaice_gland5min
#execs:
# cscore_edge
# find_edge_nsidc
# find_edge_ncep
# find_edge_ims
# solo_ncep

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

def solo_score(fcst, fdate):
  if (fcst == "nsidc"): return 0
  fname = fcst+"."+fdate.strftime("%Y%m%d")
  if (os.path.exists(fname)):
    cmd = (exdir + "solo_" +fcst+" "+fixdir+"seaice_gland5min "+fname)
    print("integrals for ",fcst)
    sys.stdout.flush()
    x = os.system(cmd)
    if (x != 0):
      print("command ",cmd," returned error code ",x)
    return x 
  else:
    print("could not find ",fname)
    return 1

def edge_score(fcst, fdate, obs, obsdate):
  retcode = int(0)
  fname   = fcst+"_edge."+fdate.strftime("%Y%m%d")
  obsname = obs +"_edge."+obsdate.strftime("%Y%m%d")
  outfile = ("edge." + fcst + "." + obs + "." +fdate.strftime("%Y%m%d") 
                + "."+obsdate.strftime("%Y%m%d") )
  #print('edge_score ',fname,' ',obsname,' ',outfile)
  if (os.path.exists(fname) and os.path.exists(obsname) and not 
      os.path.exists(outfile) ):
    cmd = (exdir + "cscore_edge "+fixdir+"seaice_alldist.bin "+fname+" "+obsname +
           " 50.0 > " + outfile )
    x = os.system(cmd)
    if (x != 0):
      print("command ",cmd," returned error code ",x)
      sys.stdout.flush()
      retcode += x

  return retcode

def score_nsidc(fcst_dir, nsidcdir, fdate, obsdate):
  retcode = int(0)
  vyear = int(obsdate.strftime("%Y"))

  valid_fname = fcst_dir+'ice'+obsdate.strftime("%Y%m%d")+'00.01.'+fdate.strftime("%Y%m%d")+'00.subset.nc'
  if (not os.path.exists(valid_fname) ):
    valid_fname = fcst_dir+'ice'+obsdate.strftime("%Y%m%d")+'00.01.'+fdate.strftime("%Y%m%d")+'00.nc'
    if (not os.path.exists(valid_fname)):
      print("cannot find forecast file for "+fdate.strftime("%Y%m%d") )
  
  if (os.path.exists(exdir + 'score_nsidc')):
    print("Have the fcst vs. nsidc scoring executable")
    sys.stdout.flush()
    pole="north"
    ptag="n"
    #obsname = (nsidcdir + pole + str(vyear) + "/seaice_conc_daily_"+ptag+"h_f17_"+
    #                    obsdate.strftime("%Y%m%d")+"_v03r01.nc" )
    obsname = nsidc_name(pole, obsdate, nsidcdir)

    cmd = (exdir+"score_nsidc "+valid_fname+" "+obsname+ " "+fixdir+"skip_hr" + " > score."+
                ptag+"."+obsdate.strftime("%Y%m%d")+"f"+fdate.strftime("%Y%m%d")+".csv")
    x = os.system(cmd)
    if (x != 0):
      print("command ",cmd," returned error code ",x)
      retcode += x

#    pole="south"
#    ptag="s"
#    obsname = nsidc_name(pole, obsdate, nsidcdir)

  else:
    print("No score_nsidc executable")
    sys.stdout.flush()
    retcode += 1

  return retcode

#---------------------------- Begin program ---------------------


# dates, times -- initial date/time, verification date-time, or initial, 
#     lead range, and delta

#the +1 is for the command name itself, which is sys.argv[0]
if (len(sys.argv) == 3+1):
  print("Initial date and verification time")
  sys.stdout.flush()
  initial_date = parse_8digits(sys.argv[1])
  valid_date   = parse_8digits(sys.argv[2])
  fcst_dir     = sys.argv[3]
  single = True
  print(initial_date, " ", valid_date)
  sys.stdout.flush()
elif (len(sys.argv) == 4+1):
  initial_date = parse_8digits(sys.argv[1])
  lead         = int(sys.argv[2])
  dt       = datetime.timedelta(int(sys.argv[3]));
  fcst_dir = sys.argv[4]
  single = False
#RG Note: a timedelta is days and hh:mm:ss, fix arguments to handle 
#         hours as a delta
  print("Date, max lead, delta", initial_date," ",lead," ", dt)
  sys.stdout.flush()
else:
  print("wrong number of arguments")
  raise NotImplementedError('need 3 or 4 args, last being forecast directory')

#===============================================================================
#If a single verification, then one thing, else, create many single verifications:
if (single):
#IMS:
  if (imsverf): 
    x = get_ims(initial_date, dirs['imsdir'])
    if (x != 0):
      print("could not get file for ims verification, turning off imsverf\n")
      imsverf = False
    x = get_ims(valid_date, dirs['imsdir'])
    if (x != 0):
      print("could not get file for ims verification, turning off imsverf\n")
      imsverf = False
#NCEP -- grib/grib2
  if (ncepverf):
    x = get_ncep(initial_date, valid_date, dirs['ncepdir'])
    if (x != 0):
      print("could not get file for ncep verification, turning off ncepverf\n")
      ncepverf = False
#NSIDC -- netcdf
  if (nsidcverf):
    x = get_nsidc(initial_date, valid_date, dirs['nsidcdir'])
    if (x != 0):
      print("could not get file for nsidc verification, turning off nsidcverf\n")
      nsidcverf = False

  x = get_obs(initial_date, valid_date,
         imsverf, ncepverf, nsidcverf, dirs['imsdir'], dirs['ncepdir'], 
               dirs['nsidcdir'])
  if (x != 0):
    print("get_obs failed for ",initial_date.strftime("%Y%m%d")," ", valid_date.strftime("%Y%m%d")," ",x)
    obs = False
  else:
    obs = True

#Model Forecast
  x = get_fcst(initial_date, valid_date, fcst_dir)
  if (x != 0):
    print("get_fcst failed for ",initial_date.strftime("%Y%m%d")," ", valid_date.strftime("%Y%m%d")," ",x)
    fcst = False
  else:
    fcst = True

  #now call verification with dirs, fcst, verf logicals
  #print("working with observed data \n")
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
    if (imsverf): edge_score("ncep", valid_date, "ims", valid_date)
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
    

    print("\n")
    sys.stdout.flush()

else:
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

