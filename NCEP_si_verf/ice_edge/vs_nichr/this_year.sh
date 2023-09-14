#!/bin/sh

set -xe
year=`date +"%Y"`

for lead in 1 2 3 4 5 6 7 8 10 16
do
  grep rms persist/nic_v_nic.$lead/*.n.${year}* > nrms.$lead.$year 
  grep rms persist/nic_v_nic.$lead/*.s.${year}* > srms.$lead.$year 
  python3 edge_rmse_series_plot.py nrms.$lead.$year $lead "${year}_NH"
  python3 edge_rmse_series_plot.py srms.$lead.$year $lead "${year}_SH"
done

scp -p *${year}*.png seaice@emcrzdm:polar/ice_edge/nic_v_nic/
