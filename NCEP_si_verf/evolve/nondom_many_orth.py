import sys
import os
import csv
import copy

import numpy

from multiobj import *

#----------------------------------------------------

nstat = 9
ncand = 1200

stat   = numpy.zeros((ncand,nstat))
exptno = numpy.zeros((ncand))
genno  = numpy.zeros((ncand))

#------  read in and transform (mean errors = abs(mean error)) 
# run on multiple input files:
k = 0
makeabs = [0,3,6]
ngen    = len(sys.argv)

for fno in range(1,len(sys.argv)):
  print(len(sys.argv), fno, sys.argv[fno], flush=True)
  fin = open(sys.argv[fno], "r")
  for line in fin:
    words = line.split()
    exptno[k] = int(words[1])
    genno[k]  = fno
    for i in range (0,nstat):
      if (i in makeabs):
        stat[k,i] = abs(float(words[i+2]))
      else:
        stat[k,i] = float(words[i+2])
  
    k += 1
  fin.close()

nexpt = k
print(nexpt,"experiments from ",len(sys.argv)-1,"generations")
best = numpy.zeros((nstat))
for i in range (0,nstat):
  best[i] = numpy.min(stat[0:nexpt,i])
  print('best val for stat #',i, best[i])

# ----- append candidates --------------------------------------
candidates = []
k = 0
dominated = numpy.zeros((nexpt),dtype='bool')
pset = [genno[k], exptno[k], stat[k]]
candidates.append(pset)

nparam = len(pset[2])
#debug: print("original pset: ",pset, dominated[k], flush=True)
best_expt = pset[1]

orthlist = [0, 4, 6]
newbest = False
for k in range(1,nexpt):
  if (exptno[k] == int(best_expt) ):
      #debug: print("0 skipping ",k,flush=True)
      continue
  pset2 = [genno[k], exptno[k],stat[k]]
  nbetter =  checklist(pset, pset2, orthlist)
  if (nbetter == 0):
    dominated[k] = True
  elif (nbetter < nparam):
    dominated[k] = False
    candidates.append(pset2)
  elif (nbetter == nparam):
    dominated[k] = False
    pset = copy.deepcopy(pset2)
    best_expt = pset[1]
    newbest = True
  else: 
    print("error -- should not be here", flush=True)

passno = 1
if (newbest and passno < 10):
  del candidates
  candidates = []
  candidates.append(pset)
  #debug: print(passno, "Found a new best (dominating previous reference) set", flush=True)
  newbest = False
  for k in range(1,nexpt):
    if (int(exptno[k]) == int(best_expt) ):
        #debug: print("1 skipping ",k,flush=True)
        continue
    pset2 = [genno[k], exptno[k],stat[k]]
    nbetter =  checklist(pset, pset2, orthlist)
    if (nbetter == 0):
      dominated[k] = True
    elif (nbetter < nparam):
      dominated[k] = False
      candidates.append(pset2)
    elif (nbetter == nparam):
      # RG: work out k for [0,120] -- actual expt no, vs [0,nexpt] -- nonfatal expts
      # to_debug: dominated[pset[0]] = True
      dominated[k] = False
      pset = copy.deepcopy(pset2)
      best_expt = pset[1]
      newbest = True
      print("new best ",pset)
    else: 
      print("error -- should not be here", flush=True)
  passno += 1

#---------------------------------------------------------------
# Now have a set of candidates, one of which is guaranteed to be nondominated

finalset = []
finalset.append(pset)
nparm = len(pset[2])
ncands = len(candidates)
nf = 1
for k in range(0,ncands):
  newdom = False
  dominated = False
  #if any of candidates[k] dominate finalset[i] for any i, replace that dominated finalset
  for i in range(0, len(finalset)):
    if (checklist(finalset[i], candidates[k], orthlist) == nparm):
      finalset[i] = copy.deepcopy(candidates[k])
      newdom = True
      break
  # if it is dominated by any in hand, ignore it:
  for i in range(0, len(finalset)):
    if (checklist(finalset[i], candidates[k], orthlist) == 0):
      dominated = True
      break
  # if not dominant or dominated, add it to list:
  if (not newdom and not dominated):
    finalset.append(candidates[k])

#--------------------------------------------------------------
bygen = numpy.zeros((ngen),dtype="int")
print("length of the final set: ",len(finalset))
for k in range(0,len(finalset)):
  bygen[int(finalset[k][0])] += 1
  print(k, int(finalset[k][0]), int(finalset[k][1]), end="")
  for i in range(0, nparm):
    print(" ",finalset[k][2][i], end="")
  print("\n", end="")

for k in range(0, ngen):
  print("generation ",k," contributed ",bygen[k],"members")

