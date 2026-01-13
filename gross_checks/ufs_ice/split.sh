#!/bin/sh

if [ $# -eq 1 ] ; then
  fname=$1
else
  echo need a file to work on
  exit 1
fi

for f in albsni_h congel_h daidtd_h daidtt_h divu_h dsnow_h dvidtd_h dvidtt_h evap_h fbot_h fhocn_h flat_h flwup_h flwdn_h frazil_h fresh_h frzmlt_h fsalt_h fsens_h fswabs_h fswdn_h hi_h hpond_h ipond_h meltb_h melts_h meltt_h Qref_h rain_h scale_factor_h shear_h sice_h sitempbot_h sitempsnic_h snoice_h sss_h sst_h strairx_h strairy_h strocnx_h strocny_h Tref_h uatm_h uocn_h uvel_h vatm_h vocn_h vvel_h
do
  grep $f $fname | grep -v excessive | grep pm | sort -nr -k 6,6 > ${f}.s
done
wc *.s | sort -n

