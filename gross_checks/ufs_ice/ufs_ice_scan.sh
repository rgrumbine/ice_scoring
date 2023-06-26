#!/bin/sh 

#Hera:

echo zzz module list
module list

set -x

echo zzz HOME = $HOME
export PYTHONPATH=$HOME/rgdev/mmablib/py:$HOME/rgdev/ice_scoring/gross_checks/shared
export MODDEF=$HOME/rgdev/ice_scoring/model_definitions

export OUTDIR=$HOME/clim_data/hr1
export level=extremes


for f in 20191203  20191221  20200108  20200126  20200213  20200604  20200622  20200710  20200728  20200815 20191206  20191224  20200111  20200129  20200216  20200607  20200625  20200713  20200731  20200818 20191209  20191227  20200114  20200201  20200219  20200610  20200628  20200716  20200803  20200821 20191212  20191230  20200117  20200204  20200222  20200613  20200701  20200719  20200806  20200824 20191215  20200102  20200120  20200207  20200225  20200616  20200704  20200722  20200809  20200827 20191218  20200105  20200123  20200210  20200601  20200619  20200707  20200725  20200812  20200830 
do
  tag=$f
  j=0
  while [ $j -le 15 ]
  do
    time python3 $GDIR/ufs_ice/ufs_ice.subset.py $modelout/$f/ice$tag.01.${f}00.subset.nc \
                          $GDIR/ufs_ice/ufs_ice.subset.$level redone > ice.subset.${f}.lead${j}.$level.results

    j=`expr $j + 1`
    tag=`expr $tag + 1`
    tag=`$HOME/bin/dtgfix3 $tag`
  done
done

cat ice.subset.*.results > all
for lead in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
  cat ice.subset.*.lead${lead}.results > all.lead.$lead
done

