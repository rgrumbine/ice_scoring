# Multiple inheritance from both bounds (value limits) and curves (domains)
from bounders import *
from curves import *

class region(curve, bounds) :

  #the line is a character string with the name of the area, the parameter, and its allowed bounds
  def __init__(self, line, base="curves/"):
    words = line.split()
    if (len(words) < 6):
      print("not enough elements in line, can't initialize region class member", line)
      exit(1)
 
    self.name = words[0]
    fname = base + self.name +".curve"
    # RG: throw exception if can't open file
    # RG: throw exception if can't read from file (empty or no points)
    self.read_curve(fname)

    # from class bounds
    self.set(words[1], words[2], words[3], words[4], words[5])

  def is_ok(self, pt, value, param = "NULL"):
    tmp = self.inside(pt)         # is the point inside the curve?
    t2  = self.ptinbounds(value)  # is it out in bounds?
    #debug print("region is_ok,",tmp,t2,param, self.param, flush=True) 
    if (self.param == "all"):
      return(tmp and t2)
    elif (param != "NULL"):
      return (tmp and t2) and (param == self.param)    # is it the right parameter?
    return(tmp and t2)

def any_ok(regions, pt, value, param = "NULL"):
  any = False
  for i in range(0, len(regions)):
    any = any or regions[i].is_ok(pt, value, param)
  return any

