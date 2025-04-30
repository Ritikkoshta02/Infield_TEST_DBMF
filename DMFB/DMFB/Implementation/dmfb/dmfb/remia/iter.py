import sys
#import time
#sys.path.append("/home/sukanta/App/z3-master/build")
from z3 import *
#s = Optimize()
p, q, r = Bools('p q r')
s = Solver()
s.add(Implies(p, q))
s.add(Not(q))
print(s.check())
s.push()
s.add(p)
print(s.check())
s.pop()
print(s.check())
