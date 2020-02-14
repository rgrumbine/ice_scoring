import os
import sys
import datetime

#------------------------------------------------------------------
#--------------- Utility Functions --------------------------------
def parse_8digits(tag):
  tmp = int(tag)
  (yy,mm,dd) = (int(int(tmp)/10000),int((int(tmp)%10000)/100),int(tmp)%100)
  tag_out = datetime.date(int(yy), int(mm), int(dd))
  return tag_out

#----------------- High level declarations -----------------------------
exdir = "./exec/"
# Directories w. verification data
dirs = {
  'imsdir' : '',
  'ncepdir' : '',
  'nsidcdir' : ''
}

# Known machines:
machines = {
  'RG_Home'       : '/Volumes/ncep',
  'HERA'          : '/scratch1',
  'WCOSS_C'       : '/etc/SuSE-release',
  'WCOSS_DELL_P3' : '/gpfs/dell2'
}
#----------------- Identify our machines -----------------------------

# Determine which known machine we're on, if any:
mlist = []
machine=""
for x in machines:
  mlist += [x]
  if (os.path.exists(machines[x]) ):
    machine = (x)
    break

if not machine:
    print ('ice verification is currently only supported on: %s' % ' '.join(machines))
    raise NotImplementedError('Cannot auto-detect platform, ABORT!')

#------------------------------------------------------------------
# Establish paths to verification data:
if (machine == 'HERA'):
  dirs['imsdir'] = '/home/Robert.Grumbine/clim_data/ims/'
  dirs['ncepdir'] = '/home/Robert.Grumbine/clim_data/ice5min/'
  dirs['nsidcdir'] = '/home/Robert.Grumbine/clim_data/nsidc.nc/'
  dirs['fixdir']   = '/home/Robert.Grumbine/rgdev/mmablib/ice_scoring/fix'
elif (machine == 'WCOSS_C'):
  dirs['imsdir'] = '/u/Robert.Grumbine/noscrub/ims/'
  dirs['ncepdir'] = '/u/Robert.Grumbine/noscrub/sice/'
  dirs['nsidcdir'] = '/u/Robert.Grumbine/noscrub/nsidc/'
elif (machine == 'WCOSS_DELL_P3'):
  dirs['imsdir'] = '/u/Robert.Grumbine/noscrub/ims/'
  dirs['ncepdir'] = '/u/Robert.Grumbine/noscrub/sice/'
  dirs['nsidcdir'] = '/u/Robert.Grumbine/noscrub/nsidc/'
elif (machine == 'RG_Home'):
  dirs['imsdir'] = '/Volumes/ncep/allconc/ims/'
  dirs['ncepdir'] = '/Volumes/ncep/allconc/ice5min/'
  dirs['nsidcdir'] = '/Volumes/ncep/allconc/nsidc_nc/'
else:
  print ('ice verification is currently only supported on: %s' % ' '.join(machines))
  raise NotImplementedError('Cannot find verification data directory, ABORT!')

#------------------------------------------------------------------
#Do we have the fixed file directory:
if (not os.path.exists(dirs['fixdir'])):
  print('no ice verification fixed directory ')
  raise NotImplementedError('Cannot find any verification fixed directory.  ABORT!')

#Do we have verification data directories
nsidcverf = os.path.exists(dirs['nsidcdir'])
ncepverf = os.path.exists(dirs['ncepdir'])
imsverf  = os.path.exists(dirs['imsdir'])
if (not nsidcverf and not ncepverf and not imsverf):
  print('no ice verification directory is present, aborting')
  raise NotImplementedError('Cannot find any verification data directories, ABORT!')
#------------------------------------------------------------------
#Variables established by this script:
# machines (a dictionary of machine identifiers)
# dirs (a dictionary of directory paths)
# execdir (location of executables)
# imsdir, ncepdir, nsidcdir, fixdir (entries to dictionary) 
