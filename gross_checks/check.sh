. $HOME/rgdev/toolbox/misc/python_load.wcoss2

export GDIR=$HOME/rgdev/ice_scoring/gross_checks/

export PYTHONPATH=$PYTHONPATH:$GDIR/shared
ln -sf $GDIR/curves curves

#after check has been done
python3 $GDIR/graphics/plot_errs.py all all 1.

python3 $GDIR/exceptions/exceptions.py $GDIR/exceptions/physical.exceptions all > nonphysical
python3 $GDIR/graphics/plot_errs.py nonphysical nonphysical 1.

python3 $GDIR/exceptions/exceptions.py $GDIR/exceptions/known.errors nonphysical > unknown
python3 $GDIR/graphics/plot_errs.py unknown unknown 1.
