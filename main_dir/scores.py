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
#--------------- Scoring Functions --------------------------------

def edge_score(fcst, fdate, obs, obsdate):
  retcode = int(0)
  edgedir = dirs['edgedir']
  fname   = edgedir+fcst+"_edge."+fdate.strftime("%Y%m%d")
  obsname = edgedir+obs +"_edge."+obsdate.strftime("%Y%m%d")

  outfile = (edgedir + "edge." + fcst + "." + obs + "." +fdate.strftime("%Y%m%d") 
                + "."+obsdate.strftime("%Y%m%d") )

  #debug print('setup_verf: edge_score ',fname,' ',obsname,' ',outfile, flush=True)

  if (os.path.exists(fname) and os.path.exists(obsname) and not 
      os.path.exists(outfile) ):
    cmd = ('time ' +exdir + "cscore_edge "+fixdir+"seaice_alldist.bin "+fname+" "+obsname +
           " 50.0 > " + outfile )
    #debug print("edge_score: ",cmd,flush=True)

    x = os.system(cmd)
    if (x != 0):
      print("command ",cmd," returned error code ",x, flush=True)
      retcode += x

  return retcode

#------------------------------------------------------------------

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

#---------------------------------------------------------------------
