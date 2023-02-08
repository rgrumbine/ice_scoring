import os
import sys
import datetime

#Arguments:
#   start_date verification_date forecast_dir_path

from verf_files import *
from platforms import *

##################### ------------- 
#--------------- Utility Functions --------------------------------
from scores import *

#---------------------------- Begin program ---------------------
# dates, times -- initial date/time, verification date-time, or initial, 
#     lead range, and delta

#the +1 is for the command name itself, which is sys.argv[0]
initial_date = parse_8digits(sys.argv[1])
valid_date   = parse_8digits(sys.argv[2])
fcst_dir     = sys.argv[3] 
fcst_dir     += "/"+sys.argv[1]
single       = True
#debug print("fcst_verf initial_date", valid_date, flush=True)

#===============================================================================
imsverf   = True
nsidcverf = True
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

#OSI-SAF
  #if (osiverf):
    #x = get_osisaf(initial_date, valid_date, dirs['osidir'])
    #if (x != 0):
    #  print("could not get file for osi verification, turning off osiverf\n",flush=True)
    #  osiverf = False

  obs = (nsidcverf or ncepverf or imsverf or osiverf)

#Get Model Forecast ---------------------------------------------
  x = get_fcst(initial_date, valid_date, fcst_dir)
  if (x != 0):
    print("get_fcst failed for ",initial_date.strftime("%Y%m%d")," ", 
           valid_date.strftime("%Y%m%d")," ",x, flush=True)
    fcst = False
    exit(1)
  else:
    #debug print("setup_verf have forecast ",initial_date.strftime("%Y%m%d")," ", valid_date.strftime("%Y%m%d")," ",x, flush=True)
    fcst = True

  print(flush=True)

#------------------------------------------------------------------

  #now call verification with dirs, fcst, verf logicals
  #debug print("setup_verf working with observed data \n", flush=True)
  solo = False
  edges = False
  conc  = True

  #debug: print("fcst = True, try scoring",flush=True)
  if (solo):
    solo_score("fcst", valid_date) # -- to be developed

  if (edges):
    fcst_edge(initial_date.strftime("%Y%m%d"), valid_date.strftime("%Y%m%d"), fcst_dir)
    if (imsverf):   
      #debug print("trying imsverf edge",flush=True)
      edge_score("fcst", valid_date, "ims", valid_date)
      edge_score("ims", valid_date, "fcst", valid_date)
    if (ncepverf):  
      #debug print("trying ncepverf edge",flush=True)
      edge_score("fcst", valid_date, "ncep", valid_date)
      edge_score("ncep", valid_date, "fcst", valid_date)
    if (nsidcverf): 
      #debug print("trying nsidcverf edge",flush=True)
      edge_score("fcst", valid_date, "nsidc_north", valid_date)
      edge_score("nsidc_north", valid_date, "fcst", valid_date)

  if (conc):
    #debug: print("pymain trying concentration verf",flush=True)
    if (nsidcverf): 
      score_nsidc(fcst_dir, dirs['nsidcdir'], initial_date, valid_date)
    #elif (ncepverf):
    #elif (osiverf):
    else:
      print("could not score concentration for ",fcst_dir, 
             dirs['nsidcdir'], initial_date, valid_date, flush=True)

  print("\n", flush=True)
