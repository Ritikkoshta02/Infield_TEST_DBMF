'''
Created on 13-Jan-2016
@author: sukanta
'''

import subprocess
import networkx as nx
subprocess.call(["rm","clauses.py"])
myfile = open("clauses.py","w+")

G = nx.DiGraph()

def init():
#===============================================================================
# init() appends the initial conditions for the z3 solver to analyse the clauses
#===============================================================================
    myfile.write("import sys\n")
    myfile.write("sys.path.append(\"/home/sukanta/App/z3/bin\")\n")
    myfile.write("from z3 import *\n")
    myfile.write("s=Solver()\n")
    
def finish():     
    myfile.write("print s.check()\n")
    myfile.write("lst=s.model()\n")
    myfile.write("for i in lst:\n")
    myfile.write("   print str(i) + \" = \" + str(s.model()[i])\n")
    
    myfile.close()
    
def varDeclare(T,testDropletId,(row,col)):
    for r in range(1,row+1):
        for c in range(1,col+1):
            varString = ""
            for t in range(1,T+1):
                varString += "x_" + str(testDropletId) + "_" + str(r) + "_" +       \
                         str(c) + "_" + str(t) + " = Bool('" + "x_" +    \
                         str(testDropletId) + "_" + str(r) + "_" + str(c) +     \
                         "_" + str(t) + "')\n" 
            myfile.write(varString)

def varDeclareForDMFBCellEdges(row,col):
    global G
    # create vertices
    for r in range(1,row+1):
        for c in range(1,col+1):
            G.add_node((r,c))
    
    # create edges
    for r in range(1,row+1):
        for c in range(2,col+1):
            G.add_edge((r,c-1),(r,c))
            #print "(%d,%d)--(%d,%d)"%(r,c-1,r,c)
            varName = 'e_%d_%d_%d_%d'%(r,c-1,r,c)
            G[(r,c-1)][(r,c)]['var'] = varName
    for r in range(2,row+1):
        for c in range(1,col+1):
            G.add_edge((r-1,c),(r,c))
            #print "(%d,%d)--(%d,%d)"%(r-1,c,r,c)
            varName = 'e_%d_%d_%d_%d'%(r-1,c,r,c)
            G[(r-1,c)][(r,c)]['var'] = varName
            
    myfile.write('#Edge variables\n')
    for (u,v) in G.edges():
        edgeVar = G[u][v]['var']
        myfile.write(edgeVar + " = Bool('" + edgeVar + "')\n")
            
def cellInDmfb(row_index, col_index, row, col):
    return ((row_index in range(1,row+1)) and (col_index in range(1,col+1)))

def fourNeighbour(row_index, col_index, row, col):
#================================================================================
# Returns 4-neighbour cells of (row_index,col_index) 
# in the biochip of size row X col
#================================================================================
    neighbour = []
    
    if cellInDmfb(row_index, col_index, row, col) == False:
        print 'fourNeighbour: Index out of DMFB'
    else:
        if (cellInDmfb(row_index-1, col_index, row, col) == True):
            neighbour.append((row_index-1, col_index))
            
        if (cellInDmfb(row_index, col_index-1, row, col) == True):
            neighbour.append((row_index, col_index-1))
            
        if (cellInDmfb(row_index, col_index+1, row, col) == True ):
            neighbour.append((row_index, col_index+1))
            
        if (cellInDmfb(row_index+1, col_index, row, col) == True):
            neighbour.append((row_index+1, col_index))
        
    return neighbour
            
def testDropletClause(T,testDropletId, (row,col)):
#================================================================================
# Clauses for test droplet
# in the biochip of size row X col
#================================================================================  
    global G      
    myfile.write('# Test droplet clause for dropletid %d\n' %testDropletId)
    
    for r in range(1,row+1):
        for c in range(1,col+1):
            neighbour = fourNeighbour(r, c, row, col)
            myfile.write('#Condition for cell (%d,%d)\n'%(r,c))
            for t in range(2,T+1):
                condition = "s.add(Implies(x_" + str(testDropletId) + "_" + str(r) + "_" + str(c) + "_" + str(t) +\
                            ",(Or(x_" + str(testDropletId) + "_" + str(r) + "_" + str(c) + "_" + str(t-1) + "," 
                for (x,y) in neighbour:
                    condition += "x_" + str(testDropletId) + "_" + str(x) + "_" + str(y) + "_" + str(t-1) + ","
                
                condition = condition[:-1]
                condition += "))))\n"
                myfile.write(condition)
                
    myfile.write('# Test droplet (Id = %d) consistency condition\n'%testDropletId)
    for t in range(1,T+1):
        # Atmost 1 test droplet is present at any time instant
        condition = "s.add(("
        for r in range(1,row+1):
            for c in range(1,col+1):
                condition += "If(x_"+str(testDropletId)+"_"+str(r)+"_"+str(c)+"_"+str(t)+" == True,1,0) + "
        condition = condition[:-3]
        condition += ") == 1)\n"
        myfile.write(condition)
        

def edgeCoverageClause(T, testDropletId):
# Valid for only one test droplet
    myfile.write("#Edge coverage clauses\n")
    for (u,v) in G.edges():
        edgeVar = G[u][v]['var']                    
        condition = "s.add(Implies(" + edgeVar + ", ("
        for t in range(2,T+1):
            condition += "If(Or(And(x_" + str(testDropletId) + "_" + str(u[0]) + "_" + str(u[1]) + "_" + str(t-1) +\
                            ", x_" + str(testDropletId) + "_" + str(v[0]) + "_" + str(v[1]) + "_" + str(t) + ")," + \
                            "And(x_" + str(testDropletId) + "_" + str(v[0]) + "_" + str(v[1]) + "_" + str(t-1) +\
                            ", x_" + str(testDropletId) + "_" + str(u[0]) + "_" + str(u[1]) + "_" + str(t) + ")) == True,1,0) + "
        condition = condition[:-3]
        condition += ") >= 1))\n"
        
        myfile.write(condition)
        
    myfile.write('#Condition for visiting all edges\n')
    condition = "s.add(And("
    for (u,v) in G.edges():
        edgeVar = G[u][v]['var'] 
        condition += edgeVar + ", "
    condition = condition[:-2]
    condition += "))\n"
    myfile.write(condition)
    
    
    
T = 90
(row,col) = (7,7)
init()
varDeclare(T,1,(row,col))
varDeclareForDMFBCellEdges(row,col)

testDropletClause(T,1, (row,col))
edgeCoverageClause(T, 1)

myfile.write('s.add(And(x_1_1_1_1,x_1_1_1_90))\n')
finish()
