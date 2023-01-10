import os
import sys
import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Plot the rmse of a set of matchups in file 'fin' for lead time 'lead' 
#    adding a label 'label' to the title

fin = open(sys.argv[1],"r")
lead = int(sys.argv[2])
label = sys.argv[3]
rms = []
nmatch = []
index = []

k = 0
for line in fin:
    words = line.split() 
    #debug print(len(words),line,end="", flush=True)
    jd = (words[0][-11:-4])
    #debug print(jd, flush=True)
    x = datetime.datetime.strptime(jd,"%Y%j").date()
    #debug print(x, flush=True)
    if (float(words[3]) > 2000):
      rms.append(float(words[1]))
      nmatch.append(float(words[3]))
      #index.append(k)
      #index.append(jd-2019000)
      index.append(x)
      k += 1

mean = np.average(rms)
std  = np.std(rms)
print(lead," day lead mean, std",np.average(rms), np.std(rms) )

matplotlib.use('Agg')
fig,ax = plt.subplots()
ax.set(xlabel="Date", ylabel="rmse km") 
ax.set(title = label+" ice edge persistence rmse at "+"{:d}".format(lead)+" day lead")
ax.plot(index, rms)
ax.grid()
fig.savefig("edge_rmse_"+label+"{:d}".format(lead)+".png")
plt.close()
