#!/bin/sh
# Robert Grumbine
# 8 June 2018
# mirror the iabp 'C' files

wget  -np -r -N -l 2 --no-remove-listing  ftp://iabp.apl.washington.edu/pub/IABP/C/
