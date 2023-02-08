#!/bin/sh

  export FIXDIR=~/rgdev/fix
  export EXDIR=~/rgdev/ice_scoring/exec
  . ~/rgdev/toolbox/python_load.wcoss2 
  export PYTHONPATH=~/rgdev/mmablib/py
  time python3 ./rtofs.py
