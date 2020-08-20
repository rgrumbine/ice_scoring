import sys
import os
import datetime
from math import *

import csv
import numpy as np
import matplotlib
#matplotlib.use('Agg') #for batch mode
#matplotlib.use('Qt5Agg') #for interactive mode
import matplotlib.pyplot as plt

lead = int(sys.argv[1])
idate = int(sys.argv[2])

(yy,mm,dd) = (int(int(idate)/10000), int(int(idate)%10000)/100, int(idate)%100)
start_date = datetime.date(int(yy), int(mm), int(dd))
dt = datetime.timedelta(1)

#For score vs. forecast lead through all leads, for a given critical level:
dates = []
xmajor = []
score = np.zeros((lead))
xtick_relative = np.zeros((lead))

valid_date = start_date
for i in range (0,lead):
  valid_date = valid_date + dt 
  dates.append(valid_date.strftime("%y%m%d") )
  score[i] = i
  xtick_relative[i] = float(i)/float(lead)
  if ((i%7) == 0):
    xmajor.append(valid_date.strftime("%y%m%d") )
  else:
    xmajor.append("")


#done with day by day, now plot summary vs. cutoff:
fig,ax = plt.subplots()
ax.set(xlabel = "Forecast verifying date", ylabel = 'threat score [0:1]')
ax.set(title = "Threat score for critical = "+" from "+start_date.strftime("%Y%m%d"))

plt.ylim(0,35)

#ax.tick_params(direction='out',labelrotation=90.)
ax.tick_params(labelrotation=315.)

#ax.minorticks_off()
ax.set_xticklabels(xmajor)

#print(ax.get_xticks(minor=False))
#ax.set_xticks(xtick_relative)
#print(xtick_relative)
#print(ax.get_xticks(minor=False))

ax.plot(dates,score)
ax.grid()
#fig.show()
plt.savefig("threat_f"+start_date.strftime("%Y%m%d")+".png")
plt.close()
