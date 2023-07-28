"""
  This function computes the modified Hausdorff distance between two sets
  P(n,k),Q(m,k) entered as matrices with vectors (points) in the rows, i.e.
  each row represent a vector in a k-dimensional space
  with dimension k -  constant 
  Note that if geographical coordinates are used and 
  converted to cartesian, k = 2 is required
  for geogr coord, first index = longitude, 2nd = latitude

  Assumed that k<n, and k<m

  The number of vectors n and m can be different
  MHD improves over its
  predecessor (classic Hausdorff Distance)
  by being much less sensitive to outlier points.  The function
  is defined by
 
  d_MH(P,Q) = max{1/|P|\sum_{p\in P}d(p,Q),1/|Q|\sum_{q\in Q}d(q,P)}
 
  where d(p,Q) = min_{q\in Q}d(p,q), and similarly for d(P,q).
 
  The function is not a true topological metric since it fails the triangle
  inquality requirement.  In practice, this does not appear to be a
  problem.  Indeed, the function corresponds strongly with the human
  perception of shape.
 
  Reference: 
  "A Modified Hausdorff Distance for Object Matching," Dubuisson
    & Jain.  Proc. International Conference on Pattern Recognition,
    Jerusalem, Israel.  1994.
  Dukhovskoy, D.S.,, J. Ubnoske, E. Blanchard-Wrigglesworth, H.R. Hiester, 
    A. Proshutinsky, 2015. Skill metrics for evaluation and comparison 
    of sea ice models. J. Geophys. Res., 120, , doi:10.1002/2015JC010989

  P,Q can be in any units
  if P,Q are geogr. coord, its better to convert
              them into cartesian x,y (km) - use option 'geo2cart'
 
  NOAA NWS NCEP EMC
  Dmitry Dukhovskoy
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
import importlib

sys.path.append('/home/ddmitry/codes/MyPython')
import mod_misc1 as msc
importlib.reload(msc)
from mod_misc1 import dist_sphcrd as dstgeo

plt.ion()
def modifHD(P,Q,geo2cart=False):
  if not isinstance(P,np.ndarray):
    raise Exception("array P should be numpy ndarry ")

  if not isinstance(Q,np.ndarray):
    raise Exception("array Q should be numpy ndarry ")

  nP = P.shape[0]
  kP = P.shape[1]

  nQ = Q.shape[0]
  kQ = Q.shape[1]

# Assuming k<n 
# Transpose to have vectors in rows if needed:
  if nP < kP:
    P = P.transpose()
    nP = P.shape[0]
    kP = P.shape[1]

  if nQ < kQ:
    Q = Q.transpose()
    nQ = Q.shape[0]
    kQ = Q.shape[1]

  if not kQ == kP:
    raise Exception("Space dimensions P and Q should match {0} {1}".format(kP,kQ))

  if geo2cart and not kP == 2:
    raise Exception("For geogr. coordinates space dim should be 2, k={0}".\
                    format(kP))
  print('Computing MHD P={0}x{1}, Q={2}x{3}'.format(nP,kP,nQ,kQ))

# Check coordinates:
  for kk in range(kP):
    amin = np.min(P[:,kk])
    amax = np.max(P[:,kk])
    print('Dim {0} min/max coord= {1}/{2}'.format(kk+1,amin,amax))

# Convert to cartesian coord if needed
  if geo2cart:
    x0 = P[0,0]
    y0 = P[0,1]

    ix     = np.where(P[:,0] < x0)
    iy     = np.where(P[:,1] < y0)
    Y0     = P[:,0]*0.+y0
    X0     = P[:,0]*0.+x0
    px     = dstgeo(y0,x0,Y0,P[:,0])*1.e-3  # m --> km
    py     = dstgeo(y0,x0,P[:,1],X0)*1.e-3  # m --> km
    px[ix] = -px[ix]
    py[iy] = -py[iy]

    ix     = np.where(Q[:,0] < x0)
    iy     = np.where(Q[:,1] < y0)
    Y0     = Q[:,0]*0.+y0
    X0     = Q[:,0]*0.+x0
    qx     = dstgeo(y0,x0,Y0,Q[:,0])*1.e-3  # m --> km
    qy     = dstgeo(y0,x0,Q[:,1],X0)*1.e-3  # m --> km
    qx[ix] = -qx[ix]
    qy[iy] = -qy[iy]

#    px = np.expand_dims(px,axis=1)
#    py = np.expand_dims(py,axis=1)
    P = np.stack((px,py), axis=1)
    Q = np.stack((qx,qy), axis=1)

# Compute inter-point distance matrix 
  ipdm = calc_ipdm(P,Q)
  dist_pQ = np.min(ipdm, axis=1) # Min dist from p to Q
  dist_Pq = np.min(ipdm, axis=0) # min dist from q to P

  dP2Q = 1./nP*np.sum(dist_pQ)
  dQ2P = 1./nQ*np.sum(dist_Pq)
  MHD = max(dP2Q, dQ2P)

  return MHD

def calc_ipdm(P,Q):
  """
  Compute inter-point data matrix
  for 2 arrays P and Q
  sqrt of 2-norm is computed
  vectors (points) are in the rows
  Algorithm can be optimized 
  and can be slow for large data sets
  """
  nP = P.shape[0]
  kP = P.shape[1]

  nQ = Q.shape[0]
  kQ = Q.shape[1]

  IPDM = np.zeros((nP,nQ))
  for ii in range(nP):
    aa = P[ii,:]
#
# Difference
    DD = np.zeros((nQ))
    for kk in range(kQ):
      DD = DD + (Q[:,kk]-aa[kk])**2

    IPDM[ii,:]= np.sqrt(DD)

  return IPDM





