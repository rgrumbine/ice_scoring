import os
import sys
import datetime

#Arguments:
#   start_date verification_date forecast_dir_path

from platforms import *

from verf_files import *

##################### ------------- 
#--------------- Environment Checks  --------------------------------

#debug print("setup_verf: exbase, exdir, fixdir = ","\n",exbase,"\n", exdir, "\n",fixdir, flush=True)
for p in (exbase, exdir, fixdir):
  if (not os.path.exists(p)):
    print("could not find ",p,flush=True)
    exit(1)

#fixed files:
#  seaice_alldist.bin
#  seaice_gland5min
for f in ( 'seaice_alldist.bin',  'seaice_gland5min'):
  if (not os.path.exists(fixdir+f)):
    print("could not find ",fixdir+f,flush=True)
    exit(1)

#execs:
for f in ('cscore_edge', 'find_edge_nsidc_north', 'find_edge_ncep', 'find_edge_ims', 'solo_ncep'):
  if (not os.path.exists(exdir+f)):
    print("could not find ",exdir+f,flush=True)
    exit(1)

#debug exit(0)
#------------------------------------------------------------------
#--------------- Utility Functions --------------------------------

def solo_score(fcst, fdate, fout = sys.stdout ):
"""
  solo_score is items that can be computed with just the given
  forecast, on a given date
  So far, just the area and extent integrals
"""

  if (fcst == "nsidc"): return 0
  fname = fcst+"."+fdate.strftime("%Y%m%d")
  if (os.path.exists(fname)):
    cmd = ('' +exdir + "solo_" +fcst+" "+fixdir+"seaice_gland5min "+fname)
    print("integrals for ",fcst, fdate.strftime("%Y%m%d")," ", end="", flush=True)
    sys.stdout.flush()
    x = os.system(cmd)
    if (x != 0):
      print("command ",cmd," returned error code ",x, flush=True)
    return x 
  else:
    print("could not find ",fname, flush=True)
    return 1

#====================================================================
#---------------------------- Begin program -------------------------
dt = datetime.timedelta(1)
start = parse_8digits(sys.argv[1])
end   = parse_8digits(sys.argv[2])
#debug: print(start, end, flush=True)

lead = 1

while (start < end):

  valid = start + lead*dt

  #-------------------------------------- Observation Suite ------
  imsverf   = True
  ncepverf  = True
  osiverf   = False
  nsidcverf = False
  #IMS:
  if (imsverf): 
    x = get_ims(start, dirs['imsdir'])
    if (x != 0):
      print("could not get initial file for ims verification, turning off imsverf\n", flush=True)
      imsverf = False
    x = get_ims(valid, dirs['imsdir'])
    if (x != 0):
      print("could not get valid date file for ims verification, turning off imsverf\n", flush=True)
      imsverf = False
  if (not imsverf):
    print("ims fail: ",dirs['imsdir'], start, valid)

  #NCEP -- grib/grib2
  if (ncepverf):
    x = get_ncep(start, valid, dirs['ncepdir'])
    if (x != 0):
      print("could not get files for ncep verification, turning off ncepverf\n",flush=True)
      ncepverf = False
  if (not ncepverf):
    print("ncep fail: ",dirs['ncepdir'], start, valid)

  #NSIDC -- netcdf
  if (nsidcverf):
    x = get_nsidc(start, valid, dirs['nsidcdir'])
    if (x != 0):
      print("could not get files for nsidc verification, turning off nsidcverf\n",flush=True)
      nsidcverf = False
  #if (not nsidcverf):
  #  print("nsidc fail: ",dirs['nsidcdir'], start, valid)
  #  exit(1)

  #OSI-SAF -- netcdf
  if (osiverf):
    x = get_nsidc(start, valid, dirs['osisafdir'])
    if (x != 0):
      print("could not get files for osisaf verification, turning off osisaf\n",flush=True)
      osiverf = False
      
  sys.stdout.flush()

  #-- END ------------------------------- Observation Suite ------

  #now call verification with dirs, fcst, verf logicals

  #debug print("setup_verf working with observed data \n", flush=True)
  if (imsverf):
    solo_score("ims", valid)
  if (ncepverf):
    solo_score("ncep", valid)
  if (nsidcverf):
    solo_score("nsidc", valid) #-- still to work out NH/SH vs. single input
  if (osiverf):
    solo_score("osi",valid)

  print("\n", flush=True)
  start += dt

  #sys.stdout.flush()
