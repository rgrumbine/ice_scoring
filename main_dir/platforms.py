import os
import sys
import datetime

#run with argument 'trial' to get output for success

#------------------------------------------------------------------
exbase = os.environ['EXBASE']
exdir  = exbase+"/exec/"
fixdir = exbase+"/fix/"
#debug 
print("platforms.py exbase, exdir, fixdir = ","\n",exbase,"\n", exdir,"\n", fixdir, flush=True)

#--------------- Utility Functions --------------------------------
def parse_8digits(tag):
  tmp = int(tag)
  (yy,mm,dd) = (int(int(tmp)/10000),int((int(tmp)%10000)/100),int(tmp)%100)
  tag_out = datetime.date(int(yy), int(mm), int(dd))
  return tag_out

#----------------- High level declarations -----------------------------
# Directories w. verification data
dirs = {
  'imsdir'    : '' ,
  'ncepdir'   : '' ,
  'nsidcdir'  : '' ,
  'osisafdir' :''
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

#debug 
print("platforms.py machine = ",machine, flush=True)

if not machine:
    print ('ice verification is currently only supported on: %s' % ' '.join(machines))
    raise NotImplementedError('Cannot auto-detect platform, ABORT!')

#------------------------------------------------------------------
# Establish paths to verification data:
if (machine == 'HERA'):
  dirs['imsdir'] = '/home/Robert.Grumbine/clim_data/verification_data/ims/'
  dirs['ncepdir'] = '/home/Robert.Grumbine/clim_data/verification_data/ice5min/'
  #dirs['nsidcdir'] = '/home/Robert.Grumbine/clim_data/verification_data/nsidc.nc/'
  dirs['nsidcdir'] = '/home/Robert.Grumbine/clim_data/verification_data/G02202_V4/'
  dirs['osisafdir'] = '/home/Robert.Grumbine/clim_data/verification_data/osisaf/'
  dirs['fixdir']   = '/home/Robert.Grumbine/rgdev/fix'
elif (machine == 'Orion'):
  dirs['imsdir'] = '/home/rgrumbin/rgdev/verification_data/ims/'
  dirs['ncepdir'] = '/home/rgrumbin/rgdev/verification_data/ice5min/'
  dirs['nsidcdir'] = '/home/rgrumbin/rgdev/verification_data/G02202_V4/'
  dirs['osisafdir'] = '/home/rgrumbin/rgdev/verification_data/osisaf/'
  dirs['fixdir']   = '/home/rgrumbin/rgdev/ice_scoring/fix'
elif (machine == 'WCOSS_C'):
  dirs['imsdir'] = '/u/robert.grumbine/noscrub/verification/ims/'
  dirs['ncepdir'] = '/u/robert.grumbine/noscrub/verification/sice/'
  dirs['nsidcdir'] = '/u/robert.grumbine/noscrub/verification/G02202_V4/'
  dirs['osisafdir'] = '/u/robert.grumbine/noscrub/verification/osisaf/'
  dirs['fixdir']   = '/u/robert.grumbine/rgdev/ice_scoring/fix'
elif (machine == 'Gaea'):
  dirs['imsdir'] = '/lustre/f2/dev/ncep/Robert.Grumbine/CICE_INPUTDATA/Verification_data/ims/'
  dirs['ncepdir'] = '/lustre/f2/dev/ncep/Robert.Grumbine/CICE_INPUTDATA/Verification_data/ice5min/'
  dirs['nsidcdir'] = '/lustre/f2/dev/ncep/Robert.Grumbine/CICE_INPUTDATA/Verification_data/G02202_V4/'
  dirs['osisafdir'] = '/lustre/f2/dev/ncep/Robert.Grumbine/CICE_INPUTDATA/Verification_data/osisaf/'
  dirs['fixdir']   = '/lustre/f2/dev/ncep/Robert.Grumbine/fix'
elif (machine == 'RG_Home'):
  dirs['imsdir'] = '/Volumes/ncep/allconc/ims/'
  dirs['ncepdir'] = '/Volumes/ncep/allconc/ice5min/'
  dirs['nsidcdir'] = '/Volumes/ncep/allconc/nsidc_nc/'
  dirs['fixdir']   = '/u/Robert.Grumbine/para/mmablib/ice_scoring/fix'
else:
  print ('ice verification is currently only supported on: %s' % ' '.join(machines))
  raise NotImplementedError('Cannot find verification data directory, ABORT!')

#debug 
print("platforms.py fixdir = ", (dirs['fixdir']) , flush=True)
print("platforms.py os path exists ", os.path.exists(dirs['fixdir']), flush=True)
#debug0 exit(1)

#------------------------------------------------------------------
#Do we have the fixed files directory?
if (not os.path.exists(dirs['fixdir'])):
  print('no ice verification fixed (reference) directory ',dirs['fixdir'])
  raise NotImplementedError('Cannot find any verification fixed (reference) directory.  ABORT!')

#Do we have verification data directories?
nsidcverf = os.path.exists(dirs['nsidcdir'])
ncepverf  = os.path.exists(dirs['ncepdir'])
imsverf   = os.path.exists(dirs['imsdir'])
#debug 
print("platforms.py obsdirs: ",dirs['nsidcdir'], dirs['ncepdir'], dirs['imsdir'] , flush=True)

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

if (len(sys.argv) >  1) :
  if (sys.argv[1] == "trial"):
    print("Evaluation programs and scripts look ok to run on ",machine)
    print("ims dir   = ", dirs['imsdir'], imsverf)
    print("nsidc dir = ", dirs['nsidcdir'], nsidcverf)
    print("ncep dir  = ", dirs['ncepdir'], ncepverf)
    print("reference fixed files directory = ",dirs['fixdir'], flush=True)