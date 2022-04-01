import os
import sys
import datetime

if (not os.path.exists("skip_hr") ):
  print("could not find the required skip file")
  exit(1)

start = datetime.datetime(2022,3,20)
end   = datetime.datetime(2022,3,28)
dt    = datetime.timedelta(1)


dbase="/u/Robert.Grumbine/noscrub/rtofs_cice/prod/rtofs."

while (start <= end):
  dy  = start.strftime("%03j")
  print("dy = ",dy)
  valid    = start

  valid -= dt
  # looks like n00 refers to the day before the nominal analysis time

  for lead in ("n00", "f24", "f48", "f72", "f96", "f120", "f144", "f168", "f192"):
  #for lead in ("n00", "f24"):
    #lead = "f24"
    fname   = dbase+start.strftime("%Y%m%d")+"/rtofs_glo.t00z."+lead+".cice_inst"

    valid_dy = valid.strftime("%03j")

    crit = .01
    #while (crit <= 0.15+1.e-4): 
    for crit in (0.01, 0.03, 0.05, 0.10, 0.15 ):
      if (os.path.exists(fname)): 
        critstring="{:3.2f}".format(crit)
        print("critstring = ",critstring,lead, flush=True)
        outname = "rtofs.edge."+lead+"."+start.strftime("%Y%m%d")+critstring
        #debug print("outname=",outname, flush=True)
        if ( not os.path.exists(outname)):
          #find the edge:
          cmd="./find_edge_cice skip_hr "+ fname +" "+critstring+" > "+outname
          #debug print(cmd, flush=True)
          os.system(cmd)
    
        #score it:
        cmd = "./cscore_edge seaice_alldist.bin " + outname +" cleaned/n.2022"+valid_dy+".beta 50. > n."+valid_dy+"."+start.strftime("%Y%m%d")+critstring
        #debug print(cmd, flush=True)
        os.system(cmd)
        cmd = "./cscore_edge seaice_alldist.bin " + "cleaned/n.2022"+valid_dy+".beta " + outname + " 50. > nr."+valid_dy+"."+start.strftime("%Y%m%d")+critstring
        #debug print(cmd, flush=True)
        os.system(cmd)
      else:
        print("could not find model file:",fname, flush=True)
  
      #crit += 0.01

    valid += dt
  
  start += dt

