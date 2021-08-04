import os
import sys
import datetime

#------------------------------------------------------------------
exbase = os.environ['EXDIR']
exdir  = exbase+"/exec/"
fixdir = exbase+"/fix/"
#debug print("exbase, exdir, fixdir = ",exbase, exdir, fixdir)

#--------------- Utility Functions --------------------------------
def parse_8digits(tag):
  tmp = int(tag)
  (yy,mm,dd) = (int(int(tmp)/10000),int((int(tmp)%10000)/100),int(tmp)%100)
  tag_out = datetime.date(int(yy), int(mm), int(dd))
  return tag_out

#----------------- High level declarations -----------------------------
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
  'WCOSS_DELL_P3' : '/gpfs/dell2',
  'Orion'         : '/home/rgrumbin',
  'Gaea'          : '/lustre/f2/scratch'
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

#debug print("machine = ",machine)

if not machine:
    print ('ice verification is currently only supported on: %s' % ' '.join(machines))
    raise NotImplementedError('Cannot auto-detect platform, ABORT!')

#------------------------------------------------------------------
# Establish paths to verification data:
if (machine == 'HERA'):
  dirs['imsdir'] = '/home/Robert.Grumbine/clim_data/verification_data/ims/'
  dirs['ncepdir'] = '/home/Robert.Grumbine/clim_data/verification_data/ice5min/'
  dirs['nsidcdir'] = '/home/Robert.Grumbine/clim_data/verification_data/nsidc.nc/'
  dirs['fixdir']   = '/home/Robert.Grumbine/rgdev/fix'
elif (machine == 'Orion'):
  dirs['imsdir'] = '/home/rgrumbin/rgdev/verification_data/ims/'
  dirs['ncepdir'] = '/home/rgrumbin/rgdev/verification_data/ice5min/'
  dirs['nsidcdir'] = '/home/rgrumbin/rgdev/verification_data/nsidc.nc/'
  dirs['fixdir']   = '/home/rgrumbin/rgdev/ice_scoring/fix'
elif (machine == 'WCOSS_C'):
  dirs['imsdir'] = '/u/Robert.Grumbine/noscrub/ims/'
  dirs['ncepdir'] = '/u/Robert.Grumbine/noscrub/sice/'
  dirs['nsidcdir'] = '/u/Robert.Grumbine/noscrub/nsidc/'
  dirs['fixdir']   = '/u/Robert.Grumbine/para/mmablib/ice_scoring/fix'
elif (machine == 'WCOSS_DELL_P3'):
  dirs['imsdir'] = '/u/Robert.Grumbine/noscrub/ims/'
  dirs['ncepdir'] = '/u/Robert.Grumbine/noscrub/ice5min/'
  dirs['nsidcdir'] = '/u/Robert.Grumbine/noscrub/sidads.colorado.edu/pub/DATASETS/NOAA/G02202_V3/'
  dirs['fixdir']   = '/u/Robert.Grumbine/para/mmablib/ice_scoring/fix'
elif (machine == 'Gaea'):
  dirs['imsdir'] = '/lustre/f2/dev/ncep/Robert.Grumbine/CICE_INPUTDATA/Verification_data/ims/'
  dirs['ncepdir'] = '/lustre/f2/dev/ncep/Robert.Grumbine/CICE_INPUTDATA/Verification_data/ice5min/'
  dirs['nsidcdir'] = '/lustre/f2/dev/ncep/Robert.Grumbine/CICE_INPUTDATA/Verification_data/nsidc.nc/'
  dirs['fixdir']   = '/lustre/f2/dev/ncep/Robert.Grumbine/fix'
elif (machine == 'RG_Home'):
  dirs['imsdir'] = '/Volumes/ncep/allconc/ims/'
  dirs['ncepdir'] = '/Volumes/ncep/allconc/ice5min/'
  dirs['nsidcdir'] = '/Volumes/ncep/allconc/nsidc_nc/'
  dirs['fixdir']   = '/u/Robert.Grumbine/para/mmablib/ice_scoring/fix'
else:
  print ('ice verification is currently only supported on: %s' % ' '.join(machines))
  raise NotImplementedError('Cannot find verification data directory, ABORT!')

#debug print("fixdir = ", (dirs['fixdir']) )
#debug print("os path exists ", os.path.exists(dirs['fixdir']))
#debug exit(1)

#------------------------------------------------------------------
#Do we have the fixed files directory?
if (not os.path.exists(dirs['fixdir'])):
  print('no ice verification fixed (reference) directory ',dirs['fixdir'])
  raise NotImplementedError('Cannot find any verification fixed (reference) directory.  ABORT!')

#Do we have verification data directories?
nsidcverf = os.path.exists(dirs['nsidcdir'])
ncepverf  = os.path.exists(dirs['ncepdir'])
imsverf   = os.path.exists(dirs['imsdir'])
#debug print(dirs['nsidcdir'], dirs['ncepdir'], dirs['imsdir'] )

if (not nsidcverf and not ncepverf and not imsverf):
  print('no ice verification directory is present, aborting')
  print('tried verification directories ', dirs['nsidcdir'], dirs['ncepdir'], dirs['imsdir'] )
  raise NotImplementedError('Cannot find any verification data directories, ABORT!')
#------------------------------------------------------------------
#Variables established by this script:
#  machines (a dictionary of machine identifiers)
#  dirs (a dictionary of directory paths)
#  execdir (location of executables, needs EXDIR environment variable)
#  fixdir (location of executables, needs EXDIR environment variable)
#  imsdir, ncepdir, nsidcdir, fixdir (entries to dictionary) 

print("Evaluation programs and scripts look ok to run on ",machine)
print("ims dir   = ", dirs['imsdir'])
print("nsidc dir = ", dirs['nsidcdir'])
print("ncep dir  = ", dirs['ncepdir'])
print("reference fixed files directory = ",dirs['fixdir'])
exit(0)
