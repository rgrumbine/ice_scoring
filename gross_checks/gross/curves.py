'''
class for dealing with bounding curves
-- read_curve, inside (bool)

Robert Grumbine
26 April 2021
'''

import sys

# Notes for future
# RG: add lightweight export to kml, import from kml
# RG: add bounding box to curve initialization
# RG: learn to deal with crossing dateline / variant longitude ranges
#        -- currently expect +- 180.0

#points are defined (lon, lat, ...)
class curve :
  ''' class curve -- list of lon-lat points describing a bounding curve '''
  def __init__(self, name="NULL"):
    self.name = name

  def read_curve(self, fname):
    ''' curve.read_curve(fname) --- read in a curve from file fname '''
    self.points = []
    try:
      file = open(fname,"r",encoding='utf-8')
    except:
      print("Could not open curve file ",fname," exiting")
      sys.exit(1)

    count = 0
    for line in file:
      words = line.split()
      if (count == 0):
        self.name = words[0] #Allow extra comments after name
      else:
        m = (float(words[0]), float(words[1]))
        self.points.append(m)
      count += 1
    #Ensure closure:
    if (self.points[0] != self.points[len(self.points)-1]):
      m = self.points[0]
      self.points.append(m)
    self.npts = len(self.points)

  def inside(self, pt):
    ''' curve.inside(pt) -- is pt inside this curve? '''
    x = inside(pt, self.points, self.npts)
    return(x != 0)


#RG utility -- is point inside bounding curve
# derived from C++ implementation
def isleft(p0, p1, p2):
  ''' isleft(p0,p1,p2) -- is point p2 left of line between p1 and p0 '''
  tmp = (p1[0]-p0[0]) * (p2[1]-p0[1]) - (p2[0] - p0[0])*(p1[1]-p0[1])
  if (tmp > 0):
    return 1
  if (tmp < 0):
    return -1

  return 0

def inside(x, bcurve, npts):
  ''' inside(x, bcurve, npts) -- is point x inside the curve? '''
  unclosed = False
  if (bcurve[0][0] != bcurve[npts-1][0]  or
      bcurve[0][1] != bcurve[npts-1][1] ):
    print("did not close, add extra point for ",bcurve.name)
    sys.exit(1)

  wn = 0
  for i in range(0,npts-1):
    if (bcurve[i][0] <= x[0]):
      if (bcurve[i+1][0] > x[0]):
        if (isleft(bcurve[i], bcurve[i+1], x) > 0):
          wn += 1
    else:
      if (bcurve[i+1][0] <= x[0]):
        if (isleft(bcurve[i], bcurve[i+1], x) < 0):
          wn -= 1

  return wn
