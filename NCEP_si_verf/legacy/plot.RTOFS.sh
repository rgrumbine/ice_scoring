#!/bin/sh
#Plot all forecast leads from a date

#tag must be exported from caller:

cd scores/

for hhh in 000 024 048 072 096 120 144 168 192
do
  if [ ! -f score.$tag.$hhh.png -a -f scoreout.RTOFS.$tag.$hhh ] ; then
    grep -v hlevel scoreout*.$tag.$hhh | grep -v scoring > glob.$tag.$hhh
    grep nhlevel scoreout*.$tag.$hhh | grep -v scoring > nh.$tag.$hhh
    grep shlevel scoreout*.$tag.$hhh | grep -v scoring > sh.$tag.$hhh

    echo set grid > gin
    echo set term png >> gin
    echo set out \"score.$tag.$hhh.png\" >> gin
    echo set ylabel \"Threat score\" >> gin
    echo set xlabel \"Concentration cutoff\" >> gin
  
    echo plot \[0:1\]\[0:1\] \"glob.$tag.$hhh\" using 2:11 with lp \\ >> gin
    echo title \"Global forecast from $tag lead $hhh hours\" ,\\ >> gin
    echo \"nh.$tag.$hhh\" using 2:11 with lp title \"Northern Hemisphere\" ,\\ >> gin
    echo \"sh.$tag.$hhh\" using 2:11 with lp title \"Southern Hemisphere\" >> gin
  
    gnuplot gin
    rm glob.$tag.$hhh nh.$tag.$hhh sh.$tag.$hhh gin

    #scp -p score.$tag.$hhh.png seaice@emcrzdm:/home/www/polar/seaice/yopp/scoring/rtofs-ops 2> /dev/null
    #To keep most recent in window:
    #scp -p score.$tag.$hhh.png seaice@emcrzdm:/home/www/polar/seaice/yopp/scoring/score.$hhh.png 2> /dev/null
  
  fi
done
############### Plot die-off curves for a day, for a level:
for level in 0.15 0.60 
do

  for f in g15 n15 s15
  do
    if [ -f $f ] ; then
      rm $f
    fi
  done
  for hhh in 000 024 048 072 096 120 144 168 192
  do
    gline=`grep " $level " scoreout*.$tag.$hhh | grep -v hlevel`
    nline=`grep " $level " scoreout*.$tag.$hhh | grep nhlevel`
    sline=`grep " $level " scoreout*.$tag.$hhh | grep shlevel`
    echo $hhh $gline >> g15
    echo $hhh $nline >> n15
    echo $hhh $sline >> s15
  done
  x=0
  x=`grep -c level g15 ` # Will be 9 if we have full set of fcsts
  echo x = $x

  #Plot the die-off curves:
  if [ \( ! -f dieoff.$tag.$level.png \) -a \( $x -eq 9 \) ] ; then
    echo set grid > gin
    echo set term png                 >> gin
    echo set out \"dieoff.$tag.$level.png\" >> gin
    echo set ylabel \"Threat score\"         >> gin
    echo set xlabel \"Forecast Lead \(hr\)\" >> gin
    echo set xtic 24                 >> gin
  
    echo plot \[0.:\]\[0.5:1\] \"g15\" using 1:12 with lp \\         >> gin
    echo title \"Global forecast from $tag level $level\" ,\\         >> gin
    echo \"n15\" using 1:12 with lp title \"Northern Hemisphere\" ,\\ >> gin
    echo \"s15\" using 1:12 with lp title \"Southern Hemisphere\"     >> gin
    gnuplot gin
  
    rm [nsg]15 gin
    #scp -p dieoff.$tag.$level.png seaice@emcrzdm:/home/www/polar/seaice/yopp/scoring/rtofs-ops 2> /dev/null
    #scp -p dieoff.$tag.$level.png seaice@emcrzdm:/home/www/polar/seaice/yopp/scoring/dieoff.$level.png 2> /dev/null
  fi

done
