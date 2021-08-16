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

setenv USER $user

#Orion
#  tbd
#WCOSS
#  tbd

#Hera:
#source /etc/profile.d/modules.csh
#module load intel/2020.2
#module load impi/2020.2
#module load netcdf/4.7.0
#module load wgrib2/2.0.8
#
#setenv mmablib /scratch2/NCEPDEV/climate/Robert.Grumbine/mmablib/
#
#module use -a /contrib/anaconda/modulefiles
#module load anaconda/latest 
#setenv XDG_RUNTIME_DIR /scratch2/NCEPDEV/climate/${USER}/runtime
#setenv MPLCONFIGDIR    /scratch2/NCEPDEV/climate/${USER}/runtime

setenv expt p6.0
setenv FCST_BASE /scratch2/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_p6/SeaIce/ 
setenv EXDIR     /scratch2/NCEPDEV/climate/${USER}/prototype_evaluations/${expt}.verf
setenv RUNBASE   /scratch2/NCEPDEV/stmp1/${USER}/prototype_evaluations/${expt}.verf

#Gaea
setenv USER $LOGNAME
setenv PATH /ncrc/home1/Robert.Grumbine/anaconda3/bin:$PATH
setenv XDG_RUNTIME_DIR /ncrc/home1/${USER}/scratch/runtime
setenv MPLCONFIGDIR    /ncrc/home1/${USER}/scratch/runtime

module load intel
module load cray-netcdf
module load wgrib2
setenv mmablib /ncrc/home1/Robert.Grumbine/rgdev/CICE/mmablib/

setenv expt gaea_intel_smoke_gx1_8x1_gx1_run_std.pstar1
setenv FCST_BASE /ncrc/home1/${USER}/scratch/CICE_RUNS/${expt}/history/
setenv RUNBASE   /ncrc/home1/${USER}/scratch/${USER}/evaluations/${expt}.verf
setenv EXDIR     /ncrc/home1/${USER}/rgdev/evaluations/

setenv dirtag pstar

#All systems ----------------------------------------------------------------
module list

if ( ! -d $FCST_BASE ) then
  echo No forecast directory to evaluate! -- dir $FCST_BASE not present
  exit 1
endif
if ( ! -d $RUNBASE ) then
  mkdir -p -m 700 $RUNBASE
endif
if ( ! -d $EXDIR ) then
  mkdir -p -m 700 $EXDIR
endif
cd     $EXDIR
setenv base `pwd`


echo env $FCST_BASE $EXDIR $base $RUNBASE

# Fewer changes below here -------------------------------------------------

#For batch python graphics
if ( ! -d $XDG_RUNTIME_DIR ) then
  mkdir -p -m 700 $XDG_RUNTIME_DIR
endif
echo $XDG_RUNTIME_DIR for python graphic support

setenv x `date`
echo start of loop at dtime $x


setenv initial 20050101
setenv yy `echo $initial | cut -c1-4`
setenv mm `echo $initial | cut -c5-6`
setenv dd `echo $initial | cut -c7-8`

setenv RUNDIR ${RUNBASE}/$yy
echo RUNDIR = $RUNDIR
if !( -d $RUNDIR ) then
  mkdir -p $RUNDIR
endif

cd $RUNDIR
if !( $? == 0 ) then
  echo could not move to rundir $RUNDIR
  exit 1
endif

setenv tag ${yy}${mm}${dd}
setenv dashtag ${yy}-${mm}-${dd}
setenv OUT $base/out.$initial.$dirtag
if ( ! -d $OUT ) then
  mkdir $OUT
endif

setenv fcst_len 364
#dirname
#if ( -d ${FCST_BASE}/${initial}/6hrly ) then
if ( -d ${FCST_BASE}/ ) then
  echo assessing experiment from $initial
  setenv i 0
  while ( $i < $fcst_len )
    setenv tag `expr $tag + 1`
    setenv tag `$mmablib/ush/dtgfix3 $tag`
    setenv i   `expr $i + 1`
    echo forecast lead $i
    # -m cProfile -o pystats.$tag.$i to generate profiling 
    #   stats for later analysis. Optional
#dirname
    echo python3  $EXDIR/setup_verf_ice.py $initial $tag ${FCST_BASE}/ 
    python3  $EXDIR/setup_verf_ice.py $initial $tag ${FCST_BASE}/ 
    if ( -f fcst_edge.$tag ) then
      mv fcst_edge.$tag          $OUT
      mv edge.fcst.*.*.$tag      $OUT
    endif
  end
  mv $expt.$initial.*.out $OUT

# Per-forecast statistics, graphics
  time python3 $EXDIR/contingency_plots.py $fcst_len $initial 0.15 $expt 
  mv *${initial}.png                $OUT
  mv score*${initial}.csv           $OUT
else
  echo no experiment output for $initial yet
endif


setenv x `date`
echo end of $expt forecast verification at $x
