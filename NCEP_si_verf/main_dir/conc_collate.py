import sys
import os

import datetime
import csv

from math import *
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg') #for batch mode

#dirbase='bm3.verf/out.'
dirbase = sys.argv[1]
figtitle = sys.argv[2]
crit     = float(sys.argv[3])
ncrit = int(0.5 + crit / 0.05)
dt = datetime.timedelta(1)

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
iiee = 12 #m^2, divide by 1e12 for millions of km^2

param = threat
label = "threat"

ptag="ps"
lead = 16
tag = datetime.datetime(2024,12,10)
end = datetime.datetime(2025,1,6)

counts = np.zeros((20,lead))
sums   = np.zeros((20,lead))
sumsq  = np.zeros((20,lead))
while (tag <= end):

    start_date = tag
    dirname = dirbase 
    if (os.path.exists(dirname)):
        for flead in range (int(0),int(lead)):
          valid_date = start_date + (flead+1)*dt
          fname = dirname + "/score."+ptag+"."+valid_date.strftime("%Y%m%d") + "f" + start_date.strftime("%Y%m%d") + ".csv" 
          #debug: print(str(flead)+" "+ fname, flush=True)
          if (os.path.exists(fname)):
            with (open(fname)) as csvfile:
              sreader = csv.reader(csvfile, delimiter = ',')
              k = -1
              for line in sreader:
                k += 1
                counts[int(k), flead] += 1
                sums[int(k), flead]   += float(line[param])
                sumsq[int(k), flead]  += float(line[param])*float(line[param])
          #except: (nothing, move on to next)

    else:
      print("no directory ",dirname)

    tag += dt

if (param == iiee):
    sums /= 1e12
    sumsq /= 1e24

print("done_"+tag.strftime("%Y%m%d"),counts.max(), flush=True )
sums  /= counts
sumsq /= counts
days = np.zeros((lead))
mean = np.zeros((lead))
rmse = np.zeros((lead))
var = np.zeros((lead))
with (open(ptag+label+'_summary_'+tag.strftime("%Y%m%d")+'.csv', 'w', newline='') ) as csvfile:
  fieldnames = ['lead', label, 'rms', 'var'];
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()

  for i in range (0,lead):
    days[i] = i+1
    mean[i] = sums[ncrit,i]
    rmse[i] = sqrt(sumsq[ncrit,i])
    var[i]  = sqrt(sumsq[ncrit,i]-sums[ncrit,i]*sums[ncrit,i])
    print("{:4.2f}".format(crit),"{0:5.3f}".format(sums[ncrit,i]), " ","{0:5.3f}".format(sqrt(sumsq[ncrit,i])), " ", "{0:6.4f}".format(sqrt(sumsq[ncrit,i]-sums[ncrit,i]*sums[ncrit,i]))  )
    writer.writerow({'lead': days[i], label : mean[i], 'rms': rmse[i], 'var':var[i]})


#Now ready to plot:
fig,ax = plt.subplots()
#ax.set(xlabel = "Forecast lead, days", ylabel = "threat score [0:1]")
ax.set(xlabel = "Forecast lead, days", ylabel = label)
ax.set(title = figtitle +" Summary for "+tag.strftime("%Y%m%d")+" critical level = "+"{:4.2f}".format(crit))
plt.ylim(min(0.5,mean.min()),max(1.0,mean.max() ))
ax.plot(days, mean, color="blue", label = label)
#ax.plot(days, rmse, color="green", label = "rms")
ax.legend()
ax.grid()
plt.savefig(ptag+label+"_"+tag.strftime("%Y%m%d")+".png")
plt.close()

fig,ax = plt.subplots()
ax.set(xlabel = "Forecast lead, days", ylabel = "sqrt(variance) [0:1]")
ax.set(title = figtitle + " Summary for "+tag.strftime("%Y%m%d")+" critical level = "+"{:4.2f}".format(crit))
plt.ylim(0,0.075)
ax.plot(days, var, color="blue", label = "sqrt(variance)")
ax.legend()
ax.grid()
plt.savefig(ptag+label+"_var_"+tag.strftime("%Y%m%d")+".png")
plt.close()
