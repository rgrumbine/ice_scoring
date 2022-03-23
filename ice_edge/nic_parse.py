import os
import sys
from math import *
import datetime

#Parse the nic ice edge file in to line segments
#line 1: NATICE ICE EDGE	DATE 20210325
#line 2: WGS84  DECIMAL DEGREES x 1000

#each line segment starts with 'LINE' and contains 1-4 locations
#  segment continues until next line that starts 'LINE'
#each location is in form 43279N145499E, where one divides by the 
#  scaling factor from line 2 of the file
#file ends with a line of '9999'

#class bundle (a bunch of segments)
#class segment (2-inf points)
# [], [].add

#class point
#  fn parse string
class point:

  def __init__(self, lat = 0.0, lon = 0.0):
    #print("pt init ",lat, lon)
    self.lat = lat
    self.lon = lon

#----------------------- for mapping --------------------------
class constants:
  rpd    = pi/180.
  kmtonm = 1./1.852

def rearth(lat):
  return (6378.137 - 21.385*sin(lat*constants.rpd) )

#haversine arcdis
#  http://www.movable-type.co.uk/scripts/gis-faq-5.1.html
#assumes lat lon in degrees, distance in km
def harcdis(pt1, pt2):

  dlon = pt2.lon - pt1.lon
  dlat = pt2.lat - pt1.lat
  mlat = (pt1.lat + pt2.lat)/2.

  a = sin(dlat*constants.rpd/2)**2 + cos(pt1.lat*constants.rpd)*cos(pt2.lat*constants.rpd)*sin(dlon*constants.rpd/2)**2
  c = 2.*asin(min(1.,sqrt(a)))

# approximating ellipsoidal flattening RG WGS84
#  return( c * (6378.137 - 21.385*sin(mlat*constants.rpd) ))
  return c*rearth(mlat)


#--------------------------------------------------------------

class segment:

  def __init__(self):
    self.pts = []
    #debug print("segment: ",len(self.pts), flush=True)

  def add(self, pt):
    if (len(self.pts) == 0):
      self.pts.append(pt)
    else:
      tmpn = point()
      x = harcdis(pt, self.pts[-1])
      #x  = 6.6
      #divide in to int(x)+1 pieces 
      n  = int(x)+1
      #debug print("begin",len(self.pts), " dist = ",x, n, flush=True )
      dx = (pt.lon - self.pts[-1].lon)/n
      dy = (pt.lat - self.pts[-1].lat)/n
      for i in range(1,n):
        tmpn = point(lon = self.pts[-1].lon + dx*i, lat = self.pts[-1].lat + dy*i)
        self.pts.append(tmpn)
      self.pts.append(pt)
      #debug print("add else ",pt.lat, pt.lon, tmpn.lat, tmpn.lon, flush=True)
    
    #debug print("segment: ",len(self.pts), flush=True)

  def print(self, fout=sys.stdout):
    print("printing, kmax = ",len(self.pts))
    for k in range (0,len(self.pts)):
      #print(k,self.pts[k].lat, self.pts[k].lon)
      print(self.pts[k].lon, self.pts[k].lat, file = fout)


class bundle:

  def __init__(self):
    self.segments = []

  def add(self, seg):
    self.segments.append(seg)

  def print(self, file="stdout"):
    for k in range (0,len(self.segments)):
      self.segments[k].print()


def parse_pt(beta):
#beta should be exactly 14 characters, including a leading space = len(beta)
  if (len(beta) != 14):
    print("beta wrong size: ",beta)
    exit(1)
  #debug print(beta[1:6], beta[6:7], beta[7:13], beta[13:14])
  p  = beta[6:7]
  l  = beta[13:14]
  lat = float(beta[1:6])
  lon = float(beta[7:13])
  lat /= scale
  lon /= scale
  if (p == "S"):
    lat *= -1.0
  if (l == "W"):
    lon *= -1.0
  x = point(lat, lon) 
  return(x)

def parse_line(line, bund1):
#Note: a space before each location, so, really, 14 characters
  loclen = 14
  x     = len(line) - 1 # skip eol characters from file read
  npts  = int(round(x/ loclen))
  start = x - npts* loclen
  nseg  = len(bund1.segments)
  #print("nseg = ",nseg, "start = ",start, npts, x, "char61 ",line[60:61])
  for k in range (0,int((x-start)/ loclen) ):
    e =  loclen*k
    #RG: revise to be k == 0 with 2 subcases, and then k != 0
    if (start == -1 and k == 0):
      pt = parse_pt(" "+line[0 : start+e+ loclen])
      bund1.segments[nseg-1].add(pt)
    elif (start == -1):
      pt = parse_pt(line[start+e : start+e+ loclen])
      bund1.segments[nseg-1].add(pt)
    elif (start > 0 and k == 0):
      #new segment -- add to bundle
      seg1 = segment()
      bund1.add(seg1)
      nseg = len(bund1.segments)
      pt = parse_pt(line[start+e : start+e+ loclen])
      bund1.segments[nseg-1].add(pt)
    else:
      pt = parse_pt(line[start+e : start+e+ loclen])
      bund1.segments[nseg-1].add(pt)



#---------------------------------------------------
#Live:
scale = 1000.
bund1 = bundle()

fin = open(sys.argv[1],"r")
#fin = open("a","r")
n = 0
for alpha in fin:
  if (n > 1):
    parse_line(alpha, bund1)
  n += 1

npts = 0
for k in range(0,len(bund1.segments)):
  npts += len(bund1.segments[k].pts)
  
print("found ",len(bund1.segments)," line segments, totalling ",npts," points")
bund1.print()
