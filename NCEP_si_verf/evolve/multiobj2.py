''' multiobj2 -- second try at functions for multi-objective analysis '''

#--------------------------------------------
def known(sname, scandidates):
  ''' known(name, candidates) -- true if name is in the candidate list '''
  result = False
  for si in range(0,len(scandidates)):
    if (sname == scandidates[si][0]):
      result = True
      return result
  return result

def dominated(sitem, scandidates):
  ''' dominated(item, candidates) -- true if item is better than all candidates '''
  dom = False
  for si in range(0, len(scandidates)):
    if (sitem[1] > scandidates[si][1] and (sitem[2] > scandidates[si][2])):
      dom = True
  return (dom)

def is_nondom(sitem, scandidates):
  ''' is_nondom(item, candidates) '''
  nondom1 = False
  nondom2 = False
  for si in range(0, len(scandidates)):
    if (sitem[1] <= scandidates[si][1]):
      nondom1 = True
      return True
    if (sitem[2] <= scandidates[si][2]):
      nondom2 = True
      return True
  return (nondom1 or nondom2)

# -- versions for multimetric --------
def dominates(ref, cand):
    ''' dominates(ref, candidate) -- true if reference dominates candidate '''
    return ref > cand
def dominated_by(ref, cand):
    ''' dominated_by(ref, cadidate) -- true if candidate dominates candidate '''
    return ref < cand
def nondom(ref, cand):
    ''' nondom(ref, cand) -- true if reference neither dominates nor is dominated by candidate '''
    return not dominates(ref, cand) and not dominated_by(ref, cand)

#return # of metrics candidate is better than the reference on.
def ncheck(ref, cand):
    ''' ncheck(ref, cand): Returns number of metrics that reference is 
           better than the candidate on '''
    fnbetter = 0
    for sk in range (0, len(cand[1])):
        if (cand[1][sk] < ref[1][sk]):
            fnbetter += 1
    return fnbetter
#--------------------------------------------
