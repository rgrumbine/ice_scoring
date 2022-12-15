#!/bin/bash
#PBS -N rtofs_eval
#PBS -o rtofs_eval
#PBS -j oe
#PBS -A ICE-DEV
#PBS -q dev
#PBS -l walltime=3:00:00
#PBS -l select=1:ncpus=1
#
echo hello from ice-dev

. $HOME/rgdev/toolbox/python_load.wcoss2

cd $HOME/rgdev/ice_scoring/gross_checks

export PYTHONPATH=$PYTHONPATH:$HOME/rgdev/ice_scoring/gross_checks/shared
export modelout=$HOME/noscrub/model_intercompare/rtofs_cice
export MODDEF=$HOME/rgdev/ice_scoring/model_definitions

#920++
for mm in 09 10 11 12
do
  for dd in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
  do
    for lead in n00 f24 f48 f72 f96 f120 f144 f168 f192
    do
      if [ -f $modelout/rtofs.2022${mm}${dd}/rtofs_glo.t00z.${lead}.cice_inst ] ; then
       python3 rtofs_cice.py \
           $modelout/rtofs.2022${mm}${dd}/rtofs_glo.t00z.${lead}.cice_inst \
           rtofs_cice/rtofs_cice.extremes fly > beta.${mm}${dd}.${lead}
      fi
    done
  done
  cat beta.${mm}*.* > beta.$mm
  python3 plot_errs.py beta.$mm early_$mm

done
