# python packages used, or potentially used.
# More or less in increasing order of specialization 
# Robert Grumbine 29 August 2022

import os
import sys
from sys import version_info
import time
import calendar
import csv
import datetime
import glob
import importlib
import math
from math import *

# Not core python:
import matplotlib
import matplotlib.pyplot as plt

import numpy 
import numpy as np
import numpy.ma as ma

import scipy
import scipy.spatial.distance as spsd
import scipy.stats as sps

import netCDF4
from netCDF4 import Dataset

import pstats

from pkgutil import iter_modules

from geographiclib.geodesic import Geodesic

exit(0)

#my modules
from struct import *
from verf_files import *
import bounders
from platforms import *
