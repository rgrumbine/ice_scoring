import os
import datetime


# -- universal environmental settings
FIXDIR=os.environ['HOME']+'/rg/fix/'
EXDIR=os.environ['HOME']+'/rgdev/ice_scoring/NCEP_si_verf/exec/'
OUTDIR=os.environ['HOME']+'/scratch/CICE_RUNS/'

acrit = 0.0

start = datetime.date(2005,1,1)
end   = datetime.date(2005,12,31)
dt = datetime.timedelta(1)

# specific to given experiments
evo=0
for EXPT in ('gaea_intel_smoke_gx3_1x1_med3_nodyn_yr_out',
             'gaea_intel_smoke_gx3_1x1_med3_nodyn_upwind_yr_out',
             'gaea_intel_smoke_gx3_1x1_med3_nodyn_notrans_yr_out',
             'gaea_intel_smoke_gx3_1x1_med3_nodyn_notrans_upwind_yr_out'
            ):

  print(EXPT)
  tag   = start

  sno="{:d}".format(evo)
  fname = 'fout'+sno

  fout = open(fname,'w')
  while (tag <= end):
    dtag=tag.strftime("%Y-%m-%d")
    cmd = EXDIR+'/cice_solo '+FIXDIR+'/seaice_gland5min '+OUTDIR+EXPT+ '/history/iceh.'+dtag+'.nc '+"{:.3f}".format(acrit) + ' ' + dtag + " >> "+ fname
    os.system(cmd)
    tag += dt
  fout.close()
  evo += 1
