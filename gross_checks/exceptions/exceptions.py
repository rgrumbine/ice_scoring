'''
Search within given bounding curves to find exceptions to limits
Robert Grumbine
'''
import sys

# Multiple inheritance from both bounds (value limits) and curves (domains)
from bounders import *
from curves import *
from regions import *

# ------------------- get regions  -----------------------------------
regions = []
f = open(sys.argv[1], 'r', encoding='utf-8')
for line in f:
  x = region(line)
  regions.append(x)
f.close()

nexcept = len(regions)
print("have ",len(regions)," regions to work with", flush=True)
counter = np.zeros(len(regions))

#in region, in bounds -------------------------------------------------
f = open(sys.argv[2], 'r', encoding='utf-8')
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
  for i in range(0, nexcept):
    if (regions[i].is_ok(pt, value, param)):
      ok = True
      counter[i] += 1

    if (ok):
      break

  if (not ok):
    badcount += 1
    if (badcount % freq == 0):
      print(line,end="",flush=True)
    else:
      print(line,end="")

# Write out summary --------------------------------------------------------
print(flush=True)
for i in range(0, len(regions)):
  if (int(counter[i]) > 0):
    #print("{:2d}".format(i), (int(counter[i])), regions[i].param, regions[i].name)
    print(f"{i:2d}", (int(counter[i])), regions[i].param, regions[i].name)
