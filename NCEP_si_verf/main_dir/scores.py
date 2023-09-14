import os
import sys
import datetime

#Arguments:
#   start_date verification_date forecast_dir_path

from utility import *    # python utilities in mmablib

from platforms import *
from verf_files import *

##################### ------------- 
#--------------- Environment Checks  --------------------------------
# Check verf environment
# x = runtime_environment("","","")
#------------------------------------------------------------------

#--------------- Scoring Functions --------------------------------
"""
Edges
"""

def edge_score(fcst, fdate, obs, obsdate, exdir, fixdir):
  retcode = int(0)
  edgedir = dirs['edgedir']
  fname   = edgedir+fcst+"_edge."+fdate.strftime("%Y%m%d")
  obsname = edgedir+obs +"_edge."+obsdate.strftime("%Y%m%d")

  outfile = (edgedir + "edge." + fcst + "." + obs + "." +fdate.strftime("%Y%m%d") 
                + "."+obsdate.strftime("%Y%m%d") )

  #debug print('scores: edge_score ',fname,' ',obsname,' ',outfile, flush=True)

  if (os.path.exists(fname) and os.path.exists(obsname) and not 
      os.path.exists(outfile) ):
    cmd = ('time ' +exdir + "cscore_edge "+fixdir+"seaice_alldist.bin "+fname+" "+obsname +
           " 50.0 > " + outfile )
    #debug print("edge_score: ",cmd,flush=True)

    x = os.system(cmd)
    if (x != 0):
      print("command ",cmd," returned error code ",x, flush=True)
      retcode += x
  else :
    print("edge score skipping ",fname, obsname, outfile, flush=True)

  return retcode

#------------------------------------------------------------------
"""
  solo_score is items that can be computed with just the given
  forecast, on a given date
  So far, just the area and extent integrals
"""

def solo_score(fcst, fdate, fout = sys.stdout ):

  if (fcst == "nsidc"): return 0
  fname = fcst+"."+fdate.strftime("%Y%m%d")
  if (os.path.exists(fname)):
    cmd = ('' +exdir + "solo_" +fcst+" "+fixdir+"seaice_gland5min "+fname)
    print("integrals for ",fcst, fdate.strftime("%Y%m%d")," ", end="", flush=True)
    x = os.system(cmd)
    if (x != 0):
      print("command ",cmd," returned error code ",x, flush=True)
    return x 
  else:
    print("could not find ",fname, flush=True)
    return 1

#---------------------------------------------------------------------
"""
Evaluating the ice concentrations
"""
def score_nsidc(fcst_dir, nsidcdir, fdate, obsdate, exdir, fixdir):
  #debug: print("py entered score_nsidc",flush=True)
  retcode = int(0)
  vyear = int(obsdate.strftime("%Y"))

  if (vyear < 2010):
    print("Invalid verification year in obsdate, score_nsidc",obsdate, vyear, fdate)
    exit(1)

  #isolate forecast file name references to fcst_name:
  #debug: print("score_nsidc calling fcst_name",flush=True)
  valid_fname = fcst_name(obsdate, fdate, fcst_dir)

  #UFS style:

  #CICE consortium name:
  #valid_fname = fcst_dir+'iceh.'+obsdate.strftime("%Y")+'-'+obsdate.strftime("%m")+'-'+obsdate.strftime("%d")+".nc"

  if (not os.path.exists(valid_fname)):
    print("scores.py cannot find forecast file for "+fdate.strftime("%Y%m%d"),obsdate.strftime("%Y%m%d"), flush=True )
    retcode = int(1)
    return retcode

  exname = 'score_nsidc'
  if (os.path.exists(exdir + exname)):
    #debug print("setup_verf Have the fcst vs. nsidc scoring executable", flush=True)
    sys.stdout.flush()
    pole="north"
    ptag="n"
    obsname = nsidc_name(pole, obsdate, nsidcdir)

    cmd = (exdir+exname+" "+valid_fname+" "+obsname+ " "+fixdir+"skip_hr " +
           fixdir + "G02202-cdr-ancillary-nh.nc" +
           " > score."+ ptag+"."+obsdate.strftime("%Y%m%d")+"f"+
                                 fdate.strftime("%Y%m%d")+".csv"  )
    x = os.system(cmd)
    if (x != 0):
      print("\n\n command ",cmd,"\n returned error code ",x, flush=True)
      print("\n")
      print(exdir+exname, os.path.exists(exdir+exname))
      print(valid_fname, os.path.exists(valid_fname))
      print(obsname , os.path.exists(obsname))
      print(fixdir, os.path.exists(fixdir))
      print(fixdir+ "G02202-cdr-ancillary-nh.nc", os.path.exists(fixdir+ "G02202-cdr-ancillary-nh.nc"))
      print(exdir+"runtime.def ", os.path.exists(exdir+"runtime.def") )
      retcode += x

#    pole="south"
#    ptag="s"
#    obsname = nsidc_name(pole, obsdate, nsidcdir)

  else:
    print("No executable to score vs. nsidc", flush=True)
    retcode += 1

  return retcode


