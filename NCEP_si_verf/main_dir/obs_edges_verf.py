import os
import sys
import datetime

#Arguments:
#   start_date verification_date forecast_dir_path

#debug2: print("just imported systems",flush=True)

# imported by platforms:  from eval_env import *
from platforms import *
from verf_files import *
#debug2: print("imported platforms and verf_files",flush="True")

##################### ------------- 
#--------------- Utility Functions --------------------------------
x = runtime_environment("","","")

if (x.ok_env() == 0):
  print("eval env is ok",flush=True)
else:
  print("problem with eval env",flush=True)
  print("exbase, dir, fixdir: ",x.exbase, x.exdir, x.fixdir, flush=True)
  exit(1)

exbase = x.exbase
exdir  = x.exdir
fixdir = x.fixdir
#debug: print("exbase, exdir, fixdir: ",exbase, exdir, fixdir)

del x

# variables defined in platorms
edgedir   = dirs['edgedir']
imsdir    = dirs['imsdir']
ncepdir   = dirs['ncepdir']
nsidcdir  = dirs['nsidcdir']
osisafdir = dirs['osisafdir']

#------------------------------------------------------------------

from scores import *
#debug2: print("imported scores module",flush="True")

#====================================================================
#---------------------------- Begin program -------------------------
#If a single verification, then one thing, else, create many single verifications:
dt = datetime.timedelta(1)
#start = parse_8digits(sys.argv[1])
#end   = parse_8digits(sys.argv[2])
fcst_dir = sys.argv[1] + "/" + sys.argv[2] + "/"
start = parse_8digits(sys.argv[2])
fcst_len = int(sys.argv[3])

#debug: print("exdir, edgedir, fixdir",exdir, edgedir, fixdir, flush=True)
#debug: print(start, end, fcst_dir, flush=True)

lead = 1
if (fcst_len > 1):
  end = start + fcst_len*dt
  print("new end = ",end)
else:
  print("end = ",end)

#while (start < end):
while (lead <= fcst_len ):

  valid = start + lead*dt
  imsverf   = False
  ncepverf  = False
  osiverf   = False
  nsidcverf = True
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
  if (nsidcverf):
    x = get_nsidc(start, valid, dirs['nsidcdir'])
    if (x != 0):
      print("could not get files for nsidc verification, turning off nsidcverf\n",flush=True)
      nsidcverf = False
    if (not nsidcverf):
      print("nsidc fail: ",dirs['nsidcdir'], start, valid)
      exit(1)

  #OSI-SAF -- netcdf

  # Model Forecast:
  if (fcstverf):
    x = get_fcst(start, valid, fcst_dir)
    if (x != 0):
      print("could not get files for forecast output",flush=True)
      fcstverf = False
      exit(1)

  print(flush=True)

  #now call verification with dirs, fcst, verf logicals
  #debug print("setup_verf working with observed data \n", flush=True)
  if (imsverf):
    ims_edge(start.strftime("%Y%m%d"), dirs['imsdir'])
    ims_edge(valid.strftime("%Y%m%d"), dirs['imsdir'])
    edge_score("ims", start, "ims", valid, exdir, fixdir)
  if (ncepverf):
    print("on ncepverf ",start, valid, dirs['ncepdir'], flush=True)
    ncep_edge(start.strftime("%Y%m%d"), dirs['ncepdir'])
    ncep_edge(valid.strftime("%Y%m%d"), dirs['ncepdir'])
    edge_score("ncep", start, "ncep", valid, exdir, fixdir)
    if (imsverf): 
      edge_score("ncep", valid, "ims", valid, exdir, fixdir)
      edge_score("ims", valid, "ncep", valid, exdir, fixdir)
  if (nsidcverf):
    nsidc_edge(start.strftime("%Y%m%d"), 0.40, dirs['nsidcdir'], exdir, fixdir)
    nsidc_edge(valid.strftime("%Y%m%d"), 0.40, dirs['nsidcdir'], exdir, fixdir)
    edge_score("nsidc_north", start, "nsidc_north", valid, exdir, fixdir)
    if(imsverf): edge_score("nsidc_north", valid, "ims", valid, exdir, fixdir)
    if(ncepverf): edge_score("nsidc_north", valid, "ncep", valid, exdir, fixdir)
  #if (osiverf):
  #  osi_edge(start.strftime("%Y%m%d"))
  #  osi_edge(valid.strftime("%Y%m%d"))
  #  edge_score("osi", start, "osi", valid, exdir, fixdir)
  #  if (imsverf):
  #  if (ncepverf):

  if (fcstverf):
    #fcst_edge(start.strftime("%Y%m%d"), 0.40, fcst_dir)
    #fcst_edge(valid.strftime("%Y%m%d"), 0.40, fcst_dir)

    #debug: print("calling fcst_edge",start.strftime("%Y%m%d"), valid.strftime("%Y%m%d"), fcst_dir, fixdir, exdir, flush=True)
    fcst_edge(start.strftime("%Y%m%d"), valid.strftime("%Y%m%d"), fcst_dir, fixdir, exdir)

    #debug: print("calling fcst edge_score ","fcst", start, "fcst", valid, exdir, fixdir, flush=True)
    edge_score("fcst", start, "fcst", valid, exdir, fixdir)

    if (nsidcverf):
      #debug: print("calling edge score for nsidc_north v. fcst",flush=True)
      edge_score("fcst",valid, "nsidc_north",valid, exdir, fixdir)
      edge_score("nsidc_north",valid, "fcst",valid, exdir, fixdir)
    if (imsverf):
      edge_score("fcst",valid, "ims",valid, exdir, fixdir)
      edge_score("ims",valid, "fcst",valid, exdir, fixdir)
    if (ncepverf):
      edge_score("fcst",valid, "ncep",valid, exdir, fixdir)
      edge_score("ncep",valid, "fcst",valid, exdir, fixdir)


  print("\n", flush=True)
  #start += dt
  lead += 1

