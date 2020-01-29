#!/bin/csh -f
#SBATCH -J bm3_v2018
#SBATCH -e bm3_v2018.err
#SBATCH -o bm3_v2018.out
#SBATCH -t 7:55:00
#SBATCH -q batch
#SBATCH -A marine-cpu
#SBATCH -N 1
#SBATCH --mail-type FAIL
#SBATCH --mail-user robert.grumbine@noaa.gov

source /etc/profile.d/modules.csh
setenv PATH /scratch2/NCEPDEV/climate/Robert.Grumbine/anaconda3/bin:$PATH
module load hpss

setenv EXDIR /scratch2/NCEPDEV/climate/Robert.Grumbine/bm3.verf
setenv FCST_BASE /scratch2/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_b3/SeaIce/ 

#How to connect to x display?
setenv XDG_RUNTIME_DIR /scratch2/NCEPDEV/climate/Robert.Grumbine/runtime
if ( ! -d $XDG_RUNTIME_DIR ) then
  mkdir -p -m 700 $XDG_RUNTIME_DIR
endif

setenv expt bm3
cd /scratch2/NCEPDEV/climate/Robert.Grumbine/${expt}.verf
setenv base `pwd`

setenv x `date`
echo start of loop at $x

foreach yy ( 2018 )
  foreach mm ( 01 02 03 04 05 06 07 08 09 10 11 12 )
    foreach dd ( 01 15 )
      setenv tag ${yy}${mm}${dd}
      setenv initial ${yy}${mm}${dd}
      setenv OUT $base/out.$initial
      if ( ! -d $OUT ) then
        mkdir $OUT
      endif

      if ( -d ${FCST_BASE}/${initial}/6hrly ) then
        echo assessing experiment from $initial
        setenv i 0
        while ( $i < 35 )
          setenv tag `expr $tag + 1`
          setenv tag `dtgfix3 $tag`
          setenv i   `expr $i + 1`
          # -m cProfile -o pystats.$tag.$i to generate profiling 
          #   stats for later analysis. Optional
          python3  $EXDIR/setup_verf_ice.py $initial $tag ${FCST_BASE}/${initial}/6hrly/ >>& $expt.$initial.$tag.out
          mv fcst_edge.$tag          $OUT
          mv edge.fcst.*.*.$tag      $OUT
        end
        mv $expt.$initial.*.out $OUT

# Per-forecast statistics, graphics
        time python3 $EXDIR/contingency_plots.py 35 $initial 0.15 
        echo time python3 $EXDIR/contingency_plots.py 35 $initial 0.15 >> $OUT/to_run
        mv *${initial}.png                $OUT
        mv score*${initial}.csv           $OUT
      else
        echo no experiment output for $initial 00 yet
      endif

    end
  end
end

setenv x `date`
echo end of $expt forecast verification at $x
