#!/bin/csh -f
#SBATCH -J p6_11
#SBATCH -e p6_11.err
#SBATCH -o p6_11.out
#SBATCH -t 7:55:00
#SBATCH -q batch
#SBATCH -A marine-cpu
#SBATCH -N 1
#SBATCH --mail-type FAIL
#SBATCH --mail-user USER@system

#Orion
#  tbd
#WCOSS
#  tbd

#Hera:
source /etc/profile.d/modules.csh
module load intel/2020.2
module load impi/2020.2
module load netcdf/4.7.0
module load wgrib2/2.0.8

module use -a /contrib/anaconda/modulefiles
module load anaconda/latest 

#All systems:
module list

setenv USER $user

setenv expt p6.0
setenv FCST_BASE /scratch2/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_p6/SeaIce/ 
setenv EXDIR   /scratch2/NCEPDEV/climate/${USER}/prototype_evaluations/${expt}.verf
setenv RUNBASE /scratch2/NCEPDEV/stmp1/${USER}/prototype_evaluations/${expt}.verf
cd /scratch2/NCEPDEV/climate/${USER}/prototype_evaluations/${expt}.verf
setenv base `pwd`

setenv mmablib /scratch2/NCEPDEV/climate/Robert.Grumbine/mmablib/

echo env $FCST_BASE $EXDIR $base $RUNBASE

# Fewer changes below here -------------------------------------------------

#setenv PATH /scratch2/NCEPDEV/climate/Robert.Grumbine/anaconda3/bin:$PATH

#For batch python graphics
setenv XDG_RUNTIME_DIR /scratch2/NCEPDEV/climate/${USER}/runtime
if ( ! -d $XDG_RUNTIME_DIR ) then
  mkdir -p -m 700 $XDG_RUNTIME_DIR
endif
echo $XDG_RUNTIME_DIR for python graphic support
setenv MPLCONFIGDIR /scratch2/NCEPDEV/climate/${USER}/runtime


setenv x `date`
echo start of loop at dtime $x

foreach yy ( 2011 )
  setenv RUNDIR ${RUNBASE}/$yy
  if ( ! -d $RUNDIR ) then
    mkdir -p $RUNDIR
  endif
  cd $RUNDIR
  #if ( $? -ne 0 ) then
  #  echo could not move to rundir $RUNDIR
  #  exit 1
  #endif

  foreach mm ( 04 05 06 07 08 09 10 11 12 )
    foreach dd ( 01 15 )
      setenv tag ${yy}${mm}${dd}
      setenv initial ${yy}${mm}${dd}
      setenv OUT $base/out.$initial
      if ( ! -d $OUT ) then
        mkdir $OUT
      else
        continue
      endif

      if ( -d ${FCST_BASE}/${initial}/6hrly ) then
        echo assessing experiment from $initial
        setenv i 0
        while ( $i < 35 )
          setenv tag `expr $tag + 1`
          setenv tag `$mmablib/ush/dtgfix3 $tag`
          setenv i   `expr $i + 1`
          # -m cProfile -o pystats.$tag.$i to generate profiling 
          #   stats for later analysis. Optional
          python3  $EXDIR/setup_verf_ice.py $initial $tag ${FCST_BASE}/${initial}/6hrly/ >>& $expt.$initial.$tag.out
          if ( -f fcst_edge.$tag ) then
            mv fcst_edge.$tag          $OUT
            mv edge.fcst.*.*.$tag      $OUT
          endif
        end
        mv $expt.$initial.*.out $OUT

# Per-forecast statistics, graphics
        time python3 $EXDIR/contingency_plots.py 35 $initial 0.15 $expt 
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
