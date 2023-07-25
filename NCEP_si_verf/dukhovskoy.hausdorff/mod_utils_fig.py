"""
  Functions for plotting and figure settings
"""
import os
import numpy as np
import matplotlib.pyplot as plt

def bottom_text(btx, pos=[0.1, 0.05], fsz=10):
  drr = os.getcwd()
  btnm = drr+'/'+btx
  plt.text(pos[0],pos[1],btnm,horizontalalignment='left',
         transform=plt.gcf().transFigure, fontsize=fsz)


def correct_evensp_grid(x, y):
  xcrct = x.copy()
  ycrct = y.copy()
  if x.ndim == 1:
    pass
  elif x.ndim == 2:
    x_row = x[0, :]
    if not np.allclose(x_row, x):
      raise ValueError("The rows of 'x' must be equal")
  else:
    raise ValueError("'x' can have at maximum 2 dimensions")
#   
  if y.ndim == 1:
    pass
  elif y.ndim == 2:
    y_col = y[:, 0]
    if not np.allclose(y_col, y.T):
      raise ValueError("The columns of 'y' must be equal")
  else:
    raise ValueError("'y' can have at maximum 2 dimensions")

  nx = len(x_row)
  ny = len(y_col)

  width = x_row[-1] - x_row[0]
  height = y_col[-1] - y_col[0]

  rtol = 1.e-6
  atol = 0.0
  dx = width/(nx-1)
  if not np.allclose(np.diff(x_row), dx, atol, rtol):
    x1r = np.arange(x_row[0],x_row[-1]+0.1*dx,dx)

    for ii in range(ny):
      xcrct[ii] = x1r

# breakpoint() 
  dy = height/(ny-1)
  if not np.allclose(np.diff(y_col), dy, atol, rtol):
    y1r = np.arange(y_col[0],y_col[-1]+0.1*dy,dy)

    for ii in range(nx):
      ycrct[:,ii] = y1r

# breakpoint()
  x_row2 = xcrct[0, :]
  np.allclose(np.diff(x_row2), dx, atol, rtol)

  return xcrct, ycrct

