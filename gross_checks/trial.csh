#!/bin/csh -f
#SBATCH -J gross
#SBATCH -e gross.err
#SBATCH -o gross.out
#SBATCH -t 7:55:00
#SBATCH -q batch
#SBATCH -A marine-cpu
#SBATCH -N 1
#SBATCH --mail-type FAIL
#SBATCH --mail-user robert.grumbine@noaa.gov

# On Hera the python modules are too incomplete, must use personal copy
module use -a /contrib/anaconda/modulefiles
module load anaconda/latest

#cd /home/Robert.Grumbine/rgdev/mmablib/ice_scoring/gross_checks
cd /home/Robert.Grumbine/rgdev/ice_scoring/gross_checks
#cd $WORKING_DIRECTORY

setenv FCST_BASE /scratch2/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_p7/SeaIce/

time python3 -m cProfile -o stats.out wholesale_ice.py $FCST_BASE \
                          ctl/icesubset.extremes redone > gross.results

#time python3 -m cProfile -o stats.out gross_ice.py  $FCST_BASE/$tag/ice20120202.01.${tag}00.subset.nc \
#                            ctl/icesubset.vhigh redone > gross.results.$tag 

python3 statview.py stats.out > stats.summary

