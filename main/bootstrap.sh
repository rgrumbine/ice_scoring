#!/bin/sh

#Bootstrap for ice model verification -- retrieve the scripts and fixed files for a basic run of the system
#Robert Grumbine
# 25 February 2020

#hera export BASE=${BASE:-/home/Robert.Grumbine/rgdev/ice_scoring/}
if [ -z $BASE ] ; then
  echo WCOSS: BASE= /u/Robert.Grumbine/rgdev/
  echo Hera:  BASE= /home/Robert.Grumbine/rgdev/
  echo Orion: BASE= /u/rgrumbin/rgdev/
  echo Gaea:  BASE= /ncrc/home1/Robert.Grumbine/rgdev/
  echo Select one of these
  echo "  "
fi
export BASE=${BASE:-$HOME/rgdev/ice_scoring/}
echo BASE = $BASE

#Check the python environment -- assumes that path already references an appropriate interpreter 
python3 ${BASE}/main/checkenv.py
if [ $? -ne 0 ] ; then
  echo you are missing necessary elements of the python environment.
  echo please install the needed modules and retry
  echo "    " If on hera, use a recent anaconda distribution, such as obtained by
  echo "    "   module use -a /contrib/anaconda/modulefiles
  echo "    "   module load anaconda/latest
  exit 1
fi

#Check the directory / data environment for needed directories
export EXDIR=`pwd`
python3 ${BASE}/main/platforms.py trial
if [ $? -ne 0 ] ; then
  echo you need to correct the machines list and directory references in platforms.py
  exit 1
fi

#Start copying elements over to carry out the evaluation
for f in contingency_plots.py runtime.def 
do
  cp -p ${BASE}/concentration/$f .
  if [ ! -f $f ] ; then
    echo could not find $f in $BASE, exiting
    exit 1
  fi
done

for f in README verf_files.py setup_verf_ice.py platforms.py all.csh year.csh
do
  cp -p ${BASE}/main/$f .
  if [ ! -f $f ] ; then
    echo could not find $f in $BASE, exiting
    exit 1
  fi
done

#create and populate the exec directory if needed:
if [ ! -d ${BASE}/exec ] ; then
  cd ${BASE}
  ./makeall.sh
  if [ $? -eq 0 ] ; then
    echo copy exec dir from $BASE
    cp -rp ${BASE}/exec $EXDIR
  else
    echo failed to find or create execs, exiting now
    exit 2
  fi
else
  echo exec directory does exist in ${BASE}/exec
fi

cd $EXDIR
for d in exec 
do
  cp -rp ${BASE}/$d .
  if [ $? -ne 0 ] ; then
    echo error trying to copy $d from $BASE
    exit 4
  fi
  if [ ! -d $d ] ; then
    echo could not find directory $d in $BASE, exiting
    exit 4
  fi
done
if [ -d exec ] ; then
  cp -p runtime.def exec
fi


# tries to create fix directory link, but doesn't try hard
cd $EXDIR
if [ ! -d ${BASE}/fix ] ; then
  echo You must manually create the fix directory
  echo WCOSS: ln -sf /u/Robert.Grumbine/rgdev/fix .
  echo Hera:  ln -sf /home/Robert.Grumbine/rgdev/fix .
  echo Orion: ln -sf /u/rgrumbin/rgdev/fix .
  echo Gaea:  ln -sf /ncrc/home1/Robert.Grumbine/rgdev/fix .
  exit 3
fi
ln -sf $BASE/../fix .

if [ $? -eq 0 ] ; then
  echo successfully created the evaluation directory and stocked it with control files,
  echo   executables, and reference fixed files
fi
