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
setenv PATH ${PATH}:/home/Robert.Grumbine/clim_data/anaconda3/bin

# 
#cd /home/Robert.Grumbine/rgdev/mmablib/ice_scoring/gross_checks
cd $WORKING_DIRECTORY

time python3 -m cProfile -o stats.out wholesale_ice.py data/ice2012020200.01.2012010100.subset.nc icesubset.vhigh redone > gross.results
python3 statview.py stats.out > stats.summary

