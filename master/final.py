import sys
import os
import datetime
import csv

from math import *
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg') #for batch mode

lead = 35
fcsts = 24

d1='p3.1.figs/'
d2='p5.0.figs/'
d3='p6.0.figs/'
d4='persistence.figs/'

leads = np.zeros((lead))
mean1 = np.zeros((lead))
mean2 = np.zeros((lead))
mean3 = np.zeros((lead))
mean4 = np.zeros((lead))
rms1 = np.zeros((lead))
rms2 = np.zeros((lead))
rms3 = np.zeros((lead))
rms4 = np.zeros((lead))
var1 = np.zeros((lead))
var2 = np.zeros((lead))
var3 = np.zeros((lead))
var4 = np.zeros((lead))

ndates = 0
dates = []
dt = datetime.timedelta(1)
all1 = np.zeros((lead*fcsts))
all2 = np.zeros((lead*fcsts))
all3 = np.zeros((lead*fcsts))
all4 = np.zeros((lead*fcsts))
n1 = int(0)
n2 = int(0)
n3 = int(0)
n4 = int(0)

allfig,allax = plt.subplots()
allax.set(xlabel = "Date", ylabel = "threat score [0:1]")
allax.set(title = "Northern Hemisphere Threat Scores")
print("data ratio: ",allax.get_data_ratio() )
#allax.set_aspect(aspect=0.5/allax.get_data_ratio() )


for mm in range (1,13):
  for dd in ('01', '15'):
      yy = 2018

      start_date = datetime.date(int(yy), int(mm), int(dd))
      tag = start_date.strftime("%Y%m%d")
      print(start_date, tag)

      f1 = d1 + "/summary_"+start_date.strftime("%Y%m%d") + ".csv" 
      f2 = d2 + "/summary_"+start_date.strftime("%Y%m%d") + ".csv" 
      f3 = d3 + "/summary_"+start_date.strftime("%Y%m%d") + ".csv" 
      f4 = d4 + "/summary_"+start_date.strftime("%Y%m%d") + ".csv" 
      #if (os.path.exists(f1) and os.path.exists(f2) and os.path.exists(f3) and os.path.exists(f4) ):
      if (os.path.exists(f1) and os.path.exists(f3) ):
        s1read = csv.reader(open(f1))
        s2read = csv.reader(open(f2))
        s3read = csv.reader(open(f3))
        s4read = csv.reader(open(f4))

        #f1, sNread, lead, meanN, rmsN, varN
        if (os.path.exists(f1)):
          with (open(f1)) as csvfile:
            s1read = csv.reader(csvfile, delimiter = ',')
            k = -1 
            for line in s1read:
             if (k == -1):
               k += 1
               continue
             #print("k = ",k)
             #print("line0 = ",line[0])
             #print("line = ",line)
             leads[k]  = float(line[0])
             mean1[int(k)] = float(line[1])
             rms1[int(k)]  = float(line[2])
             var1[int(k)]  = float(line[3]) 
             if (start_date == datetime.date(int(2018), int(1), int(1))):
               dates.append(start_date + k*dt)
             else:
               dates[k] = start_date + k*dt
             print("ndates, date ",ndates, start_date, (start_date + k*dt),dates[k] )
             all1[n1] = mean1[int(k)]
             n1 += 1
             ndates += 1
             k += 1
        if (os.path.exists(f2)):
          with (open(f2)) as csvfile:
            s2read = csv.reader(csvfile, delimiter = ',')
            k = -1
            for line in s2read:
             if (k == -1):
               k += 1
               continue
             mean2[int(k)] = float(line[1])
             all2[n2] = mean2[int(k)]
             rms2[int(k)]  = float(line[2])
             var2[int(k)]  = float(line[3]) 
             n2 += 1
             k += 1
        if (os.path.exists(f3)):
          with (open(f3)) as csvfile:
            s3read = csv.reader(csvfile, delimiter = ',')
            k = -1
            for line in s3read:
             if (k == -1):
               k += 1
               continue
             mean3[int(k)] = float(line[1])
             all3[n3] = mean3[int(k)]
             rms3[int(k)]  = float(line[2])
             var3[int(k)]  = float(line[3]) 
             n3 += 1
             k += 1
        if (os.path.exists(f4)):
          with (open(f4)) as csvfile:
            s4read = csv.reader(csvfile, delimiter = ',')
            k = -1
            for line in s4read:
             if (k == -1):
               k += 1
               continue
             mean4[int(k)] = float(line[1])
             all4[n4] = mean4[int(k)]
             rms4[int(k)]  = float(line[2])
             var4[int(k)]  = float(line[3]) 
             n4 += 1
             k += 1

      else:
        #print("missing a file ",f1, f2, f3, f4)
        print("missing a file ",f1, f3)
        continue

      #Now ready to plot the given forecast:
      fig,ax = plt.subplots()
      ax.set(xlabel = "Forecast lead, days", ylabel = "threat score [0:1]")
      ax.set(title = "Northern Hemisphere Threat Scores")
      plt.ylim(0.65,0.95)

      ax.plot(leads, mean1, color="red", label = "UFS_p3.1")
      ax.plot(leads, mean2, color="blue", label = "UFS_p5.0")
      ax.plot(leads, mean3, color="green", label = "UFS_p6.0")
      ax.plot(leads, mean4, color="black", label = "Persistence")

      if (dd == "01"):
        linestyle = "solid"
      else:
        linestyle = "dashed"

      if (start_date == datetime.date(int(2018), int(1), int(1))):
        allax.plot(dates, mean1, linestyle=linestyle, color="red", label = "UFS_p3.1")
        allax.plot(dates, mean2, linestyle=linestyle, color="blue", label = "UFS_p5.0")
        allax.plot(dates, mean3, linestyle=linestyle, color="green", label = "UFS_p6.0")
        allax.plot(dates, mean4, linestyle=linestyle, color="black", label = "Persistence")
      else:
        allax.plot(dates, mean1, linestyle=linestyle, color="red")
        allax.plot(dates, mean2, linestyle=linestyle, color="blue")
        allax.plot(dates, mean3, linestyle=linestyle, color="green")
        allax.plot(dates, mean4, linestyle=linestyle, color="black")

      ax.legend()
      ax.grid()
      plt.savefig("all_"+tag+".png")
      plt.close()

# Now finish plotting a grand summary figure:
allax.legend()
allax.grid()
allfig.savefig("grand_"+tag+".png")
plt.close()
