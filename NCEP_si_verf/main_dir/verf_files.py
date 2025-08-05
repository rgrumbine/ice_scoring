import os
import datetime


#-----------------------------------------------------------------===
# utility here to help work with date strings -- int vs. string
def tostr(valid):
  if (type(valid) == int):
    #debug print(" is int ", flush=True)
    tvalid = str(valid)
  elif (type(valid) == float):
    #debug print(" is float", flush=True)
    tvalid = str(int(valid))
  elif (type(valid) == str):
    #debug print(" is str", flush=True)
    tvalid = valid
  else:
    #debug print("assume  is datetime", flush=True)
    tvalid = valid.strftime("%Y%m%d")
  return tvalid
#-------------------------------------------
"""
Tools for working with grids of information --
get of: ims, cfsv2, nsidc, osisaf, ncep analysis, model forecast 
edge for: (likewise)

get_ims
ims_edge
(repeat for others)

Also present is nsidc_name, fcst_name, for constructing file names and paths
For these two, it's more involved and less predictable
Shouldn't be needed by user, but may need updates

"""
# RG: Add nsidc_sh

#-----------------------------------------------------------
'''
Abstract base class 'gridded' to be a holder for getting and working with gridded fields
-- get_grid to get the gridded field
-- make_edge to make the set of edge points
-- get_filename to construct the file name for the desired date
   -- -- this can be wildly variable between model instances. 
         should be slowly varying for the verification data
'''

from abc import ABC, abstractmethod
class gridded(ABC):

    @abstractmethod
    def get_grid(date, basedir):
      pass
      #return 0 if successful

    @abstractmethod
    def make_edge(name, date):
      pass

    @abstractmethod
    def get_filename(date, basedir):
      pass

#-------------- Dummy ----------------------------
class dummy(ABC):

    def get_grid(fname, date, basedir):
      return 0

    def make_edge(name, date):
      return 0

    def get_filename(date, basedir):
      return 0

#-------------- osisaf ----------------------------
class osisaf(gridded):

    def get_grid(date, basedir, ptag="nh"):
      fname = osisaf.get_filename(date, basedir, ptag)
      if (os.path.exists(fname)):
        return 0
      else:
        print(fname, "does not exist osisaf:get_grid")
        return 1

    def make_edge(name, date):
      return 0

    def get_filename(date, basedir, ptag="nh"):
      tmp = basedir + "archive/ice/conc/" + date.strftime("%Y") + "/" + date.strftime("%m") + "/" + "ice_conc_"+ptag+"_polstere-100_multi_"+date.strftime("%Y%m%d")+"1200.nc"
      return tmp

#---------- NCEP obs -----------------------------------
class ncep(gridded):

    def get_grid(self, tag, ncepdir):
      retcode = int(0)

      monthfile = ncepdir + "ice5min.grib2." + tag.strftime("%Y%m") 
      index_file = ncepdir + "ice5min.grib2." + tag.strftime("%Y%m") + '.idx'
      if (not os.path.exists(index_file)):
        cmd = ( 'wgrib2 ' + monthfile + " > "+index_file )
        x = os.system(cmd)
        if (x != 0): retcode += x

      fname = ncepdir + 'ncep.'+ tag.strftime("%Y%m%d")
      if (os.path.exists(index_file) and not os.path.exists(fname) ):
        cmd = ( ' grep ' + tag.strftime("%Y%m%d") + " " + index_file + 
               " | wgrib2 -i " + monthfile + " -no_header -order we:ns -bin " + fname + " > /dev/null" )
        #debug: print("cmd = ",cmd)
        x = os.system(cmd)
        if (x != 0): retcode += x

    def make_edge(self, tag, ncepdir, edgedir, exdir, fixdir):
      retcode = int(0)
      fname = ncepdir + 'ncep.'+tag.strftime("%Y%m%d")
      edgename = edgedir + 'ncep_edge.' + tag.strftime("%Y%m%d")
      #debug: print("ncep_edge ",edgedir, fname, edgename, flush=True)

      if (not os.path.exists(edgename) and os.path.exists(fname)  ):
        #note that name does not follow convention
        cmd = exdir + 'find_edge_ncep ' + fname + ' '+fixdir+'/seaice_alldist.bin 0.40 > ' + edgename
        #debug: print("cmd = ",cmd, flush=True)

        x = os.system(cmd)
        if (x != 0): retcode += x
        return retcode

      return 0

    def get_filename(self, tag, ncepdir):
      return ncepdir + 'ncep.'+ tag.strftime("%Y%m%d")

#-------- CFSv2 ----------------------------------------
# not fully current
class cfsv2(gridded):

  def get_grid(initial_date, valid_date, NNNdir, NNN):
    retcode = int(0)
    #for now, look only at memno = 01 -- often the only one archived
    memno="01"
    initial = int(initial_date.strftime("%Y%m%d"))
    valid   = int(valid_date.strftime("%Y%m%d"))
    fname = NNN+"."+str(valid)
    if (not os.path.exists(fname)):
      fin = NNNdir +"/"+ NNN+"."+str(valid) + '.gz'
      if (os.path.exists(fin) ):
        cmd = ('cp ' + fin + ' .')
        x = os.system(cmd)
        cmd = ('gunzip '+ NNN+"."+str(valid) +'.gz')
        x = os.system(cmd)
        if (x != 0): retcode += x
      else:
  # This varies a lot between cases:
  #      fin = NNNdir + "NNN." + str(initial) + ".grib2"
        fin = NNNdir + "/ocnf.ice."+valid_date.strftime("%Y%m%d")+"00."+str(memno)+"."+initial_date.strftime("%Y%m%d")+"00"
        cmd=('wgrib2 '+fin + "| grep ICEC | wgrib2 -i " + fin +
               " -no_header -order we:ns -bin " + fname + ' > /dev/null' )
        x = os.system(cmd)
        if (x != 0): retcode += x
  
    if (not os.path.exists(fname)):
      print("cannot make "+NNN+" file ",fname, flush=True)
      retcode += 1
  
    return retcode

  def make_edge(initial, valid, NNN):
  
    retcode = int(0)
    fname = NNN+'.'+str(valid)
    if (not os.path.exists(NNN+'_edge.' + str(initial))):
      cmd = exdir + 'find_edge_'+NNN +" "+ fname + ' '+fixdir+'/seaice_alldist.bin 0.40 > '+NNN+'_edge.' + str(valid)
      #print("cmd for cfs edge = ",cmd, flush=True)
      os.system(cmd)
      x = os.system(cmd)
      if (x != 0): retcode += x
    return retcode

  def get_filename():
    return 0

#------------------------------------------------------------------
class osisaf_nh(gridded):
  def get_grid(self, initial_date, osisafdir):
    retcode = int(0)
    if (not os.path.exists(osisafdir)):
      print("no such osisaf path as ",osisafdir, flush=True)
      retcode = 1
      return retcode

    fname = self.get_filename(initial_date, osisafdir)
    if (not os.path.exists(fname)):
      print('do not have ',fname,' ',initial_date.strftime("%Y%m%d"), flush=True )
      return 1
    
    return retcode

  def make_edge(self, initial_date, toler, osisafdir, exdir, fixdir, edgedir):
    retcode = int(0)

    fin = self.get_filename(initial_date, osisafdir)
    fout = edgedir+'/osisaf_north_edge.'+initial_date.strftime("%Y%m%d")

    if (not os.path.exists(fout)):
      cmd = exdir + 'find_edge_osisaf_north ' + fin + ' ' + str(toler) + " " + fixdir+"/G02202-cdr-ancillary-nh.nc" + ' > ' + fout
      x = os.system(cmd)
      if (x != 0): retcode += x

    return retcode

  def get_filename(self, date, osisafdir):
    ptag='nh'
    pole='north'

    version = "v04r00"
    if (date <= datetime.datetime(2008,12,31)):
      instrument = "f13"
    else:
      instrument = "f17"

    retcode = int(0)
    if (not os.path.exists(osisafdir)):
      print("no such osisaf path as ",osisafdir, flush=True)
      retcode = 1
      return retcode

    valid = int(date.strftime("%Y%m%d"))

    fname = osisafdir + pole + '/daily/'+date.strftime("%Y")+'/seaice_conc_daily_'+ptag+'h_'+str(valid)+'_'+instrument+'_'+version+'.nc'

    if (os.path.exists(fname)):
      return fname
    else:
      fname_old = fname
      fname = osisafdir + pole + '/daily/'+date.strftime("%Y")+'/seaice_conc_daily_'+ptag+'h_'+instrument+'_'+str(valid)+'_'+version+'.nc'
      if (os.path.exists(fname)):
        return fname
      else:
        print("osisaf_name: could not open ",fname_old, fname, flush=True)
        retcode = 1
        #intolerant:
        exit(1)
        return retcode




#------------------------------------------------------------------
class nsidc_nh(gridded):

  def get_grid(self, initial_date, nsidcdir):
    retcode = int(0)
    if (not os.path.exists(nsidcdir)):
      print("no such nsidc path as ",nsidcdir, flush=True)
      retcode = 1
      return retcode
  
    fname = self.get_filename(initial_date, nsidcdir)
    if (not os.path.exists(fname)):
      print('do not have ',fname,' ',initial_date.strftime("%Y%m%d"), flush=True )
      return 1
  
    return retcode

  def make_edge(self, initial_date, toler, nsidcdir, exdir, fixdir, edgedir):
    retcode = int(0)
  
    fin = self.get_filename(initial_date, nsidcdir)
    fout = edgedir+'/nsidc_north_edge.'+initial_date.strftime("%Y%m%d")
  
    if (not os.path.exists(fout)):
      cmd = exdir + 'find_edge_nsidc_north ' + fin + ' ' + str(toler) + " " + fixdir+"/G02202-cdr-ancillary-nh.nc" + ' > ' + fout
      x = os.system(cmd)
      if (x != 0): retcode += x
  
    return retcode

  def get_filename(self, date, nsidcdir):
    # https://nsidc.org/ancillary-pages/smmr-ssmi-ssmis-sensors
    # date end_f11: 1995,09,30
    # date end_f13: 2008,12,31
    # date begin_f17: 2006,11,04 
    ptag='n'
    pole='north'
  
    version = "v04r00"
    if (date <= datetime.datetime(2008,12,31)):
      instrument = "f13"
    else:
      instrument = "f17"
  
    retcode = int(0)
    if (not os.path.exists(nsidcdir)):
      print("no such nsidc path as ",nsidcdir, flush=True)
      retcode = 1
      return retcode
  
    valid = int(date.strftime("%Y%m%d"))
    
    #fname = nsidcdir + pole + '/'+date.strftime("%Y")+'/seaice_conc_daily_'+ptag+'h_'+instrument+'_'+str(valid)+'_v03r01.nc'
    fname = nsidcdir + pole + '/daily/'+date.strftime("%Y")+'/seaice_conc_daily_'+ptag+'h_'+str(valid)+'_'+instrument+'_'+version+'.nc'
  
    if (os.path.exists(fname)):
      return fname
    else:
      fname_old = fname
      #fname = nsidcdir + pole + '/daily/'+date.strftime("%Y")+'/seaice_conc_daily_'+ptag+'h_'+instrument+'_'+str(valid)+'_v03r01.nc'
      fname = nsidcdir + pole + '/daily/'+date.strftime("%Y")+'/seaice_conc_daily_'+ptag+'h_'+instrument+'_'+str(valid)+'_'+version+'.nc'
      if (os.path.exists(fname)):
        return fname
      else:
        print("nsidc_name: could not open ",fname_old, fname, flush=True)
        retcode = 1
        #intolerant: 
        exit(1)
        return retcode

#-----------------------------------------------------------------===
#class nsidc_sh(gridded):
#-----------------------------------------------------------------===

class ims(gridded):

  def get_grid(self, tag, imsdir):

    retcode = int(0)
    initial = int(tag.strftime("%Y%m%d"))
  
  #more efficient to gunzip binaries than go to grib
    fname = imsdir + '/ims.'+str(initial)
    if (not os.path.exists(fname)):
      #debug: print("no file ",fname, flush=True)

      fin = imsdir + "/ims."+str(initial) +'.gz'
      if (os.path.exists(fin) ):
        cmd = ('cp ' + fin + ' .')
        x = os.system(cmd)
        cmd = ('gunzip '+ "/ims."+str(initial) +'.gz')
        x = os.system(cmd)
        if (x != 0): retcode += x
      else:
        fin = imsdir + "imssnow96." + tag.strftime("%Y%m%d")+ ".grib2"
        if (not os.path.exists(fin)):
          print("could not find grib file ",fin)
          return 1
        cmd=('wgrib2 '+fin + "| grep ICEC | wgrib2 -i " + fin +
               #" -no_header -order we:ns -bin " + fname + ' > /dev/null' )
               " -no_header -bin " + fname + ' > /dev/null' )
        x = os.system(cmd)
        if (x != 0): retcode += x
  
    if (not os.path.exists(fname)):
      print("could make ims file ",fname, flush=True)
      retcode += 1
  
    return retcode

  def get_filename(self, initial, imsdir):
    return imsdir+'ims.' + initial.strftime("%Y%m%d")

  def make_edge(self, initial, imsdir, edgedir, exdir):
    #debug: print("in ims make_edge", flush=True)

    retcode = int(0)
    inname = imsdir+'ims.' + initial.strftime("%Y%m%d")
    outname = edgedir +'ims_edge.' + initial.strftime("%Y%m%d")

    if (not os.path.exists(outname) and os.path.exists(inname) ):
      #debug: print("trying to make ims edge ", flush=True)
      cmd = exdir + 'find_edge_ims ' + inname +  '>' + outname
      #debug: print("cmd = ",cmd,flush=True)
      os.system(cmd)
      x = os.system(cmd)
      if (x != 0): retcode += x
    else:
      if (not os.path.exists(inname)):
        print("could not find ",inname)

    return retcode


#-----------------------------------------------------------------===

