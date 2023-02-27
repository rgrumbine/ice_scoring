import sys
import os
import datetime

#Roughly (very) 1 year per hour on wcoss2

#convert to a python script that will compare original and fcst N days later
#--------------- Utility Functions --------------------------------
def parse_8digits(tag):
  tmp = int(tag)
  (yy,mm,dd) = (int(int(tmp)/10000),int((int(tmp)%10000)/100),int(tmp)%100)
  tag_out = datetime.date(int(yy), int(mm), int(dd))
  return tag_out
#------------------------------------------------

obsdir = os.environ['OBSDIR']
fixdir = os.environ['FIXDIR']
exdir  = os.environ['EXDIR']

day   = datetime.timedelta(1)
start = parse_8digits(sys.argv[1])
end   = datetime.date.today()
lead  = int(sys.argv[2])
dt    = day*lead

for i in range(0,4*365+1):
  fdate = start + dt
  if (start >= end):
      break

  sname = obsdir+"/cleaned/s."+start.strftime("%Y%j")+".beta"
  fname = obsdir+"/cleaned/s."+fdate.strftime("%Y%j")+".beta"
  oname = "persist/nic_v_nic."+"{:d}".format(lead)+"/score.s."+start.strftime("%Y%j") 
  if (os.path.exists(sname) and os.path.exists(fname) ):
    if (not os.path.exists(oname) ):
      os.system("$EXDIR/cscore_edge $FIXDIR/seaice_alldist.bin "+sname+" "+fname+" 50.0 > "+oname)
  else:
    print("missing at least one of ",sname, fname)

  sname = obsdir+"/cleaned/n."+start.strftime("%Y%j")+".beta"
  fname = obsdir+"/cleaned/n."+fdate.strftime("%Y%j")+".beta"
  #oname = "score.n."+start.strftime("%Y%j") 
  oname = "persist/nic_v_nic."+"{:d}".format(lead)+"/score.n."+start.strftime("%Y%j") 
  if (os.path.exists(sname) and os.path.exists(fname) ):
    if (not os.path.exists(oname) ):
      os.system("$EXDIR/cscore_edge $FIXDIR/seaice_alldist.bin "+sname+" "+fname+" 50.0 > "+oname)
  else:
    print("missing at least one of ",sname, fname)

  start += day
