# Multiple inheritance from both bounds (value limits) and curves (domains)
from bounders import *
from curves import *

class exception(curve, bounds) :

  #the line is a character string with the name of the area, the parameter, and its allowed bounds
  def __init__(self, line):
    words = line.split()
    if (len(words) < 6):
      print("not enough elements in line, can't initialize exception class member", line)
      exit(1)
 
    self.name = words[0]
    fname = self.name +".curve"
    # RG: put in curves class
    # RG: throw exception if can't open file
    # RG: throw exception if can't read from file (empty or no points)
    self.read_curve(fname)

    # from class bounds
    self.set(words[1], words[2], words[3], words[4], words[5])

  def is_ok(self, pt, value, param = "NULL"):
    tmp = self.inside(pt)         # is the point inside the curve?
    t2  = self.ptinbounds(value)  # is it out in bounds?
    if (param != "NULL"):
      return (tmp and t2) and (param == self.param)    # is it the right parameter?
    return(tmp and t2)

def any_ok(exceptions, pt, value, param = "NULL"):
  any = False
  for i in range(0, len(exceptions)):
    any = any or exceptions[i].is_ok(pt, value, param)
  return any

# ------------------- demonstration -----------------------------------
f = open("exceptions.file")
exceptions = []
for line in f:
  x = exception(line)
  exceptions.append(x)
print("have ",len(exceptions)," exceptions to work with")

param = "hs_h"
#param = "SSS"
print("string test, should be true",exceptions[0].param == "hs_h")

#in region, in bounds -------------------------------------------------
pt = (-5.0, 75.0)
value = 1.8
print( exceptions[0].inside(pt), exceptions[0].ptinbounds(value), exceptions[0].is_ok(pt, value, param) )

#in region, out of bounds
pt = (-5.0, 75.0)
value = 2.8
print( exceptions[0].is_ok(pt, value, param))

#not in region, in bounds if it were:
pt = (-5.0, 35.0)
value = 1.8
print( exceptions[0].is_ok(pt, value, param))

# Do it in a Single call: ---------------------------------------------
# Try a run through all the exceptions and see if this point and value are ok
pt = (-5.0, 75.0)
value = 1.8

print("are any ok: ",any_ok(exceptions, pt, value, param) )

# Manual loop:
for i in range(0, len(exceptions)):
  if (exceptions[i].is_ok(pt, value, param)):
    print(exceptions[i].name, " is ok with this location and value ",pt, value, param)

