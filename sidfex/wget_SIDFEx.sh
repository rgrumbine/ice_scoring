#!/bin/sh

wget -r -l1 --no-parent -A.dat http://iabp.apl.washington.edu/WebData/

mv iabp.apl.washington.edu/WebData/*.dat sidfex
