import os
import sys
import datetime

fixdir = os.getenv('FIXDIR')
exdir  = os.getenv('EXDIR')
if (not os.path.exists(fixdir+"/skip_hr") ):
  print("could not find the required skip file")
  print("fixdir = ",fixdir)
  exit(1)

start = datetime.datetime(2022,1,31)
end   = datetime.datetime(2022,10,31)
dt    = datetime.timedelta(1)


dbase="/u/robert.grumbine/noscrub/model_intercompare/rtofs_cice/rtofs."

while (start <= end):
  dy  = start.strftime("%03j")
  print("dy = ",dy, flush=True)
  valid    = start

  valid -= dt
  # looks like n00 refers to the day before the nominal analysis time

  for lead in ("n00", "f24", "f48", "f72", "f96", "f120", "f144", "f168", "f192"):
  #for lead in ("n00", "f24"):
    #lead = "f24"
    fname   = dbase+start.strftime("%Y%m%d")+"/rtofs_glo.t00z."+lead+".cice_inst"

    valid_dy = valid.strftime("%03j")

    for crit in (0.01, 0.03, 0.05, 0.10, 0.15 ):
      if (os.path.exists(fname)): 
        critstring="{:3.2f}".format(crit)
        #debug print("critstring = ",critstring,lead, flush=True)
        outname = "rtofs_edges/rtofs.edge."+lead+"."+start.strftime("%Y%m%d")+critstring
        #debug print("outname=",outname, flush=True)
        if ( not os.path.exists(outname)):
          #find the edge:
          cmd=exdir+'/find_edge_cice '+fixdir+"/skip_hr "+ fname +" "+critstring+" > "+outname
          #debug print(cmd, flush=True)
          os.system(cmd)
    
        #score it:
        snamer = "rtofs_scores/nr."+valid_dy+"."+start.strftime("%Y%m%d")+critstring
        sname  = "rtofs_scores/n."+valid_dy+"."+start.strftime("%Y%m%d")+critstring

        if (not os.path.exists(sname)):
          cmd =  exdir+'/cscore_edge '+fixdir+'/seaice_alldist.bin ' + outname +' cleaned/n.2022'+valid_dy+'.beta 50. > '+sname
          #debug print(cmd, flush=True)
          os.system(cmd)

        if (not os.path.exists(snamer)):
          cmd =  exdir+'/cscore_edge '+fixdir+'/seaice_alldist.bin ' + 'cleaned/n.2022'+valid_dy+'.beta ' + outname + ' 50. > '+snamer
          #debug print(cmd, flush=True)
          os.system(cmd)
      else:
        print("could not find model file:",fname, flush=True)
  
    valid += dt
  
  start += dt

