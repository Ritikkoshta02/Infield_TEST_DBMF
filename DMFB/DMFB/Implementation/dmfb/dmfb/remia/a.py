import random
import re

(R, C, T, K) = (5,5,30,340)
f = "optrue.sat"
for i in range(K):
  x = random.randint(1,R)
  y = random.randint(1,C)
  t = random.randint(1,T)
  p = 0
  s = "a_"+str(x)+"_"+str(y)+"_._"+str(t)+" = True"
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
