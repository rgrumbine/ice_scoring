import os
import datetime

from platforms import *

# logfile for comments out
exbase=os.environ['EXDIR']
exdir = exbase+"/exec/"
fixdir = exbase+"/fix/"

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
    print("cannot make "+NNN+" file ",fname)
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
    print("cannot make "+NNN+" file ",fname)
    retcode += 1

  return retcode

def cfsv2_edge(initial, valid, NNN):

  retcode = int(0)
  fname = NNN+'.'+str(valid)
  if (not os.path.exists(NNN+'_edge.' + str(initial))):
    cmd = exdir + 'find_edge_'+NNN +" "+ fname + ' '+fixdir+'/seaice_alldist.bin 0.40 > '+NNN+'_edge.' + str(valid)
    print("cmd for cfs edge = ",cmd)
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
  fname = 'ims.'+str(initial)
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
    print("cannot make ims file ",fname)
    retcode += 1

  return retcode

def ims_edge(initial):
  retcode = int(0)
  fname = 'ims.'+str(initial)
  if (not os.path.exists('ims_edge.' + str(initial))):
    cmd = exdir + 'find_edge_ims ' + fname + ' > ims_edge.' + str(initial)
    os.system(cmd)
    x = os.system(cmd)
    if (x != 0): retcode += x
  return retcode

#------------------------------------------------------------------
def ncep_edge(initial):
  retcode = int(0)
  fname = 'ncep.'+str(initial)
  if (not os.path.exists('ncep_edge.' + str(initial))) :
      #note that name does not follow convention
    cmd = exdir + 'find_edge ' + fname + ' '+fixdir+'/seaice_alldist.bin 0.40 > ncep_edge.' + str(initial)
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
      fname = 'ncep.'+str(initial)
      if (not os.path.exists(fname)):
#far more efficient to gunzip binaries
        cmd=('wgrib2 '+ncep_file + "| grep "+str(initial) + " | wgrib2 -i " + 
              ncep_file + " -no_header -order we:ns -bin " + fname + " > /dev/null" )
        x = os.system(cmd)
        if (x != 0): retcode += x
    else:
      print("cannot get_ncep file ",ncep_file)
      retcode += 1
    tag += dt

  return retcode

#------------------------------------------------------------------
def nsidc_name(pole, date, nsidcdir):
  retcode = int(0)
  if (not os.path.exists(nsidcdir)):
    print("no such nsidc path as ",nsidcdir)
    retcode = 1
    return retcode

  if (not ((pole == 'north') or (pole == 'south')) ):
    print("invalid pole passed -- ",pole)
    retcode = 1
    return retcode

  ptag=pole[0]
  valid = int(date.strftime("%Y%m%d"))
  fname = nsidcdir + pole + '/'+date.strftime("%Y")+'/seaice_conc_daily_'+ptag+'h_f17_'+str(valid)+'_v03r01.nc'
  if (os.path.exists(fname)):
    return fname
  else:
    fname = nsidcdir + pole + '/daily/'+date.strftime("%Y")+'/seaice_conc_daily_'+ptag+'h_f17_'+str(valid)+'_v03r01.nc'
    if (os.path.exists(fname)):
      return fname
    else:
      retcode = 1
      return retcode


def get_nsidc(initial_date, valid_date, nsidcdir):
  retcode = int(0)
  if (not os.path.exists(nsidcdir)):
    print("no such nsidc path as ",nsidcdir)
    retcode = 1
    return retcode

  initial = int(initial_date.strftime("%Y%m%d"))
  valid   = int(valid_date.strftime("%Y%m%d"))
  yearinitial = int(initial_date.strftime("%Y"))
  yearvalid   = int(valid_date.strftime("%Y"))

  fname = nsidc_name('north', initial_date, nsidcdir) 
  if (not os.path.exists(fname)):
    print('do not have ',fname,' ',str(initial) )
    return 1

  fname = nsidc_name('north', valid_date, nsidcdir)
  if (not os.path.exists(fname)):
    print('do not have ',fname,' ',str(valid) )
    return 1

  fname = nsidc_name('south', initial_date, nsidcdir)
  if (not os.path.exists(fname)):
    print('do not have ',fname, ' ',str(initial) )
    return 1

  fname = nsidc_name('south', valid_date, nsidcdir)
  if (not os.path.exists(fname)):
    print('do not have ',fname, ' ',str(valid) )
    return 1

  return retcode

def nsidc_edge(initial, toler, nsidcdir):
  retcode = int(0)
  yearinitial = int(int(initial)/10000)
  initial_date = parse_8digits(initial)

  fout = 'nsidc_north_edge.'+str(initial)
  fin = nsidc_name('north',initial_date, nsidcdir)
  if (not os.path.exists(fout)):
    cmd = exdir + 'find_edge_nsidc_north ' + fin + ' ' + str(toler) + ' > ' + fout
    #print('north command: ',cmd  )
    x = os.system(cmd)
    if (x != 0): retcode += x

  fout = 'nsidc_south_edge.'+str(initial)
  fin = nsidc_name('south',initial_date, nsidcdir)
  if (not os.path.exists(fout)):
    cmd = exdir + 'find_edge_nsidc_south ' + fin + ' ' + str(toler) + ' > ' + fout
    #print('south command: ',cmd  )
    x = os.system(cmd)
    if (x != 0): retcode += x

  return retcode

#-----------------------------------------------------------------===
#-----------------------------------------------------------------===
def fcst_name(valid, initial, fcst_dir):
  #fname = fcst_dir+'ice'+str(valid)+'00.01.'+str(initial)+'00.nc'
  #fname = fcst_dir+'ice'+str(valid)+'.01.'+str(initial)+'00.nc'

  fname = fcst_dir+'ice'+str(valid)+'00.01.'+str(initial)+'00.subset.nc'
  if (not os.path.exists(fname) ):
    fname = fcst_dir+'ice'+str(valid)+'00.01.'+str(initial)+'00.nc'
    if (not os.path.exists(fname) ):
      print("could not find forecast for "+fcst_dir,str(valid),str(initial))
      return 1
    else:
      return fname
  else:
    return fname

def get_fcst(initial_date, valid_date, fcst_dir):
  retcode = int(0)
  initial = int(initial_date.strftime("%Y%m%d"))
  valid   = int(valid_date.strftime("%Y%m%d"))

  fname = fcst_dir+'ice'+str(valid)+'00.01.'+str(initial)+'00.subset.nc'
  if (not os.path.exists(fname) ):
    fname = fcst_dir+'ice'+str(valid)+'00.01.'+str(initial)+'00.nc'

  if (not os.path.exists(fname)):
    retcode += 1
    print("Do not have forecast file ",fname)
  return retcode


def fcst_edge(initial, valid, fcst_dir):
  retcode = int(0)
  #fname = fcst_dir+'/ice'+str(valid)+'00.01.'+str(initial)+'00.subset.nc'
  if (not os.path.exists('fcst_edge.' + str(valid))):
    fname = fcst_name(valid, initial, fcst_dir)
    cmd = exdir + 'find_edge_cice '+fixdir+'skip_hr ' + fname + ' 0.40 > fcst_edge.' + str(valid)
    x = os.system(cmd)
    if (x != 0): retcode += x
  return retcode

#------------------------------------------------------------------
