#!/bin/bash
#PBS -N rtofs_eval
#PBS -o rtofs_eval
#PBS -j oe
#PBS -A ICE-DEV
#PBS -q dev
#PBS -l walltime=1:00:00
#PBS -l select=1:ncpus=1
#


# Run time is about 1 hour per month on rtofs_cice

. $HOME/rgdev/toolbox/misc/python_load.wcoss2

export GDIR=$HOME/rgdev/ice_scoring/gross_checks
cd $GDIR

export PYTHONPATH=$PYTHONPATH:$HOME/rgdev/ice_scoring/gross_checks/shared
export MODDEF=$HOME/rgdev/ice_scoring/model_definitions
export modelout=$HOME/noscrub/model_intercompare/rtofs_cice

tag=20230306
while [ $tag -le 20230311 ] 
do
  mm=`echo $tag | cut -c5-6`
  dd=`echo $tag | cut -c7-8`
  for lead in n00 f24 f48 f72 f96 f120 f144 f168 f192
  do
    if [ -f $modelout/rtofs.${tag}/rtofs_glo.t00z.${lead}.cice_inst ] ; then
     time python3 $GDIR/rtofs_cice/rtofs_cice.py \
         $modelout/rtofs.${tag}/rtofs_glo.t00z.${lead}.cice_inst \
         $GDIR/rtofs_cice/rtofs_cice.extremes fly > beta.$tag.${lead}
     mv fhistogram fhistogram.$tag.$lead
    fi
  done

  tag=`expr $tag + 1`
  tag=`dtgfix3 $tag`
done
#  cat beta.${mm}*.* > beta.$mm
#  python3 $GDIR/plot_errs.py beta.$mm early_$mm
