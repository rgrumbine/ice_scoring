import sys
import os

import datetime
import csv

from math import *
import numpy as np

import matplotlib
import matplotlib.pyplot as plt


#-------------------------------------------------------------
#define the indices to the contingency table .csv lines:
region = 0
level = 1
a11 = 2
a12 = 3
a21 = 4
a22 = 5
pod = 6
far = 7
fcr = 8
correct = 9
threat = 10
bias = 11 #area over crit in model vs. in obs

#open up each of the 'lead' verification files and extract the  
def nhreader(lead, start_date, fbase, critical, metric, scores):
    fname = fbase + "/summary_"+ start_date.strftime("%Y%m%d") + ".csv" 
    if (os.path.exists(fname)):
      with (open(fname)) as csvfile:
        sreader = csv.reader(csvfile, delimiter = ',')
        k = 0
        for line in sreader:
          if (k == 0) :
            k += 1
          else:
            scores[k-1] = float(line[1])
            k += 1
    else:
      print("could not open ",fname)

#-------------------------------------------------------------


matplotlib.use('Agg') #for batch mode

#splice together multiple fcsts for/from a given date -- 
# argv[1] = date, 2-N = paths
basedate = sys.argv[1]

lead = 35
dt = datetime.timedelta(1)

#date from 8:
yy = int(int(basedate) / 10000)
mm = int(int(basedate) / 100) % 100
dd = int(basedate) % 100
start_date = datetime.date(int(yy), int(mm), int(dd))
print(basedate, yy, mm, dd, start_date)

score1 = np.zeros((lead))
score2 = np.zeros((lead))
score3 = np.zeros((lead))
score4 = np.zeros((lead))

days = range(1,lead+1)
print(days)


fname1 = sys.argv[2]
fname2 = sys.argv[3]
fname3 = sys.argv[4]
nhreader(lead, start_date, fname1, 0.15, threat, score1)
nhreader(lead, start_date, fname2, 0.15, threat, score2)
nhreader(lead, start_date, fname3, 0.15, threat, score3)
print(score1)
print(score2)
print(score3)

fname4 = sys.argv[5]
nhreader(lead, start_date, fname4, 0.15, threat, score4)
print(score4)

#Now ready to plot:
upper = 1.0
lower = 0.60
fig,ax = plt.subplots()
ax.set(xlabel = "Forecast lead, days", ylabel = "threat score [0:1]")
ax.set(title = "Splice for "+basedate+" critical level = 0.15 vs. NSIDC CDR")
plt.ylim(lower, upper)
ax.plot(days, score1, color="red", label = "p3.1")
ax.plot(days, score2, color="blue", label = "p5.0")
ax.plot(days, score3, color="green", label = "p6.0")
ax.plot(days, score4, color="black", label = "persistence")
ax.legend()
ax.grid()
plt.savefig("splice_"+basedate+".png")
plt.close()

