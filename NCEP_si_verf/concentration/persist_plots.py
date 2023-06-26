import sys
import os
import datetime
from math import *

import csv
import numpy as np
import matplotlib
matplotlib.use('Agg') #for batch mode
#matplotlib.use('Qt5Agg') #for interactive mode
import matplotlib.pyplot as plt

lead = int(sys.argv[1])
idate = int(sys.argv[2])
level_score = float(sys.argv[3]) #might be good to verify that this is integer multiple of 0.05


(yy,mm,dd) = (int(int(idate)/10000), int(int(idate)%10000)/100, int(idate)%100)
start_date = datetime.date(int(yy), int(mm), int(dd))
dt = datetime.timedelta(1)

#critical levels ...? all levels? hemisphere selection?
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

#For score vs. forecast lead through all leads, for a given critical level:
days = np.zeros((lead))
score = np.zeros((lead))

#For score vs. crit level for each lead
critical_level = np.zeros((20))
threat_index = np.zeros((20))
critical_level[0] = 0
threat_index[0] = 0

valid_date = start_date
for i in range (0,lead):
  valid_date = valid_date + dt 
  fname = ("score."+valid_date.strftime("%Y%m%d")+"f"+start_date.strftime("%Y%m%d")+".csv")
#score.20110126f20110101.csv

  flead = (valid_date - start_date).days
  if (not os.path.exists(fname)):
    print("missing ",valid_date.strftime("%Y%m%d"))
  else:    #at each forecast lead, plot the curve of threat vs. cutoff
    #print("can plot forcast lead ",flead," for ",valid_date.strftime("%Y%m%d"))
    with (open(fname)) as csvfile:
      sreader = csv.reader(csvfile, delimiter=',')
      k = -1
      days[i] = flead
      for line in sreader:
        k += 1
        #cd print("i,k,flead,level,threat ",i,k,flead,level,threat,line)
        #cd print(line[level], float(line[level]))
        #cd print(line[threat], float(line[threat]))

        critical_level[k] = float(line[level])
        threat_index[k] = float(line[threat])
        if (float(critical_level[k]) == level_score):
          score[i] = threat_index[k]
    #Now have this lead in hand, plot the curve:
    fig, ax = plt.subplots()
    ax.set(xlabel = "Cutoff Concentration", ylabel = 'threat score [0:1]')
    ax.set(title = 'Forecast lead '+str(flead)+' NH threat score')
    plt.ylim(0,1.0)
    ax.plot(critical_level, threat_index)
    ax.grid()
    #fig.show()
    plt.savefig("threat_"+str(flead)+"_dy_"+"from_"+start_date.strftime("%Y%m%d")+".png")
    plt.close()

#done with day by day, now plot summary vs. cutoff:
fig,ax = plt.subplots()
ax.set(xlabel = "Forecast lead, days", ylabel = 'threat score [0:1]')
ax.set(title = "Threat score for critical = "+str(level_score)+" from "+start_date.strftime("%Y%m%d"))
ax.plot(days,score)
ax.grid()
#fig.show()
plt.savefig("threat_"+str(level_score)+"_f"+start_date.strftime("%Y%m%d")+".png")
plt.close()
