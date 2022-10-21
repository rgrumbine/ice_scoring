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
dt    = day*int(sys.argv[2])

#fdate = start + dt
#print(start.strftime("%j"))

for i in range(0,4*365-90):
  fdate = start + dt

  sname = obsdir+"/cleaned/s."+start.strftime("%Y%j")+".beta"
  fname = obsdir+"/cleaned/s."+fdate.strftime("%Y%j")+".beta"
  if (os.path.exists(sname) and os.path.exists(fname) ):
    os.system("$EXDIR/cscore_edge $FIXDIR/seaice_alldist.bin "+sname+" "+fname+" 50.0 > score.s."+start.strftime("%Y%j") )
  else:
    print("missing at least one of ",sname, fname)

  sname = obsdir+"/cleaned/n."+start.strftime("%Y%j")+".beta"
  fname = obsdir+"/cleaned/n."+fdate.strftime("%Y%j")+".beta"
  if (os.path.exists(sname) and os.path.exists(fname) ):
    os.system("$EXDIR/cscore_edge $FIXDIR/seaice_alldist.bin "+sname+" "+fname+" 50.0 > score.n."+start.strftime("%Y%j") )
  else:
    print("missing at least one of ",sname, fname)

  start += day
exit(0)
 
#    ./cscore_edge seaice_alldist.bin s.${y1}${ddd}.beta s.${y2}${ddd}.beta 50. > score.s.$y1$ddd
