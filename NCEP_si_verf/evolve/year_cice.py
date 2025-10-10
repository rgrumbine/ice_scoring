import sys
import os
import datetime


# -- ~universal environmental settings
FIXDIR=os.environ['HOME']+'/rg/fix/'
EXDIR=os.environ['HOME']+'/rgdev/ice_scoring/NCEP_si_verf/exec/'
OUTDIR=os.environ['HOME']+'/scratch/CICE_RUNS/'
#OUTDIR='/ncrc/home1/Robert.Grumbine/scratch/CICE_RUNS/generation1/'

# specific to given experiments
#EXPT='reference.evo0'
GEN   = sys.argv[1]
nexpt = int(sys.argv[2])
acrit = float(sys.argv[3])


start = datetime.date(2005,1,1)
end   = datetime.date(2005,12,31)
dt = datetime.timedelta(1)

for evo in range(0,nexpt):
  sno="{:d}".format(evo)
  tag   = start

  EXPT='/wcoss2_intel_smoke_gx3_1x1_evo'+sno+'_med3_yr_out.'+GEN
  if (not os.path.exists(OUTDIR+EXPT)):
      print("directory doesn't exist ",OUTDIR+EXPT)
      continue
  
  fname = 'fout'+sno

  if (not os.path.exists(fname)):
    fout = open(fname,'w')
    while (tag <= end):
      dtag=tag.strftime("%Y-%m-%d")
      cmd = EXDIR+'/cice_solo '+FIXDIR+'/seaice_gland5min '+OUTDIR+EXPT+ '/history/iceh.'+dtag+'.nc '+"{:.3f}".format(acrit) + ' ' + dtag + " >> "+ fname
      os.system(cmd)
      tag += dt

    fout.close()

