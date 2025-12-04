#!/bin/sh

if [ $# -eq 1 ] ; then
  fname=$1
else
  echo need a file to work on
  exit 1
fi

for f in hi_h hs_h Tsfc_h aice_h uvel_h vvel_h uatm_h vatm_h sice_h fswdn_h flwdn_h rain_h sst_h sss_h uocn_h vocn_h frzmlt_h scale_factor_h fswabs_h albsni_h alvdr_h alidr_h alvdf_h alidf_h flat_h fsens_h flwup_h evap_h Tair_h Tref_h Qref_h congel_h frazil_h snoice_h dsnow_h snow_h meltt_h melts_h meltb_h meltl_h fresh_h fsalt_h fbot_h fhocn_h strairx_h strairy_h strocnx_h strocny_h divu_h shear_h dvidtt_h dvidtd_h daidtt_h daidtd_h mlt_onset_h frz_onset_h sitemptop_h sitempsnic_h sitempbot_h apond_h hpond_h ipond_h apeff_h 
do
  grep $f $fname | grep -v excessive | grep pm | sort -nr -k 6,6 > ${f}.s
done

wc *.s | sort -n
#find . -maxdepth 1 -name '*.s' -size 0 -exec rm {} \;

# have to do snow_h separately as grep collides w. dsnow
