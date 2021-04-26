#class for dealing with bounding curves

#Robert Grumbine
#26 April 2021

# RG: add lightweight export to kml, import from kml
# RG: add bounding box to curve initialization
# RG: learn to deal with crossing dateline / variant longitude ranges 
#        -- currently expect +- 180.0

#points are defined (lon, lat, ...)
class curve :
  def __init__(self, name="NULL"):
    self.name = name

  def read_curve(self, fname):
    self.points = []
    try:
      file = open(fname,"r")
    except:
      print("Could not open curve file ",fname," exiting")
      exit(1)

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
    x = inside(pt, self.points, self.npts)
    return(x != 0)


#RG utility -- is point inside bounding curve
# derived from C++ implementation
def isleft(p0, p1, p2):
  tmp = (p1[0]-p0[0]) * (p2[1]-p0[1]) - (p2[0] - p0[0])*(p1[1]-p0[1])
  if (tmp > 0):
    return 1
  elif (tmp < 0):
    return -1
  else:
    return 0

def inside(x, curve, npts):

  unclosed = False
  if (curve[0][0] != curve[npts-1][0]  or
      curve[0][1] != curve[npts-1][1] ):
    print("did not close, add extra point for ",curve.name)
    exit(1)

  wn = 0
  for i in range(0,npts-1):
    if (curve[i][0] <= x[0]):
      if (curve[i+1][0] > x[0]):
        if (isleft(curve[i], curve[i+1], x) > 0):
          wn += 1
    else:
      if (curve[i+1][0] <= x[0]):
        if (isleft(curve[i], curve[i+1], x) < 0):
          wn -= 1

  return wn
