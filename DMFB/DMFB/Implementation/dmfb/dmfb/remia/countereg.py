import random
import re

f = "optrue.sat"

for line in open(f):
  line = line.replace(' = True\n','')
  li = line.split('_')
  print(li)
  
