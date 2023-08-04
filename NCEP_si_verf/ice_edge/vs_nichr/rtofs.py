import os
import sys
import datetime

#------------------------------------------------------------
"""
Requires environment to provide:
    variables FIXDIR, EXDIR
    data files  skip_hr, seaice_alldist.bin 
    executables cscore_edge, find_edge_cice

Currently hard codes (dbase) path to rtofs cice output directories

Robert Grumbine
27 July 2023
"""
#------------------------------------------------------------

fixdir = os.getenv('FIXDIR')
if (type(fixdir) == str ):
    print("fixdir = ",fixdir)
else:
    print("Could not find environment variable FIXDIR")
    exit(1)

exdir  = os.getenv('EXDIR')
if (type(exdir) == str):
    print("exdir = ",exdir)
else:
    print("Could not find environment variable EXDIR")
    exit(1)

if (not os.path.exists(fixdir+"/skip_hr") ):
  print("could not find the required skip file")
  print("fixdir = ",fixdir)
  exit(1)

dbase="/u/robert.grumbine/noscrub/model_intercompare/rtofs_cice/rtofs."

dt    = datetime.timedelta(1)
start = datetime.datetime(2023,1,1)
end   = datetime.datetime.today()
end  -= 8*dt
#end = datetime.datetime(2023,7,1)

#------------------------------------------------------------


while (start <= end):
  dy  = start.strftime("%03j")
  print("dy = ",dy, flush=True)
  valid    = start

  #valid -= dt
  # looks like n00 refers to the day before the nominal analysis time
  nlead=0
  for lead in ("n00", "f24", "f48", "f72", "f96", "f120", "f144", "f168", "f192"):
    fname   = dbase+start.strftime("%Y%m%d")+"/rtofs_glo.t00z."+lead+".cice_inst"

    valid_dy = valid.strftime("%03j")
    yy       = valid.strftime("%Y")

    for crit in (0.01, 0.03, 0.05, 0.10, 0.15 ):
      if (os.path.exists(fname)): 
        critstring="{:3.2f}".format(crit)
        #debug: print("critstring = ",critstring,lead, flush=True)
        outname = "rtofs_edges/rtofs.edge."+lead+"."+start.strftime("%Y%m%d")+critstring
        #debug: print("outname=",outname, flush=True)
        if ( not os.path.exists(outname)):
          #find the edge:
          cmd=exdir+'/find_edge_cice '+fixdir+"/skip_hr "+ fname +" "+critstring+" > "+outname
          #debug: print(cmd, flush=True)
          retval = os.system(cmd)
          if (retval != 0 ):
              print("Error ",retval,"in trying to run ",cmd)
              exit(2)
    
        #score it:
        snamer = "rtofs_scores/nr."+"{:1d}".format(nlead)+"."+start.strftime("%Y%m%d")+critstring
        sname  = "rtofs_scores/n."+"{:1d}".format(nlead)+"."+start.strftime("%Y%m%d")+critstring

        if (not os.path.exists(sname)):
          cmd =  exdir+'/cscore_edge '+fixdir+'/seaice_alldist.bin ' + outname +' cleaned/n.'+yy+valid_dy+'.beta 50. > '+sname
          #debug print(cmd, flush=True)
          os.system(cmd)

        if (not os.path.exists(snamer)):
          cmd =  exdir+'/cscore_edge '+fixdir+'/seaice_alldist.bin ' + 'cleaned/n.'+yy+valid_dy+'.beta ' + outname + ' 50. > '+snamer
          #debug print(cmd, flush=True)
          os.system(cmd)
      else:
        print("could not find model file:",fname, flush=True)
  
    valid += dt
    nlead += 1
  
  start += dt

