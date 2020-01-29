#!/bin/sh
#2 April 2014  Robert Grumbine
#9 June 2018

FCSTDIR=/Volumes/ncep/final.drift.archive/fcsts/
OBSDIR=/Volumes/APPS/

#AMSRE 20021001-20110430
#AMSR2 20120928-20YYMMDD

end=20110430
end=20180501

for LEAD in 3 6
#for LEAD in 3
do
  #tag=20021001
  tag=20120928
  while [ $tag -le $end ]
  do
    if [ -f $FCSTDIR/sk2.$tag -a -f $OBSDIR/ifremer${LEAD}/${tag}.txt ] ; then
      ln -sf $OBSDIR/ifremer${LEAD}/${tag}.txt dboydata
      for RANGE in 30 25 20 15 10 5
      #for RANGE in 10
      do
        ./ifremercheck $RANGE 3 ${LEAD} matchup.$tag.${LEAD}.$RANGE \
                 $FCSTDIR/sk2.$tag > score.$tag.${LEAD}.$RANGE
      done
    fi

    tag=`expr $tag + 1`
    tag=`dtgfix3 $tag`
  done
done
