# Multiple inheritance from both bounds (value limits) and curves (domains)
from bounders import *
from curves import *

from regions import *

# ------------------- demonstration -----------------------------------
f = open("exceptions.file")
regions = []
for line in f:
  x = region(line)
  regions.append(x)
print("have ",len(regions)," regions to work with")

param = "hs_h"
#param = "SSS"
print("string test, should be true",regions[0].param == "hs_h")

#in region, in bounds -------------------------------------------------
pt = (-5.0, 75.0)
value = 1.8
print( regions[0].inside(pt), regions[0].ptinbounds(value), regions[0].is_ok(pt, value, param) )

#in region, out of bounds
pt = (-5.0, 75.0)
value = 2.8
print( regions[0].is_ok(pt, value, param))

#not in region, in bounds if it were:
pt = (-5.0, 35.0)
value = 1.8
print( regions[0].is_ok(pt, value, param))

# Do it in a Single call: ---------------------------------------------
# Try a run through all the regions and see if this point and value are ok
pt = (-5.0, 75.0)
value = 1.8

print("are any ok: ",any_ok(regions, pt, value, param) )

# Manual loop:
for i in range(0, len(regions)):
  if (regions[i].is_ok(pt, value, param)):
    print(regions[i].name, " is ok with this location and value ",pt, value, param)

