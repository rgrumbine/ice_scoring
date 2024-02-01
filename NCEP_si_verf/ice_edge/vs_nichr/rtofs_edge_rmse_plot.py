import os
import sys
import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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
    #n.1.202301010.15:rms  46.59 with  3844 matchups
    tag = (words[0][-16:-8])
    #debug print(tag, flush=True)
    x = datetime.datetime.strptime(tag,"%Y%m%d").date()
    #debug: print(k, x, flush=True)
    if (float(words[3]) > 2000):
      rms.append(float(words[1]))
      nmatch.append(float(words[3]))
      index.append(x)
      k += 1

mean = np.average(rms)
std  = np.std(rms)
print(lead," day lead mean, std",np.average(rms), np.std(rms) )

matplotlib.use('Agg')
fig,ax = plt.subplots()
ax.set(xlabel="Date", ylabel="rmse km") 
ax.set(title = label+" rtofs ice edge vs nichr rmse (km) at "+"{:d}".format(lead)+" day lead")
ax.plot(index, rms)
ax.grid()
fig.savefig("edge_rmse_"+label+"{:d}".format(lead)+".png")
plt.close()

#nic_v_nic.5/score.n.2019077:rms  50.62 with 14805 matchups
#nic_v_nic.5/score.n.2019079:rms  46.85 with 14860 matchups
