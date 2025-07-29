import os
import datetime

#-----------------------------------------------------------
'''
Abstract base class 'gridded' to be a holder for getting and working with gridded fields
-- get_grid to get the gridded field
-- make_edge to make the set of edge points
-- get_filename to construct the file name for the desired date
   -- -- this can be wildly variable between model instances. 
         should be slowly varying for the verification data
'''

import verf_files

#---------- forecast model -----------------------------------
class hr3b(verf_files.gridded):

#For hr3b need ymd is in fcstdir path need hr (hh of fcst lead)
    def get_grid(self, hr, fcstdir):
      retcode = 0
      fname = self.get_filename(hr, fcstdir)
      if (not os.path.exists(fname)):
        retcode = 1
        print("Do not have forecast file ",fname," for ",hr, flush=True)
      return retcode

    def make_edge(self, tag, hr, fcstdir, edgedir, exdir, fixdir):
      retcode = int(0)
      fname = edgedir + 'fcst_edge.' + tag.strftime("%Y%m%d") + "{:03d}".format(hr)
    
      if (os.path.exists(fname) ):
        print("already have ",fname," skipping", flush=True)
    
      else:
        fcstin = self.get_filename(hr, fcstdir)
        if (type(fcstin) == int):
          print("verf_files.py fcst_edge Could not find forecast for ",hr, fcstdir)
          return 1
        cmd = exdir + 'find_edge_cice '+fixdir+'skip_hr ' + fcstin + ' 0.40 > ' + fname

        x = os.system(cmd)
        if (x != 0): retcode += x
      return retcode

    def get_filename(self, hr, fcstdir):
      return fcstdir + 'gfs.ice.t00z.6hr_avg.f'+ "{:03d}".format(hr) + ".nc"

#---------- forecast model -----------------------------------
class rtofs(verf_files.gridded):

#For rtofs need ymd is in fcstdir path need hr (hh of fcst lead)
    def get_grid(self, hr, fcstdir):
      retcode = 0
      fname = self.get_filename(hr, fcstdir)
      if (not os.path.exists(fname)):
        retcode = 1
        print("Do not have forecast file ",fname," for ",hr, flush=True)
      return retcode

    def make_edge(self, tag, hr, fcstdir, edgedir, exdir, fixdir):
      retcode = int(0)
      fname = edgedir + 'fcst_edge.' + tag.strftime("%Y%m%d") + "{:03d}".format(hr)
    
      if (os.path.exists(fname) ):
        print("already have ",fname," skipping", flush=True)
    
      else:
        fcstin = self.get_filename(hr, fcstdir)
        if (type(fcstin) == int):
          print("verf_files.py fcst_edge Could not find forecast for ",hr, fcstdir)
          return 1
        cmd = exdir + 'find_edge_cice '+fixdir+'skip_hr ' + fcstin + ' 0.40 > ' + fname

        x = os.system(cmd)
        if (x != 0): retcode += x
      return retcode

    def get_filename(self, hr, fcstdir):
      return fcstdir + 'rtofs_glo_2ds_f'+"{:03d}".format(hr) + "_ice.nc"

