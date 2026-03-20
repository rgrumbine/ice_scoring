import sys
import os
import csv
import copy

import numpy

from multiobj import *
#----------------------------------------------------

nstat = 9
ncand = 1200

stat = numpy.zeros((ncand,nstat))
exptno = numpy.zeros((ncand))

#------  read in and transform (mean errors = abs(mean error)) 
fin = open(sys.argv[1], "r")
k = 0
makeabs = [0,3,6]
for line in fin:
  words = line.split()
  exptno[k] = int(words[0])
  for i in range (0,nstat):
    if (i in makeabs):
      stat[k,i] = abs(float(words[i+1]))
      #debug: print(i,k,stat[k,i], flush=True)
    else:
      stat[k,i] = float(words[i+1])

  k += 1
nexpt = k

best = numpy.zeros((nstat))
for i in range (0,nstat):
  best[i] = numpy.min(stat[0:nexpt,i])
  print('best val for stat #',i, best[i])

# ----- append candidates --------------------------------------
candidates = []
k = 0
pset = [exptno[k], stat[k]]
candidates.append(pset)
#debug: print(pset)
#debug: print(candidates)
#debug: print(candidates[k][1])
#debug: print(candidates[k][1][5])

dominated = numpy.zeros((nexpt),dtype='bool')
nparam = len(pset[1])
#debug: print("original pset: ",pset, dominated[k], flush=True)
best_expt = pset[0]

newbest = False
for k in range(1,nexpt):
  if (exptno[k] == int(best_expt) ):
      #debug: print("0 skipping ",k,flush=True)
      continue
  pset2 = [exptno[k],stat[k]]
  #debug: print(k, check(pset, pset2))
  nbetter =  check(pset, pset2)
  if (nbetter == 0):
    dominated[k] = True
  elif (nbetter < nparam):
    dominated[k] = False
    candidates.append(pset2)
  elif (nbetter == nparam):
    dominated[k] = False
    pset = copy.deepcopy(pset2)
    best_expt = pset[0]
    newbest = True
    #debug: print("new best ",pset)
    # recursive check? of everything up to previous -- looking for dominated sets
    #domchck(candidates, ref, 1:best_expt
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
    pset2 = [exptno[k],stat[k]]
    #debug: print(k, check(pset, pset2))
    nbetter =  check(pset, pset2)
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
      best_expt = pset[0]
      newbest = True
      print("new best ",pset)
    else: 
      print("error -- should not be here", flush=True)
  passno += 1

#debug: print(len(candidates), "initial candidates", flush=True)
#debug: for k in range(0, nexpt):
#debug:   pset2 = [exptno[k],stat[k]]
#debug:   print(exptno[k], stat[k], check(pset,pset2),  dominated[k], flush=True)

#---------------------------------------------------------------
# Now have a set of candidates, one of which is guaranteed to be nondominated

finalset = []
finalset.append(pset)
nparm = len(pset[1])
ncands = len(candidates)
nf = 1
for k in range(0,ncands):
  newdom = False
  dominated = False
  #if any of candidates[k] dominate finalset[i] for any i, replace that dominated finalset
  for i in range(0, len(finalset)):
    #debug: print(i,k,len(finalset), len(candidates), flush=True )
    if (check(finalset[i], candidates[k]) == nparm):
      #debug: print("candidate ",k," dominates finalset member",i, flush=True)
      finalset[i] = copy.deepcopy(candidates[k])
      newdom = True
      break
  # if it is dominated by any in hand, ignore it:
  for i in range(0, len(finalset)):
    if (check(finalset[i], candidates[k]) == 0):
      #debug: print("candidate ",k, " is dominated by member ",i, flush=True)
      dominated = True
      break
  # if not dominant or dominated, add it to list:
  if (not newdom and not dominated):
    finalset.append(candidates[k])

print("length of the final set: ",len(finalset))
for k in range(0,len(finalset)):
  print(k, int(finalset[k][0]),  end="")
  for i in range(0, nparm):
    print(" ",finalset[k][1][i], end="")
  print("\n", end="")


 
