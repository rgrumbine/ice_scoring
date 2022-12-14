#!/bin/csh -fx
#SBATCH -J gross
#SBATCH -e gross.err
#SBATCH -o gross.out
#SBATCH -t 0:55:00
#SBATCH -q batch
#SBATCH -A marine-cpu
#SBATCH -N 1
#SBATCH --mail-type FAIL
#SBATCH --mail-user robert.grumbine@noaa.gov

# On Hera the python modules are too incomplete, must use personal copy
source /etc/profile.d/modules.csh

module use -a /contrib/anaconda/modulefiles
module load anaconda/latest

echo zzz module list
module list

set -x
echo zzz HOME = $HOME
setenv PYTHONPATH $HOME/rgdev/mmablib/py:$HOME/rgdev/ice_scoring/gross_checks/shared

setenv FCST_BASE /scratch1/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_p8/SeaIce/ 

setenv OUTDIR $HOME/clim_data/prototype_evaluations

#cd $WORKING_DIRECTORY
cd $HOME/rgdev/ice_scoring/gross_checks
setenv base `pwd`

setenv level extremes
time python3 -m cProfile -o stats.out $base/ufs_ice/wholesale_ice.py $FCST_BASE \
                          $base/ctl/icesubset.$level redone > $OUTDIR/$level.results

#time python3 -m cProfile -o stats.out gross_ice.py \
#      $FCST_BASE/$tag/ice20120202.01.${tag}00.subset.nc \
#          ctl/icesubset.$level redone > gross.results.$tag 

python3 statview.py stats.out > stats.summary
