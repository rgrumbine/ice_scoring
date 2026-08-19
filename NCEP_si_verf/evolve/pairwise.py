''' pairwise checks for dominant and non-dominated solutions given a pair of metrics '''

import sys
import copy

import numpy

from multiobj2 import *

#----------------------------------------------------

nstat = 2
ncand = 1200 #some large number

stat = numpy.zeros((ncand,nstat))
exptno = numpy.zeros((ncand))
generation = []

#------  read in and transform
fin = open(sys.argv[1], "r", encoding='utf-8')
nh = float(sys.argv[2])
sh = float(sys.argv[3])

k = 0
use = [4,7]
for line in fin:
  words = line.split()
  #print(words[0],flush=True)
  expt = words[0].split(':')
  if ('g' in expt[0]):
    d2 = expt[0].split('/')
    #debug: print(d2)
    generation.append(d2[0][3:])
    exptno[k] = int(d2[1][4:])
  else:
    generation.append(0)
    exptno[k] = int(expt[0][4:])
  #debug: print(generation[k], exptno[k], words[0], words[4], words[7])
  stat[k,0] = abs(float(words[4])-nh)
  stat[k,1] = abs(float(words[7])-sh)
  k += 1
fin.close()
nexpt = k

# Diagnostic/informational only. Does not affect candidate selection.
best = numpy.zeros((nstat))
for i in range (0,nstat):
  best[i] = numpy.min(stat[0:nexpt,i])
  print('best val for stat #',i, best[i])

#debug: exit(0)
# ----- append candidates --------------------------------------
candidates = []
k = 0
pset = [exptno[k], stat[k], generation[k]]
candidates.append(pset)
#debug: print(pset)
#debug: print(candidates)
#debug: print(candidates[k][1])
#debug: print(candidates[k][1][5])

undominant = numpy.zeros((nexpt),dtype='bool')
nparam = len(pset[1])
#debug: print("original pset: ",pset, undominant[k], flush=True)
best_expt = pset[0]

newbest = False
for k in range(1,nexpt):
  if (exptno[k] == (best_expt) ):
      continue
  pset2 = [exptno[k],stat[k],generation[k]]
  #debug: print(k, ncheck(pset, pset2))
  nbetter =  ncheck(pset, pset2)
  if (nbetter == 0):
    undominant[k] = True
  elif (nbetter < nparam):
    undominant[k] = False
    candidates.append(pset2)
  elif (nbetter == nparam):
    undominant[k] = False
    pset = copy.deepcopy(pset2)
    best_expt = pset[0]
    newbest = True
    #debug: print("new best ",pset)
    # recursive check? of everything up to previous -- looking for undominant sets
    #domchck(candidates, ref, 1:best_expt
  else:
    print("error -- should not be here", flush=True)

#debug: exit(0)

passno = 1
if (newbest and passno < 10):
  del candidates
  candidates = []
  candidates.append(pset)
  #debug: print(passno, "Found a new best (dominating previous reference) set", flush=True)
  newbest = False
  for k in range(1,nexpt):
    if ((exptno[k]) == (best_expt) ):
        #debug: print("1 skipping ",k,flush=True)
        continue
    pset2 = [exptno[k],stat[k],generation[k]]
    #debug: print(passno, k, ncheck(pset, pset2))
    nbetter =  ncheck(pset, pset2)
    if (nbetter == 0):
      undominant[k] = True
    elif (nbetter < nparam):
      undominant[k] = False
      candidates.append(pset2)
    elif (nbetter == nparam):
      # RG: work out k for [0,120] -- actual expt no, vs [0,nexpt] -- nonfatal expts
      # to_debug: undominant[pset[0]] = True
      undominant[k] = False
      pset = copy.deepcopy(pset2)
      best_expt = pset[0]
      newbest = True
      #debug: print("new best ",pset)
    else:
      print("error -- should not be here", flush=True)
  passno += 1

#debug: print(len(candidates), "initial candidates", flush=True)
#debug: for k in range(0, nexpt):
#debug:   pset2 = [exptno[k],stat[k]]
#debug:   print(exptno[k], stat[k], ncheck(pset,pset2),  undominant[k], flush=True)

#---------------------------------------------------------------
# Now have a set of candidates, one of which is guaranteed to be undominant

finalset = []
finalset.append(pset)
nparm = len(pset[1])
ncands = len(candidates)
nf = 1
for k in range(0,ncands):
  newdom = False
  drop   = False
  #if any of candidates[k] dominate finalset[i] for any i, replace that undominant finalset
  for i in range(0, len(finalset)):
    #debug: print(i,k,len(finalset), len(candidates), flush=True )
    if (ncheck(finalset[i], candidates[k]) == nparm):
      #debug: print("candidate ",k," dominates finalset member",i, flush=True)
      finalset[i] = copy.deepcopy(candidates[k])
      newdom = True
      break
  # if it is dominated by any in hand, ignore it:
  for i in range(0, len(finalset)):
    if (ncheck(finalset[i], candidates[k]) == 0):
      #debug: print("candidate ",k, " is dominated by member ",i, flush=True)
      drop = True
      break
  # if not dominant or dominated, add it to list:
  if (not newdom and not drop):
    finalset.append(candidates[k])

print("length of the final set: ",len(finalset))
for k in range(0,len(finalset)):
  #print("{:2d}".format(k), finalset[k][2],' ',  end="")
  #print("{:3d}".format(int(finalset[k][0])),  end="")
  #for i in range(0, nparm):
  #  print(" ","{:.3f}".format(finalset[k][1][i]), end="")
  print(f"{k:2d}", finalset[k][2],' ',  end="")
  print(f"{int(finalset[k][0]):3d}",  end="")
  for i in range(0, nparm):
    print(" ",f"{finalset[k][1][i]:6.3f}", end="")
  print("\n", end="")
