import os
import datetime

# Class to be specialized by ims, ncep, osisaf, nsidc, ... -- 
#     observed/analyzed grids of sea ice cover
# Robert Grumbine

#examples:
#  ims = obs_grid(name="ims", type="grib2", scope="NH")
#  nsidc_north = ""(name="nsidc_north", type="nc", scope="NH")
#  nsidc_south = ""(name="nsidc_south", type="nc", scope="SH")
#  osi_north = ""(name="osi_north", type="nc", scope="NH")
#  osi_south = ""(name="osi_south", type="nc", scope="SH")
#  ncep = obs_grid(name="ncep", type=grib2", scope="global")
#
#additional class? -- split_grid (nsidc, osisaf), where separate
#  NH and SH grids exist, but combined coverage is global

class obs_grid :

  def __init__(self, name="NNN", type="nc", Ndir="./", scope="global"):
    self.name = name
    self.type = type                  #or grib2
    self.dir  = Ndir
    self.solo_name = self.name+"_solo"
    self.edge_name = self.name+"_edge"
    self.scope     = scope            # global, NH, SH


  def get2(self, initial, valid):
    retcode = self.get(initial)
    retcode += self.get(valid)
    return retcode

  def get(self, datein):
    retcode = int(0)
    fname = self.name + datein.strftime("%Y%m%d")
    if (not os.path.exists(fname)):
      print("try unzip")
      x = get_gz(fin, fname, datein)
      if (x == 0):
        return retcode

    if (self.type == "grib2"):
      retcode = self.get_grib(fin, fname)
    elif (self.type == "nc"):
      retcode = self.get_nc(fin, fname)

    if (retcode != 0):
      print("cannot get ",self.name," file for ",datein.strftime("%Y%m%d"), flush=True)

    return retcode

  def get_gz(self, fin, fname, datein):
    fin = self.dir + self.name+"."+ datein.strftime("%Y%m%d") + '.gz'
    if (os.path.exists(fin) ):
      cmd = ('cp ' + fin + ' .')
      x = os.system(cmd)
      cmd = ('gunzip '+ "NNN."+str(initial) +'.gz')
      retcode = os.system(cmd)
      return retcode
    
  def get_grib(self, fin, fname):
    retcode = int(0)
    print("trying grib", flush=True)
    cmd=('wgrib2 '+fin + "| grep ICEC | wgrib2 -i " + fin +
           " -no_header -order we:ns -bin " + fname + ' > /dev/null' )
    retcode = os.system(cmd)
    return retcode

  def get_nc(self, fin, fname):
    retcode = int(0)
    print("trying .nc", flush=True)
    return retcode


