import random
import re
T = 64
K = 40
cor = [(3,1), (1,2), (1,1), (1,5), (1,11), (3,15), (1,14), (1,8)]
#cor = [(2,3), (4,3), (3,3), (3,4), (2,6), (2,10), (5,11), (4,13), (5,14), (2,13), (4,14), (2,7), (2,9), (4,2), (5,2), (3,5), (3,11), (3,13), (4,13), (3,12), (3,8)]
#cor = [(6,1), (6,3), (6,7), (6,9), (6,11), (7,15), (8,15), (8,3), (8,9), (8,1), (8,7), (8,13), (5,3), (5,5), (5,7), (5,9), (5,15)]
#cor = [(6,2), (6,4), (6,6), (6,8), (6,12), (6,14), (7,2), (7,4), (7,6), (7,8), (7,10), (7,12), (7,14), (8,12), (8,8), (8,14), (8,2), (8,10), (8,4), (8,6), (5,2), (5,4), (5,6), (5,8), (5,10), (5,12)]
#(R, C, T, K) = (8,15,70,420)
f = "pcrmixtrue.sat"
for i in range(K):
  for (x,y) in cor:
  #y = random.randint(1,C)
    t = random.randint(1,T)
    p = 0
    s = "a_"+str(x)+"_"+str(y)+"_.*_"+str(t)+" = True"
    #s = "a_.*_"+str(x)+"_"+str(y)+"_"+str(t)+" = True"
    for line in open(f):
      line = line.rstrip()
      if re.search(s, line) :
        p = 1
  
    if p == 1 :
      print "    insertCheckpoint1X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)
    else:
      print "    insertCheckpoint0X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t) 



K = 30 
cor = [(2,1), (4,1), (1,3), (1,4), (1,6), (1,10), (1,12), (2,15), (4,15), (1,13), (1,15), (1,7), (1,9), (3,2), (2,2), (2,5), (2,11), (3,14), (2,14), (2,12), (2,8)]
#(R, C, T, K) = (8,15,70,420)
for i in range(K):
  for (x,y) in cor:
  #y = random.randint(1,C)
    t = random.randint(1,T)
    p = 0
    #s = "a_.*_"+str(x)+"_"+str(y)+"_"+str(t)+" = True"
    s = "a_"+str(x)+"_"+str(y)+"_.*_"+str(t)+" = True"
    for line in open(f):
      line = line.rstrip()
      if re.search(s, line) :
        p = 1

    if p == 1 :
      print "    insertCheckpoint1X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)
    else:
      print "    insertCheckpoint0X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)  

K = 30
cor = [(2,3), (4,3), (3,3), (3,4), (2,6), (2,10), (5,11), (4,13), (5,14), (2,13), (4,14), (2,7), (2,9), (4,2), (5,2), (3,5), (3,11), (3,13), (4,13), (3,12), (3,8)]

#f = "optrue.sat"
for i in range(K):
  for (x,y) in cor:
  #y = random.randint(1,C)
    t = random.randint(1,T)
    p = 0
    s = "a_"+str(x)+"_"+str(y)+"_.*_"+str(t)+" = True"
    #s = "a_.*_"+str(x)+"_"+str(y)+"_"+str(t)+" = True"
    for line in open(f):
      line = line.rstrip()
      if re.search(s, line) :
        p = 1

    if p == 1 :
      print "    insertCheckpoint1X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)
    else:
      print "    insertCheckpoint0X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)

K = 25
cor = [(6,1), (6,3), (6,7), (6,9), (6,11), (7,15), (8,15), (8,3), (8,9), (8,1), (8,7), (8,13), (5,3), (5,5), (5,7), (5,9), (5,15)]

for i in range(K):
  for (x,y) in cor:
  #y = random.randint(1,C)
    t = random.randint(1,T)
    p = 0
    s = "a_"+str(x)+"_"+str(y)+"_.*_"+str(t)+" = True"
    #s = "a_.*_"+str(x)+"_"+str(y)+"_"+str(t)+" = True"
    for line in open(f):
      line = line.rstrip()
      if re.search(s, line) :
        p = 1

    if p == 1 :
      print "    insertCheckpoint1X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)
    else:
      print "    insertCheckpoint0X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)


K = 25
cor = [(6,2), (6,4), (6,6), (6,8), (6,12), (6,14), (7,2), (7,4), (7,6), (7,8), (7,10), (7,12), (7,14), (8,12), (8,8), (8,14), (8,2), (8,10), (8,4), (8,6), (5,2), (5,4), (5,6), (5,8), (5,10), (5,12)]
for i in range(K):
  for (x,y) in cor:
  #y = random.randint(1,C)
    t = random.randint(1,T)
    p = 0
    s = "a_"+str(x)+"_"+str(y)+"_.*_"+str(t)+" = True"
    #s = "a_.*_"+str(x)+"_"+str(y)+"_"+str(t)+" = True"
    for line in open(f):
      line = line.rstrip()
      if re.search(s, line) :
        p = 1

    if p == 1 :
      print "    insertCheckpoint1X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)
    else:
      print "    insertCheckpoint0X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)

  #f = open('dil.sat')
  #s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
  #print "a_" + str(x) + "_" + str(y) + "_?_" + str(t) '=' True"
  #if s.find('a_" + str(x) + "_" + str(y) + "_" + ? + "_" + str(t) = True') != -1:
  #s = a_+str(x)_+str(y)_._+str(t)
  #for line in open("file.txt")
  #  if 
  #print (s)
  #if s.find('a_" + str(x) + "_" + str(y) + "_?_" + str(t) = True') != -1:
    #print "insertCheckpoint1X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)
  #else:
    #print "insertCheckpoint0X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)

#print(random.randint(0,9))
