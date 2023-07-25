import os

"""
Check for all the environment declarations and files needed

"""

print("at top level", flush=True)

class runtime_environment:
  exbase = ""
  exdir = ""
  fixdir = ""

  def __init__(self, exbase, exdir, fixdir):
    self.exbase = exbase
    self.exdir  = exdir
    self.fixdir = fixdir

  def ok_env(self):
    
    print("entered ok_env", flush=True)
  
  #--------------- Package python Checks  --------------------------------
  # verf_files, platforms, scores
  #
  # os, sys, datetime
  #--------------- Environment Checks  --------------------------------
    try:
      exbase = os.environ['EXBASE']
    except:
      print("EXBASE was not defined, running with current working directory",flush=True)
      exbase = "."
    
    exdir  = exbase+"/exec/"
    fixdir = exbase+"/fix/"

    self.exbase = exbase
    self.exdir  = exdir
    self.fixdir = fixdir
  
    for p in (exbase, exdir, fixdir):
      if (not os.path.exists(p)):
        print("could not find directory, exiting ",p,flush=True)
        print("check eval: exbase, exdir, fixdir = ","\n",exbase,"\n", 
                    exdir, "\n",fixdir, flush=True)
        return 1
    
    #fixed files:
    #  seaice_alldist.bin
    #  seaice_gland5min
    for f in ( 'seaice_alldist.bin',  'seaice_gland5min'):
      if (not os.path.exists(fixdir+f)):
        print("could not find fixed file ",fixdir+f,flush=True)
        return 1
    
    #execs:
    for f in ('cscore_edge', 'find_edge_nsidc_north', 'find_edge_ncep', 
              'find_edge_ims', 'solo_ncep'):
      if (not os.path.exists(exdir+f)):
        print("could not find executable ",exdir+f,flush=True)
        return 1
  
    return 0
  
#--------------- Utility Functions --------------------------------
