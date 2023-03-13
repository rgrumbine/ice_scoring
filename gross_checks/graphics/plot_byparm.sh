#!/bin/sh

. $HOME/rgdev/toolbox/misc/python_load.wcoss2

fn=$1
export nmax=`wc -l $fn | cut -f1 -d\ `
export nmax=`expr $nmax \/ 16`
echo $nmax
#nmax=30000
#exit

for p in aice albsni congel divu evap_ai fhocn_ai flat_ai flwdn flwup_ai frazil fresh_ai frzmlt fsalt_ai fsens_ai fswabs_ai fswdn fswfac fswthru_ai hi hs meltb meltl meltt opening rain_ai shear sice sig1 sig2 snoice snow_ai sss sst strairx strairy strcorx strcory strength strocnx strocny Tair Tsfc uatm uocn uvel vatm vocn vvel 
#"fswabs " "snow "  
do
  x=`grep -c $p $fn`
  echo $x $p >> $fn.parms
  grep $p $fn | grep ' pm' | sort -nr -k 6 >  $p.s
  if [ $x -ge $nmax ] ; then
    python3 $HOME/rgdev/ice_scoring/gross_checks/plot_errs.py $p.s $p 4.
  fi
done
