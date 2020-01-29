#!/bin/bash --login

#coupled model CICE scoring
#Denise Worthen, Robert Grumbine 17 May 2018

#vtag = verification date
#tag  = forecast date

#export sys=theia
export sys=WCOSS

if [ $sys == 'WCOSS' ] ; then
#Wcoss:
#. /usrx/local/Modules/3.2.10/init/bash
  export OBS=/u/Robert.Grumbine/onoscrub/obs
  #RTOFS output:
  export RTOFS=/u/Robert.Grumbine/onoscrub/rtofs
  export RTOFS_CICE=/u/Robert.Grumbine/onoscrub/rtofs_cice
# and ensure data are available:
  ${OBS}/get2.sh
  ${RTOFS}/get_rtofs_history.sh
  ${RTOFS_CICE}/copy.sh
  cd /u/Robert.Grumbine/para/mmablib/ice_scoring/concentration/
else
#Theia:
. /usrx/local/Modules/3.2.10/init/bash
  export OBS=/scratch4/NCEPDEV/ocean/save/Denise.Worthen/IceData/RGobs
  #CICE output:
  export HyCICE=/scratch3/NCEPDEV/stmp2/Denise.Worthen/CICE003/history
  cd /u/Robert.Grumbine/para/mmablib/ice_scoring/concentration/
fi

#May need to change for different systems (tide/theia/cray/luna/...)
module purge
##Phase 1-2
#module load EnvVars ibmpe ics
#module load prod_util NetCDF grib_util
#Phase 3
module load ips/18.0.1.163
module load prod_envir/1.0.2
module load prod_util/1.1.0 grib_util/1.1.0
module load bufr_dumplist/2.0.0
module load dumpjb/5.0.0
module load NetCDF/4.5.0

module list

#Theia, CICE output:
export HyCICE=/scratch3/NCEPDEV/stmp2/Denise.Worthen/CICE003/history

#. = /u/Robert.Grumbine/para/mmablib/ice_scoring/concentration
export EXDIR=`pwd`
export FIXDIR=$EXDIR/../fix

start=20190301
end=`date +"%Y%m%d"`
end=20190320

export tag=$start
while [ $tag -le $end ] 
do

  vtag=$tag
  ym=`echo $tag | cut -c1-6`
  cdate=`echo $tag|cut -c1-4`-`echo $tag|cut -c5-6`-`echo $vtag|cut -c7-8`
  echo $cdate
  hh=000
  echo day $tag
  while [ $hh -le 192 ] 
  do
    echo hour scoreout.$tag.$hh
    if [ ! -f scores/scoreout.RTOFS.$tag.$hh ] ; then
  
      #Use this for recent (2017/10/17-present) ice observations
      if [ ! -f $OBS/ice.$vtag ] ; then
        if [ ! -f $OBS/seaice.t00z.5min.grb.grib2.$vtag ] ; then
          echo need the analysis file for $vtag
        else
          ${WGRIB2} $OBS/seaice.t00z.5min.grb.grib2.$vtag -order we:ns -bin $OBS/ice.$vtag
        fi
      fi
      # Use this for older (than 2017/10/17) ice observations
      #  vym=`echo $vtag | cut -c1-6`
      #  if [ -f $OBS/ice5min.grib2.${vym} ] ; then
      #    grep $vtag $OBS/index.$vym | ${WGRIB2} -i $OBS/ice5min.grib2.$vym -order we:ns  -bin obs/ice.$vtag
      #  fi
    
#if wcoss
      if [ -f $OBS/ice.$vtag  -a -f ${RTOFS}/${tag}/rtofs_glo_2ds_f${hh}_daily_diag.nc ] ; then
        echo scoring RTOFS date $tag at lead of $hh > scores/scoreout.RTOFS.$tag.$hh 
        ${EXDIR}/score_diag ${RTOFS}/${tag}/rtofs_glo_2ds_f${hh}_daily_diag.nc $OBS/ice.${vtag} ${FIXDIR}/skip_hr >> scores/scoreout.RTOFS.$tag.$hh
      fi 
# else theia:
      if [ -f $OBS/ice.$vtag  -a -f ${HyCICE}/iceh_24h.$cdate.nc ] ; then
        echo scoring CICE date $tag at lead of $hh > scores/scoreout.CICE.$tag.$hh 
        ${EXDIR}/score_diag ${HyCICE}/iceh_24h.$cdate.nc $OBS/ice.${vtag} ${FIXDIR}/skip_hr >> scores/scoreout.CICE.$tag.$hh
      fi
 
    fi

    vtag=`expr $vtag + 1`
    vtag=`/u/Robert.Grumbine/para/mmablib/mmablib/ush/dtgfix3 $vtag` 

    hh=`expr $hh + 24`
    if [ $hh -lt 100 ] ; then
      hh=0$hh
    fi 
  done


#################################
## Now that scores are computed, do any plotting:
  #./plot.RTOFS.sh
 

  tag=`expr $tag  + 1`
  tag=`/u/Robert.Grumbine/para/mmablib/mmablib/ush/dtgfix3 $tag`
done
