import os
import sys
import datetime

#Arguments:
#   start_date verification_date forecast_dir_path

from platforms import *
from verf_files import *

##################### ------------- 
#--------------- Environment Checks  --------------------------------
# Check verf environment

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
"""
Edges
"""

def edge_score(fcst, fdate, obs, obsdate):
  retcode = int(0)
  edgedir = dirs['edgedir']
  fname   = edgedir+fcst+"_edge."+fdate.strftime("%Y%m%d")
  obsname = edgedir+obs +"_edge."+obsdate.strftime("%Y%m%d")

  outfile = (edgedir + "edge." + fcst + "." + obs + "." +fdate.strftime("%Y%m%d") 
                + "."+obsdate.strftime("%Y%m%d") )

  #debug 
  print('scores: edge_score ',fname,' ',obsname,' ',outfile, flush=True)

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
def score_nsidc(fcst_dir, nsidcdir, fdate, obsdate):
  #debug: print("py entered score_nsidc",flush=True)
  retcode = int(0)
  vyear = int(obsdate.strftime("%Y"))

  #isolate forecast file name references to fcst_name:
  valid_fname = fcst_name(obsdate, fdate, fcst_dir)
  #UFS style:
  #valid_fname = fcst_dir+'ice'+obsdate.strftime("%Y%m%d")+'00.01.'+fdate.strftime("%Y%m%d")+'00.subset.nc'
  #CICE consortium name:
  #valid_fname = fcst_dir+'iceh.'+obsdate.strftime("%Y")+'-'+obsdate.strftime("%m")+'-'+obsdate.strftime("%d")+".nc"

  if (not os.path.exists(valid_fname)):
    print("scores.py cannot find forecast file for "+fdate.strftime("%Y%m%d"),obsdate.strftime("%Y%m%d"), flush=True )
    retcode = int(1)
    return retcode

  #exname = 'generic'
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


