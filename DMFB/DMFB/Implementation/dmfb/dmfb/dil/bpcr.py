import random
import re
T = 38
K = 28
cor = [(4,1), (4,2), (4,7), (4,8), (5,1), (5,2), (5,7), (5,8), (6,1), (6,8)]
#cor = [(2,1), (3,1), (3,3), (4,4), (3,4), (1,1), (7,1), (7,2), (7,8), (7,7), (1,3), (2,3), (2,6)]
#cor = [(2,2), (3,2), (2,4), (2,5), (3,7), (3,6), (2,8), (7,3), (7,5), (8,5), (8,7), (9,6), (9,7)]
#(R, C, T, K) = (8,15,70,420)
f = "diltrue.sat"
for i in range(K):
  for (x,y) in cor:
  #y = random.randint(1,C)
    t = random.randint(1,T)
    p = 0
    s = "a_"+str(x)+"_"+str(y)+"_.*_"+str(t)+" = True"
    for line in open(f):
      line = line.rstrip()
      if re.search(s, line) :
        p = 1
  
    if p == 1 :
      print "    insertCheckpoint1X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)
    else:
      print "    insertCheckpoint0X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t) 



K = 23
cor = [(2,1), (3,1), (3,3), (4,4), (3,4), (1,1), (7,1), (7,2), (7,8), (7,7), (1,3), (2,3), (2,6)]
#(R, C, T, K) = (8,15,70,420)
for i in range(K):
  for (x,y) in cor:
  #y = random.randint(1,C)
    t = random.randint(1,T)
    p = 0
    s = "a_"+str(x)+"_"+str(y)+"_.*_"+str(t)+" = True"
    for line in open(f):
      line = line.rstrip()
      if re.search(s, line) :
        p = 1

    if p == 1 :
      print "    insertCheckpoint1X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)
    else:
      print "    insertCheckpoint0X(clauseFile, (%d,%d), %d, dropletIdList)" %(x,y,t)  



K = 18
cor = [(2,2), (3,2), (2,4), (2,5), (3,7), (3,6), (2,8), (7,3), (7,5), (8,5), (8,7), (9,6), (9,7), (8,2), (8,4), (8,3), (7,6), (9,2), (9,8), (9,3), (8,8), (9,5), (9,4)]
#(R, C, T, K) = (8,15,70,420)
for i in range(K):
  for (x,y) in cor:
  #y = random.randint(1,C)
    t = random.randint(1,T)
    p = 0
    s = "a_"+str(x)+"_"+str(y)+"_.*_"+str(t)+" = True"
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
