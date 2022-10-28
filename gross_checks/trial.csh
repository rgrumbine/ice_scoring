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

echo $HOME
setenv PYTHONPATH $HOME/rgdev/mmablib/py

#cd $WORKING_DIRECTORY
cd $HOME/rgdev/ice_scoring/gross_checks

#setenv FCST_BASE /scratch2/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_p7/SeaIce/
setenv FCST_BASE /scratch1/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_p8/SeaIce/ 


setenv level extremes
time python3 -m cProfile -o stats.out wholesale_ice.py $FCST_BASE \
                          ctl/icesubset.$level redone > $level.results

#time python3 -m cProfile -o stats.out gross_ice.py \
#      $FCST_BASE/$tag/ice20120202.01.${tag}00.subset.nc \
#          ctl/icesubset.$level redone > gross.results.$tag 

python3 statview.py stats.out > stats.summary
