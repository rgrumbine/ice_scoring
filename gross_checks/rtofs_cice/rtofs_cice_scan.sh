#!/bin/bash
# --- Hera
#SBATCH -J eval_rtofs
#SBATCH -e eval_rtofs
#SBATCH -o eval_rtofs
#SBATCH -t 4:25:00
#SBATCH -q batch
#SBATCH -A marine-cpu
#SBATCH -N 1
#SBATCH --mail-type FAIL
#SBATCH --mail-user robert.grumbine@noaa.gov
# --- Hera
# --- Wcoss2
##PBS -N rtofs_eval
##PBS -o rtofs_eval
##PBS -j oe
##PBS -A ICE-DEV
##PBS -q dev
##PBS -l walltime=4:25:00
##PBS -l select=1:ncpus=1
#Wcoss2

# Run time is about 1 hour per month on rtofs_cice
export MODEL=rtofs_cice

#set by calling script -----------------------------------------
export GDIR=$HOME/rgdev/ice_scoring/gross_checks

set -x

export PYTHONPATH=$PYTHONPATH:$HOME/rgdev/ice_scoring/gross_checks/shared
export MODDEF=$HOME/rgdev/ice_scoring/model_definitions

export modelout=${modelout:-$HOME/noscrub/model_intercompare/rtofs_cice}
#export modelout=${modelout:-$HOME/clim_data/rtofs_gross/}

export start=${start:-20260321}
export end=${end:-20260331}
export level=${level:-extreme}

tag=$start
while [ $tag -le $end ] 
do
  mm=`echo $tag | cut -c5-6`
  dd=`echo $tag | cut -c7-8`
  for lead in n00 f24 f48 f72 f96 f120 f144 f168 f192
  do
    if [ -f $modelout/rtofs.${tag}/rtofs_glo.t00z.${lead}.cice_inst.nc ] ; then
      time python3 $GDIR/$MODEL/$MODEL.py \
          $modelout/rtofs.${tag}/rtofs_glo.t00z.${lead}.cice_inst.nc \
          $GDIR/ctl/$MODEL.$level fly > beta.$tag.${lead}
      mv fhistogram fhistogram.$tag.$lead

    elif [ -f $modelout/${tag}/rtofs_glo.t00z.${lead}.cice_inst.nc ] ; then
      time python3 $GDIR/$MODEL/$MODEL.py \
          $modelout/${tag}/rtofs_glo.t00z.${lead}.cice_inst.nc \
          $GDIR/ctl/$MODEL.$level fly > beta.$tag.${lead}
      mv fhistogram fhistogram.$tag.$lead
    fi
  done

  tag=`expr $tag + 1`
  tag=`dtgfix3 $tag`
done

