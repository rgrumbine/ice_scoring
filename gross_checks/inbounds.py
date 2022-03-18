import os
import sys

# Multiple inheritance from both bounds (value limits) and curves (domains)
from bounders import *
from curves import *
from regions import *

# ------------------- demonstration -----------------------------------
#print out things that _are_ in the bounds
f = open(sys.argv[1])
regions = []
for line in f:
  x = region(line)
  regions.append(x)
f.close()

nexcept = len(regions)
print("have ",len(regions)," regions to work with")
counter = np.zeros(len(regions))

ok = False

#in region, in bounds -------------------------------------------------
f = open(sys.argv[2])
badcount = 0
freq = 1000
for line in f:
  words = line.split()
  param = words[0]
  tlon = float(words[3])
  if (tlon < -180.):
    tlon += 360.
  tlat = float(words[4])
  pt = (tlon, tlat)
  value = float(words[5])
  ok = False
  for i in range(0, nexcept):
    if (regions[i].is_ok(pt, value, param)):
      ok = True
      counter[i] += 1
      print(line,end="")
      #print("curve ",i," is ok with this location and value ",pt, value, param)
    if (ok):
      break

