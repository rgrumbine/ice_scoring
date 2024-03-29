import os
import datetime

from utility import *       #mmablib python utilities
from platforms import *

#-------------------------------------------
"""
Tools for working with grids of information --
get of: ims, cfsv2, nsidc, ncep analysis, model forecast 
edge for: (likewise)

get_ims
ims_edge
(repeat for others)

Also present is nsidc_name, fcst_name, for constructing file names and paths
For these two, it's more involved and less predictable
Shouldn't be needed by user, but may need updates

"""
#-------------------------------------------
# RG: logfile for comments out

#-------- Skeleton for grid type sources: ---
# NNN tools (NNN = ims, ncep, nsidc_north, cfsv2, ...)
def get_NNN(initial_date, NNNdir, NNN):
  retcode = int(0)
  initial = int(initial_date.strftime("%Y%m%d"))
  fname = NNN + str(initial)
  if (not os.path.exists(fname)):
    fin = NNNdir + NNN+"."+str(initial) + '.gz'
    if (os.path.exists(fin) ):
      cmd = ('cp ' + fin + ' .')
      x = os.system(cmd)
      cmd = ('gunzip '+ "NNN."+str(initial) +'.gz')
      x = os.system(cmd)
      if (x != 0): retcode += x
    else:
# This varies a lot between cases:
#      fin = NNNdir + "NNN." + str(initial) + ".grib2"
      cmd=('wgrib2 '+fin + "| grep ICEC | wgrib2 -i " + fin +
             " -no_header -order we:ns -bin " + fname + ' > /dev/null' )
      x = os.system(cmd)
      if (x != 0): retcode += x

  if (not os.path.exists(fname)):
    print("cannot make "+NNN+" file ",fname, flush=True)
    retcode += 1

  return retcode
def NNN_edge(initial, NNN):
  retcode = int(0)
  fname = NNN+'.'+str(initial)
  if (not os.path.exists(NNN+'_edge.' + str(initial))):
    cmd = exdir + 'find_edge_'+NNN + fname + ' > '+NNN+'_edge.' + str(initial)
    os.system(cmd)
    x = os.system(cmd)
    if (x != 0): retcode += x
  return retcode

#-------- CFSv2 ----------------------------------------
def get_cfsv2(initial_date, valid_date, NNNdir, NNN):
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

def cfsv2_edge(initial, valid, NNN):

  retcode = int(0)
  fname = NNN+'.'+str(valid)
  if (not os.path.exists(NNN+'_edge.' + str(initial))):
    cmd = exdir + 'find_edge_'+NNN +" "+ fname + ' '+fixdir+'/seaice_alldist.bin 0.40 > '+NNN+'_edge.' + str(valid)
    #print("cmd for cfs edge = ",cmd, flush=True)
    os.system(cmd)
    x = os.system(cmd)
    if (x != 0): retcode += x
  return retcode

#------------------------------------------------------------------
#ims tools
def get_ims(initial_date, imsdir):
  retcode = int(0)
  initial    = int(initial_date.strftime("%Y%m%d"))

#more efficient to gunzip binaries than go to grib
  fname = imsdir + 'ims.'+str(initial)
  if (not os.path.exists(fname)):
    fin = imsdir + "ims."+str(initial) +'.gz'
    if (os.path.exists(fin) ):
      cmd = ('cp ' + fin + ' .')
      x = os.system(cmd)
      cmd = ('gunzip '+ "ims."+str(initial) +'.gz')
      x = os.system(cmd)
      if (x != 0): retcode += x
    else:
      fin = imsdir + "imssnow96." + str(initial) + ".grib2"
      cmd=('wgrib2 '+fin + "| grep ICEC | wgrib2 -i " + fin + 
             #" -no_header -order we:ns -bin " + fname + ' > /dev/null' )
             " -no_header -bin " + fname + ' > /dev/null' )
      x = os.system(cmd)
      if (x != 0): retcode += x

  if (not os.path.exists(fname)):
    print("cannot make ims file ",fname, flush=True)
    retcode += 1

  return retcode

def ims_edge(initial, imsdir):
  retcode = int(0)
  inname = imsdir+'ims.'+str(initial)
  outname = imsdir+'ims_edge.' + str(initial)
  if (not os.path.exists(outname) and os.path.exists(inname) ):
    cmd = exdir + 'find_edge_ims ' + inname +  '>' + outname
    os.system(cmd)
    x = os.system(cmd)
    if (x != 0): retcode += x
  return retcode

#------------------------------------------------------------------
def ncep_edge(initial, ncepdir):
  retcode = int(0)
  edgedir = dirs['edgedir']
  fname = ncepdir + 'ncep.'+str(initial)
  edgename = edgedir + 'ncep_edge.' + str(initial)
  print("ncep_edge ",edgedir, fname, edgename, flush=True)

  if (not os.path.exists(edgename) and os.path.exists(fname)  ):
    #note that name does not follow convention
    cmd = exdir + 'find_edge ' + fname + ' '+fixdir+'/seaice_alldist.bin 0.40 > ' + edgename
    x = os.system(cmd)
    if (x != 0): retcode += x
    return retcode

def get_ncep(initial_date, valid_date, ncepdir):
  retcode = int(0)
  tag = initial_date
  dt  = datetime.timedelta(1);
  count = (valid_date - initial_date)/dt
  
  for i in range (0,int(count)+1):
    yyyymm  = int(tag.strftime("%Y%m"))
    initial = int(tag.strftime("%Y%m%d"))
    ncep_file = ncepdir + "ice5min.grib2." + str(yyyymm) 
    if (os.path.exists(ncep_file) ):
      fname = ncepdir + 'ncep.'+str(initial)
      if (not os.path.exists(fname)):
#far more efficient to gunzip binaries
        cmd=('wgrib2 '+ncep_file + "| grep "+str(initial) + " | wgrib2 -i " + 
              ncep_file + " -no_header -order we:ns -bin " + fname + " > /dev/null" )
        x = os.system(cmd)
        if (x != 0): retcode += x
    else:
      print("cannot get_ncep file ",ncep_file, flush=True)
      retcode += 1
    tag += dt

  return retcode

#------------------------------------------------------------------
def nsidc_name(pole, date, nsidcdir):
# https://nsidc.org/ancillary-pages/smmr-ssmi-ssmis-sensors
# date end_f11: 1995,09,30
# date end_f13: 2008,12,31
# date begin_f17: 2006,11,04 

  version = "v04r00"
  if (date <= datetime.date(2008,12,31)):
    instrument = "f13"
  else:
    instrument = "f17"

  retcode = int(0)
  if (not os.path.exists(nsidcdir)):
    print("no such nsidc path as ",nsidcdir, flush=True)
    retcode = 1
    return retcode

  if (not ((pole == 'north') or (pole == 'south')) ):
    print("invalid pole passed -- ",pole, flush=True)
    retcode = 1
    return retcode

  ptag=pole[0]
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


def get_nsidc(initial_date, valid_date, nsidcdir):
  retcode = int(0)
  if (not os.path.exists(nsidcdir)):
    print("no such nsidc path as ",nsidcdir, flush=True)
    retcode = 1
    return retcode

  initial = int(initial_date.strftime("%Y%m%d"))
  valid   = int(valid_date.strftime("%Y%m%d"))
  yearinitial = int(initial_date.strftime("%Y"))
  yearvalid   = int(valid_date.strftime("%Y"))

  fname = nsidc_name('north', initial_date, nsidcdir) 
  if (not os.path.exists(fname)):
    print('do not have ',fname,' ',str(initial), flush=True )
    return 1

  fname = nsidc_name('north', valid_date, nsidcdir)
  if (not os.path.exists(fname)):
    print('do not have ',fname,' ',str(valid), flush=True )
    return 1

  fname = nsidc_name('south', initial_date, nsidcdir)
  if (not os.path.exists(fname)):
    print('do not have ',fname, ' ',str(initial), flush=True )
    return 1

  fname = nsidc_name('south', valid_date, nsidcdir)
  if (not os.path.exists(fname)):
    print('do not have ',fname, ' ',str(valid), flush=True )
    return 1

  return retcode

def nsidc_edge(initial, toler, nsidcdir, exdir, fixdir):
  retcode = int(0)
  yearinitial = int(int(initial)/10000)
  initial_date = parse_8digits(initial)
  edgedir = dirs['edgedir']

  fin = nsidc_name('north',initial_date, nsidcdir)
  #debug print("nsidc edge fin name = ",fin, flush=True)

  fout = edgedir+'/nsidc_north_edge.'+str(initial)
  #debug print(fin, toler, fout, flush=True)

  if (not os.path.exists(fout)):
    cmd = exdir + 'find_edge_nsidc_north ' + fin + ' ' + str(toler) + " " + fixdir+"/G02202-cdr-ancillary-nh.nc" + ' > ' + fout
    #debug print('north command: ',cmd , flush=True )
    x = os.system(cmd)
    if (x != 0): retcode += x

  fout = edgedir+'/nsidc_south_edge.'+str(initial)
  fin = nsidc_name('south',initial_date, nsidcdir)
  if (not os.path.exists(fout)):
    cmd = exdir + 'find_edge_nsidc_south ' + fin + ' ' + str(toler) + " " + fixdir+"/G02202-cdr-ancillary-sh.nc" + ' > ' + fout
    #debug print('south command: ',cmd, flush=True  )
    x = os.system(cmd)
    if (x != 0): retcode += x

  return retcode

#-----------------------------------------------------------------===
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

#-----------------------------------------------------------------===
#    getting the forecast files

def fcst_name(valid, initial, fcst_dir):
#n.b.: assumes that valid and initial are same type
  #debug print("fcst_name values: valid, initial, fcstdir:",valid, initial,fcst_dir, flush=True)
  #debug print("types valid, initial, fcstdir: ",type(valid), type(initial), type(fcst_dir), flush=True )

  tvalid = tostr(valid)
  tinitial = tostr(initial)
  #debug: print(tvalid, tinitial, type(tvalid), type(tinitial) , flush=True )

  #Some UFS prototype name formats:
  #fname = fcst_dir + '/ice' + tvalid + '00.01.' + tinitial + '00.nc'
  #fname = fcst_dir + '/ice' + tvalid +   '.01.' + tinitial + '00.nc'
  #fname = fcst_dir + '/ice' + tvalid +   '.01.' + tinitial + '00.subset.nc'

  fname = fcst_dir + '/ice' + tvalid +   '.01.' + tinitial + '00.subset.nc'

  #CICE consortium default
  #fdate = parse_8digits(int(tvalid))
  #fname = fcst_dir+'iceh.'+fdate.strftime("%Y")+'-'+fdate.strftime("%m")+'-'+fdate.strftime("%d")+".nc"

  #debug: print("\nfname, type\n", fname, type(fname),flush=True)
  if (not os.path.exists(fname) ):
    print("fcst_name: verf_files.py could not find forecast for "+
              fcst_dir, str(valid), str(initial), flush=True)
    print(fname, flush=True)
    #intolerant: 
    exit(1)
    #return 1
  else:
    return fname

def get_fcst(initial_date, valid_date, fcst_dir):
  retcode = int(0)
  initial = int(initial_date.strftime("%Y%m%d"))
  valid   = int(valid_date.strftime("%Y%m%d"))
  #debug print('get fcst ',initial, valid, flush=True)
  #debug print('get fcst ', initial, type(initial), initial_date, type(initial_date))

  #debug: print("get_fcst calling fcst_name", flush=True)
  fname = fcst_name(valid, initial, fcst_dir)
  #debug print("fname = ",fname, flush=True)

  if (not os.path.exists(fname)):
    retcode += 1
    print("Do not have forecast file ",fname," for ",initial, valid, flush=True)
  return retcode


#pass 8digit dates:
def fcst_edge(initial, valid, fcst_dir, fixdir, exdir):
  retcode = int(0)
  edgedir = dirs['edgedir']
  fname = edgedir + 'fcst_edge.' + str(valid)
  #debug: print("edgedir, fname ",edgedir, fname, flush=True)
 
  #if (not os.path.exists(fname) ):
  if (os.path.exists(fname) ):
    print("already have ",fname," skipping", flush=True)

  else:
    #debug: print("fcst_edge calling fcst_name", flush=True)

    fcstin = fcst_name(valid, initial, fcst_dir)
    if (type(fcstin) == int):
      print("verf_files.py fcst_edge Could not find forecast for ",valid, initial, fcst_dir)
      return 1
    #RG: want something cleaner for selecting model format/version!
    #UFS
    #debug: print("cmd", type(exdir), type(fixdir), type(fcstin), type(valid), flush=True )
    cmd = exdir + 'find_edge_cice '+fixdir+'skip_hr ' + fcstin + ' 0.40 > ' + fname

    #CICE
    #cmd = exdir + 'find_edge_consortium '+fixdir+'skip_hr ' + fname + ' 0.40 > fcst_edge.' + str(valid)

    x = os.system(cmd)
    if (x != 0): retcode += x
  return retcode

#------------------------------------------------------------------
