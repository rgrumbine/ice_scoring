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
title_base = sys.argv[4]
ptag = "ps"


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
iiee = 12

param = threat
label = "threat"

#For score vs. forecast lead through all leads, for a given critical level:
days = np.zeros((lead))
score = np.zeros((lead))

#For score vs. crit level for each lead
critical_level = np.zeros((20))
threat_index = np.zeros((20))

valid_date = start_date
for i in range (1,lead):
  valid_date = start_date + i*dt 
  fname = ("score."+ptag+"."+valid_date.strftime("%Y%m%d")+"f"+start_date.strftime("%Y%m%d")+".csv")
  print(fname,flush=True)
  flead = (valid_date - start_date).days
  if (not os.path.exists(fname)):
    print("contingency plot missing ",valid_date.strftime("%Y%m%d"), fname, flush=True)
  else:    #at each forecast lead, plot the curve of threat vs. cutoff
    #print("can plot forcast lead ",flead," for ",valid_date.strftime("%Y%m%d"))
    with (open(fname)) as csvfile:
      sreader = csv.reader(csvfile, delimiter=',')
      k = -1
      days[i] = flead
      for line in sreader:
        k += 1
        #print("k = ",k,line)
        critical_level[k] = float(line[level])
        threat_index[k] = float(line[param])
        if (float(critical_level[k]) == level_score):
          score[i] = threat_index[k]
    #Now have this lead in hand, plot the curve:
    fig, ax = plt.subplots()
    #ax.set(xlabel = "Critical Concentration", ylabel = 'threat score [0:1]')
    #ax.set(title = title_base + ' Forecast lead '+str(flead)+' days\nNH threat score')
    ax.set(xlabel = "Critical Concentration", ylabel = label)
    ax.set(title = title_base + ' Forecast lead '+str(flead)+' days\n'+label)
    plt.ylim(min(threat_index.min(),0.5),max(1.0,threat_index.max() ) )
    ax.plot(critical_level, threat_index)
    ax.grid()
    #fig.show()
    plt.savefig(label+"_"+str(flead)+"_dy_"+"from_"+start_date.strftime("%Y%m%d")+".png")
    plt.close()

#done with day by day, now plot summary vs. cutoff:
fig,ax = plt.subplots()
ax.set(xlabel = "Forecast lead, days", ylabel = label)
ax.set(title = title_base + " score for critical = "+str(level_score)+" \nfrom "+start_date.strftime("%Y%m%d"))
ax.plot(days[1:lead],score[1:lead])
ax.grid()
#fig.show()
plt.savefig(label+"_"+str(level_score)+"_f"+start_date.strftime("%Y%m%d")+".png")
plt.close()
