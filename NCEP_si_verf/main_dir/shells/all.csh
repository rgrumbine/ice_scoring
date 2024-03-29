#!/bin/csh 
#SBATCH -J hr1_all
#SBATCH -e hr1_all.err
#SBATCH -o hr1_all.out
#  #SBATCH -t 7:55:00
#SBATCH -t 0:25:00
#SBATCH -q batch
#SBATCH -A marine-cpu
#  #SBATCH -A fv3-cpu
#SBATCH -N 1
#SBATCH --mail-type FAIL
#SBATCH --mail-user USER@system

setenv USER $user
setenv expt hr1

#Orion
#  tbd
#WCOSS
#  tbd

#Hera:
source /etc/profile.d/modules.csh
module load intel/2022.1.2
module load impi/2022.1.2
module load netcdf/4.7.0
module load wgrib2/2.0.8

setenv mmablib /scratch1/NCEPDEV/climate/rgdev/mmablib/
#
module use -a /contrib/anaconda/modulefiles
module load anaconda/latest 
setenv XDG_RUNTIME_DIR /scratch1/NCEPDEV/climate/${USER}/runtime
setenv MPLCONFIGDIR    /scratch1/NCEPDEV/climate/${USER}/runtime

setenv EXDIR     /scratch1/NCEPDEV/climate/${USER}/clim_data/${expt}
setenv RUNBASE   /scratch1/NCEPDEV/stmp2/${USER}/${expt}

setenv FCST_BASE /scratch1/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_hr1/SeaIce/ 

##Gaea
#setenv USER $LOGNAME
#setenv PATH /ncrc/home1/Robert.Grumbine/anaconda3/bin:$PATH
#setenv XDG_RUNTIME_DIR /ncrc/home1/${USER}/scratch/runtime
#setenv MPLCONFIGDIR    /ncrc/home1/${USER}/scratch/runtime
#
#module load intel
#module load cray-netcdf
#module load wgrib2
#setenv mmablib /ncrc/home1/Robert.Grumbine/rgdev/CICE/mmablib/
#
#setenv expt gaea_intel_smoke_gx1_2x1_gx1_run_std.beta2
#setenv FCST_BASE /ncrc/home1/${USER}/scratch/CICE_RUNS/${expt}/history/
#setenv RUNBASE   /ncrc/home1/${USER}/scratch/${USER}/evaluations/${expt}
#setenv EXDIR     /ncrc/home1/${USER}/rgdev/evaluations/${expt}

#All systems:
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
setenv EXBASE $EXDIR


echo env $FCST_BASE $EXDIR $base $RUNBASE

# Fewer changes below here -------------------------------------------------

#For batch python graphics
if ( ! -d $XDG_RUNTIME_DIR ) then
  mkdir -p -m 700 $XDG_RUNTIME_DIR
endif
echo $XDG_RUNTIME_DIR for python graphic support


setenv x `date`
echo start of loop at dtime $x
setenv fcst_len 15
#setenv fcst_len 1

#For HR1:
#start 20191203
#every 3 days to 20200830
setenv PDY 20191203
setenv dt 3
setenv end 20200830

setenv yy `echo $PDY | cut -c1-4`
setenv mm `echo $PDY | cut -c5-6`
setenv dd `echo $PDY | cut -c7-8`

#foreach yy ( 2011 2012 2013 2014 2015 2016 2017 2018 )
  setenv RUNDIR ${RUNBASE}/$yy
  if ( ! -d $RUNDIR ) then
    mkdir -p $RUNDIR
  endif
  cd $RUNDIR
  if ( $? != 0 ) then
    echo could not move to rundir $RUNDIR
    exit 1
  endif

  #foreach mm ( 01 02 03 04 05 06 07 08 09 10 11 12 )
  #  foreach dd ( 01 15 )
      setenv tag     ${yy}${mm}${dd}
      setenv initial ${yy}${mm}${dd}
      setenv dashtag ${yy}-${mm}-${dd}
      setenv OUT $base/out.$initial
      if ( ! -d $OUT ) then
        mkdir $OUT
      #else
        #continue
        #exit 1
      endif

#dirname
      #if ( -d ${FCST_BASE}/${initial}/6hrly ) then
      if ( -d ${FCST_BASE}/${initial}/ ) then
        echo assessing experiment from $initial
        setenv i 0
        while ( $i < $fcst_len )
          setenv tag `expr $tag + 1`
          setenv tag `$mmablib/ush/dtgfix3 $tag`
          setenv i   `expr $i + 1`
          # -m cProfile -o pystats.$tag.$i to generate profiling 
          #   stats for later analysis. Optional
#dirname
          #python3  $EXDIR/setup_verf_ice.py $initial $tag ${FCST_BASE}/${initial}/6hrly/ >>& $expt.$initial.$tag.out
          python3  $EXDIR/setup_verf_ice.py $initial $tag ${FCST_BASE}/${initial}/ >>& $expt.$initial.$tag.out
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

#    end
#  end
#end

setenv x `date`
echo end of $expt forecast verification at $x
