
#Model specific names of grid specifications are in 2nd argument (cice.header here)
#Model variable names and their bounds are in ctl/icesubset.high (here)
#'beta' is an optional argument, useful when bounds are unknown but variable names are

export MODDEF=../model_definitions

yy=1994
while [ $yy -le 2023 ] 
#while [ $yy -le 1994 ] 
do
  #for mm in 05 11
  for mm in 11 
  do
    tag=${yy}${mm}01
    time python3 ensemble.py $HOME/clim_data/sfs/gefs.${tag}/ cice.header sfs.199611 gamma > bout.$yy.$mm
  done
  yy=`expr $yy + 1`
done
