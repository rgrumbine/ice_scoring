import os
import sys
import copy
from abc import ABC

'''
Define an abstract base class for computing platforms, make it easier to ensure that necessities are present

'''
#------------------------------------------------------------------

#----------------- High level declarations -----------------------------
# Directories w. verification data
dirs = {
  'verf_head' : '' ,
  'edgedir'   : '' ,
  'imsdir'    : '' ,
  'ncepdir'   : '' ,
  'nsidcdir'  : '' ,
  'osisafdir' : ''
}

class platform(ABC):
  def __init__(self, name, dirtag):
    self.name = name
    self.dirtag = dirtag
  # then after initializing, update 'machines'
    self.dirs = {
      'verf_head' : '' ,
      'edgedir'   : '' ,
      'imsdir'    : '' ,
      'ncepdir'   : '' ,
      'nsidcdir'  : '' ,
      'osisafdir' : ''
    }

  #def is_machine(self, name):
  #  return(self.name == name)

  def is_machine(self):
    #debug: print("dirtag = ",self.dirtag, flush=True)
    #debug: print(os.path.exists(self.dirtag), flush=True)
    return(os.path.exists(self.dirtag))


#----------------- Identify our machines -----------------------------

mlist = []

# Known computing platforms:
mlist += [platform('WCOSS'         , '/etc/wcoss.conf')]
mlist += [platform('WCOSS_DELL_P3' , '/gpfs/dell2')]
mlist += [platform('Orion'         , '/home/rgrumbin')]
mlist += [platform('Gaea'          , '/gpfs/f5/nggps_emc/')]
mlist += [platform('RG_Home'       , '/Volumes/ncep')]
mlist += [platform('HERA'          , '/scratch1')]
# Add yours here in same vein, and then below specify the paths

#debug: print(len(mlist), flush=True)

nomachine = True
for i in range(0, len(mlist)):
  if (mlist[i].is_machine() ):
    print("on machine ",mlist[i].name, flush=True)
    machine = copy.deepcopy(mlist[i])  # make this a 'platform'
    nomachine = False
    break

if (nomachine == True):
    raise NotImplementedError('Cannot auto-detect platform, ABORT!')

##------------------------------------------------------------------
## Establish paths to verification data:
if (machine.name == 'HERA'):
  machine.dirs['verf_head'] = '/home/Robert.Grumbine/clim_data/verification_data/'
  machine.dirs['edgedir']   = machine.dirs['verf_head']+'/edges/'
  machine.dirs['imsdir']    = machine.dirs['verf_head']+'/ims/'
  machine.dirs['ncepdir']   = machine.dirs['verf_head']+'/ice5min/'
  machine.dirs['nsidcdir']  = machine.dirs['verf_head']+'/G02202_V4/'
  machine.dirs['osisafdir'] = machine.dirs['verf_head']+'/osisaf/'
  machine.dirs['fixdir']   = '/home/Robert.Grumbine/rg/fix'
elif (machine.name == 'Orion'):
  machine.dirs['imsdir'] = '/home/rgrumbin/rgdev/verification_data/ims/'
  machine.dirs['ncepdir'] = '/home/rgrumbin/rgdev/verification_data/ice5min/'
  machine.dirs['nsidcdir'] = '/home/rgrumbin/rgdev/verification_data/G02202_V4/'
  machine.dirs['osisafdir'] = '/home/rgrumbin/rgdev/verification_data/osisaf/'
  machine.dirs['fixdir']   = '/home/rgrumbin/rgdev/ice_scoring/fix'
elif (machine.name == 'WCOSS'):
  machine.dirs['imsdir'] = '/u/robert.grumbine/noscrub/verification/ims/'
  machine.dirs['ncepdir'] = '/u/robert.grumbine/noscrub/verification/sice/'
  machine.dirs['nsidcdir'] = '/u/robert.grumbine/noscrub/verification/G02202_V4/'
  machine.dirs['osisafdir'] = '/u/robert.grumbine/noscrub/verification/osisaf.met.no/'
  machine.dirs['fixdir']   = '/u/robert.grumbine/rg/fix'
elif (machine.name == 'Gaea'):
  machine.dirs['imsdir'] = '/lustre/f2/dev/ncep/Robert.Grumbine/CICE_INPUTDATA/Verification_data/ims/'
  machine.dirs['ncepdir'] = '/lustre/f2/dev/ncep/Robert.Grumbine/CICE_INPUTDATA/Verification_data/ice5min/'
  machine.dirs['nsidcdir'] = '/lustre/f2/dev/ncep/Robert.Grumbine/CICE_INPUTDATA/Verification_data/G02202_V4/'
  machine.dirs['osisafdir'] = '/lustre/f2/dev/ncep/Robert.Grumbine/CICE_INPUTDATA/Verification_data/osisaf/'
  machine.dirs['fixdir']   = '/lustre/f2/dev/ncep/Robert.Grumbine/fix'
elif (machine.name == 'RG_Home'):
  machine.dirs['imsdir'] = '/Volumes/ncep/allconc/ims/'
  machine.dirs['ncepdir'] = '/Volumes/ncep/allconc/ice5min/'
  machine.dirs['nsidcdir'] = '/Volumes/ncep/allconc/nsidc_nc/'
  machine.dirs['fixdir']   = '/u/Robert.Grumbine/para/mmablib/ice_scoring/fix'

##------------------------------------------------------------------
##Do we have the fixed files directory?
if (not os.path.exists(machine.dirs['fixdir'])):
  print('no ice verification fixed (reference) directory ',machine.dirs['fixdir'])
  raise NotImplementedError('Cannot find any verification fixed (reference) directory.  ABORT!')

#debug: print (machine.dirs, flush=True)

#Do we have verification data directories?
nsidcverf = os.path.exists(machine.dirs['nsidcdir'])
ncepverf  = os.path.exists(machine.dirs['ncepdir'])
imsverf   = os.path.exists(machine.dirs['imsdir'])
osisafverf   = os.path.exists(machine.dirs['osisafdir'])

#debug: print (nsidcverf , ncepverf , imsverf , osisafverf, flush=True )

if (not nsidcverf and not ncepverf and not imsverf and not osisafverf ):
  print('no ice verification directory is present, aborting')
  print('tried verification directories ', machine.dirs['nsidcdir'], machine.dirs['ncepdir'], machine.dirs['imsdir'], machine.dirs['osisafdir'] )
  raise NotImplementedError('Cannot find any verification data directories, ABORT!')
##------------------------------------------------------------------
##Variables established by this script:
##  machines (a dictionary of machine identifiers)
##  dirs (a dictionary of directory paths)
##  execdir (location of executables, needs EXDIR environment variable)
##  fixdir (location of executables, needs EXDIR environment variable)
##  imsdir, ncepdir, nsidcdir, fixdir (entries to dictionary) 
#
if (len(sys.argv) >  1) :
  if (sys.argv[1] == "trial"):
    print("Evaluation programs and scripts look ok to run on ",machine)
    print("ims dir   = ", machine.dirs['imsdir'], imsverf)
    print("nsidc dir = ", machine.dirs['nsidcdir'], nsidcverf)
    print("osisaf dir = ", machine.dirs['osisafdir'], nsidcverf)
    print("ncep dir  = ", machine.dirs['ncepdir'], ncepverf)
    print("reference fixed files directory = ",machine.dirs['fixdir'], flush=True)
