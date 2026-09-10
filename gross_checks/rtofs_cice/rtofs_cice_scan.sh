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
export MODEL=${MODEL:-rtofs_cice}

#set by calling script -----------------------------------------
export GDIR=$HOME/rgdev/ice_scoring/gross_checks

set -x

export PYTHONPATH=$PYTHONPATH:$HOME/rgdev/ice_scoring/gross_checks/gross
export MODDEF=$HOME/rgdev/ice_scoring/gross_checks/model_definitions

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
      if [ ! -f beta.$tag.${lead} ] ; then
      time python3 $GDIR/$MODEL/$MODEL.py \
          $modelout/rtofs.${tag}/rtofs_glo.t00z.${lead}.cice_inst.nc \
          $GDIR/ctl/$MODEL.$level fly > beta.$tag.${lead}
      mv fhistogram fhistogram.$tag.$lead
      fi

    elif [ -f $modelout/${tag}/rtofs_glo.t00z.${lead}.cice_inst.nc ] ; then
      if [ ! -f beta.$tag.${lead} ] ; then
      time python3 $GDIR/$MODEL/$MODEL.py \
          $modelout/${tag}/rtofs_glo.t00z.${lead}.cice_inst.nc \
          $GDIR/ctl/$MODEL.$level fly > beta.$tag.${lead}
      mv fhistogram fhistogram.$tag.$lead
      fi
    fi
  done

  tag=`expr $tag + 1`
  tag=`dtgfix3 $tag`
done

# Now that all results have been scanned, check for errors:---------------------------

# For plots, last number is dot size. Expect fewer pts as go down list,
#    so make pts larger
cat beta.*.* > all.$MODEL

for model in $MODEL
do
  python3 $GDIR/graphics/plot_errs.py all.$model all.$model 12.

  python3 $GDIR/exceptions/exceptions.py $GDIR/exceptions/physical.exceptions.$model all.$model > nonphysical.$model
  python3 $GDIR/graphics/plot_errs.py nonphysical.$model nonphysical.$model 12.

  python3 $GDIR/exceptions/exceptions.py $GDIR/exceptions/known.errors nonphysical.$model > unknown.$model
  python3 $GDIR/graphics/plot_errs.py unknown.$model unknown.$model 12.
done

#-------------------------------------------------------------------------

for lead in n00 f24 f48 f72 f96 f120 f144 f168 f192
do
  cat beta.*.$lead > all.$MODEL.$lead
done

# ------------------ plot by parameter
for model in $MODEL
do
  #$GDIR/$model/${model}_split.sh unknown.$model
  $GDIR/$model/${model}_split.sh nonphysical.$model
  if [ ! -d $model ] ; then
    mkdir $model
  fi
  for f in *.s
  do
    if [ -s $f ] ; then
      python3 $GDIR/graphics/plot_errs.py $f $f 12
    fi
  done
  mv *.png *.s $model
# ------------------ copy to desk for pseudo-web
  cd $model
  # need dtn node: scp -p *.png rgrumbine@emcrzdm:rgweb/ice/gross/$model
# qsub $HOME/rgdev/forweb/cp_rtofs_gross
done
