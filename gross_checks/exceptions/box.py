import os
import sys

# Multiple inheritance from both bounds (value limits) and curves (domains)
#from bounders import *
#from curves import *
#from regions import *

# Read a gross check file and extract points inside a lat-lon box
# Arguments are filename, longitude bounds, latitude bounds (min, max)

#in box -------------------------------------------------
f = open(sys.argv[1])
lonmin = float(sys.argv[2])
lonmax = float(sys.argv[3])
latmin = float(sys.argv[4])
latmax = float(sys.argv[5])

badcount = 0
freq = 1000
ok = False

for line in f:
  if (not "pm" in line): #added to avoid having to pre-grep prior output
      continue
  words = line.split()
  param = words[0]
  tlon = float(words[3])
  if (tlon < -180.):
    tlon += 360.
  if (tlon >  180.):
    tlon -= 360.
  tlat = float(words[4])
  pt = (tlon, tlat)
  value = float(words[5])
  ok = False

  if (tlat >= latmin and tlat <= latmax and 
      tlon >= lonmin and tlon <= lonmax ):
    print(line,end="")
  
