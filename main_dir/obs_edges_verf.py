import os
import sys
import datetime

#Arguments:
#   start_date verification_date forecast_dir_path

from platforms import *
from verf_files import *

##################### ------------- 
#--------------- Utility Functions --------------------------------

#debug print("setup_verf: exbase, exdir, fixdir = ","\n",exbase,"\n", exdir, "\n",fixdir, flush=True)
for p in (exbase, exdir, fixdir):
  if (not os.path.exists(p)):
    print("could not find ",p)
    exit(1)

#fixed files:
#  seaice_alldist.bin
#  seaice_gland5min
for f in ( 'seaice_alldist.bin',  'seaice_gland5min'):
  if (not os.path.exists(fixdir+f)):
    print("could not find ",fixdir+f)
    exit(1)

#execs:
for f in ('cscore_edge', 'find_edge_nsidc_north', 'find_edge_ncep', 'find_edge_ims' ):
  if (not os.path.exists(exdir+f)):
    print("could not find ",exdir+f)
    exit(1)

#------------------------------------------------------------------

from scores import *


#====================================================================
#---------------------------- Begin program -------------------------
#If a single verification, then one thing, else, create many single verifications:
dt = datetime.timedelta(1)
start = parse_8digits(sys.argv[1])
end   = parse_8digits(sys.argv[2])
fcst_dir = sys.argv[3] + "/" + sys.argv[4] + "/"
#debug: print(start, end, flush=True)

lead = 1

while (start < end):

  valid = start + lead*dt
  imsverf   = True
  ncepverf  = True
  osiverf   = False
  nsidcverf = False
  fcstverf  = True

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
  #if (nsidcverf):
  #  x = get_nsidc(start, valid, dirs['nsidcdir'])
  #  if (x != 0):
  #    print("could not get files for nsidc verification, turning off nsidcverf\n",flush=True)
  #    nsidcverf = False
  #if (not nsidcverf):
  #  print("nsidc fail: ",dirs['nsidcdir'], start, valid)
  #  exit(1)

  #OSI-SAF -- netcdf

  if (fcstverf):
    x = get_fcst(start, valid, fcst_dir)
    if (x != 0):
      print("could not get files for forecast output",flush=True)
      fcstverf = False

  print(flush=True)

  #now call verification with dirs, fcst, verf logicals
  #debug print("setup_verf working with observed data \n", flush=True)
  if (imsverf):
    ims_edge(start.strftime("%Y%m%d"), dirs['imsdir'])
    ims_edge(valid.strftime("%Y%m%d"), dirs['imsdir'])
    edge_score("ims", start, "ims", valid)
  if (ncepverf):
    print("on ncepverf ",start, valid, dirs['ncepdir'], flush=True)
    ncep_edge(start.strftime("%Y%m%d"), dirs['ncepdir'])
    ncep_edge(valid.strftime("%Y%m%d"), dirs['ncepdir'])
    edge_score("ncep", start, "ncep", valid)
    if (imsverf): 
      edge_score("ncep", valid, "ims", valid)
      edge_score("ims", valid, "ncep", valid)
  #if (nsidcverf):
  #  nsidc_edge(start.strftime("%Y%m%d"), 0.40, dirs['nsidcdir'] )
  #  nsidc_edge(valid.strftime("%Y%m%d"), 0.40, dirs['nsidcdir'] )
  #  edge_score("nsidc_north", start, "nsidc_north", valid)
  #  if(imsverf): edge_score("nsidc_north", valid, "ims", valid)
  #  if(ncepverf): edge_score("nsidc_north", valid, "ncep", valid)
  #if (osiverf):
  #  osi_edge(start.strftime("%Y%m%d"))
  #  osi_edge(valid.strftime("%Y%m%d"))
  #  edge_score("osi", start, "osi", valid)
  #  if (imsverf):
  #  if (ncepverf):

  if (fcstverf):
    fcst_edge(start.strftime("%Y%m%d"), 0.40, fcst_dir)
    fcst_edge(valid.strftime("%Y%m%d"), 0.40, fcst_dir)
    edge_score("fcst", start, "fcst", valid)
    if (imsverf):
      edge_score("fcst",valid, "ims",valid)
      edge_score("ims",valid, "fcst",valid)
    if (ncepverf):
      edge_score("fcst",valid, "ncep",valid)
      edge_score("ncep",valid, "fcst",valid)

    


  print("\n", flush=True)
  start += dt

