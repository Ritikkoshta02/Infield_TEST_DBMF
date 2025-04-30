'''
Created on 13-Jan-2016
@author: sukanta
'''

import subprocess
import networkx as nx
from ast import literal_eval as make_tuple

subprocess.call(["rm","clauses.py"])
myfile = open("clauses.py","w+")

G = nx.Graph()


def init():
#===============================================================================
# init() appends the initial conditions for the z3 solver to analyse the clauses
#===============================================================================
    myfile.write("import sys\n")
    myfile.write("import time\n")
    myfile.write("sys.path.append(\"/home/sukanta/App/z3/bin\")\n")
    myfile.write("from z3 import *\n")
    myfile.write("s=Solver()\n")
    
def finish():    
    myfile.write('fp = open(\'op\',\'w\')\n')
    myfile.write('start = time.time()\n')
    myfile.write('if s.check() == unsat:\n')
    myfile.write('    print \'unsat\'\n')
    myfile.write('    print time.time()-start \n')
    myfile.write('else:\n')
    myfile.write("    print \'sat\'\n")
    myfile.write("    lst = s.model()\n")
    myfile.write("    for i in lst:\n")
    myfile.write("        fp.write(str(i) + \" = \" + str(s.model()[i]) + '\\n')\n")
    myfile.write("    print time.time()-start \n")
    
    myfile.close()
    
    
def varDeclare(T,testDropletId,(row,col)):
    #Special cell (1,0) for test droplet
    varString = ""
    for t in range(1,T+1):
        varString += "x_1_1_0_" + str(t) + " = Bool('x_1_1_0_" + str(t) + "')\n" 
    myfile.write(varString)
    
    for r in range(1,row+1):
        for c in range(1,col+1):
            varString = ""
            for t in range(1,T+1):
                varString += "x_" + str(testDropletId) + "_" + str(r) + "_" +       \
                         str(c) + "_" + str(t) + " = Bool('" + "x_" +    \
                         str(testDropletId) + "_" + str(r) + "_" + str(c) +     \
                         "_" + str(t) + "')\n" 
            myfile.write(varString)
    myfile.write('#Variables for source reservoir of test droplet\n')
    
def varDeclareForDMFBCellEdges(row,col):
    '''Edges are created row wise first i.e., (1,1)--(1,2)--(1,3)
    then column wise (1,1)
                       |
                     (2,1)
                       |
                     (3,1)
    Note:: For edge coverage edges must be given in this order'''
    
    global G
    # create vertices
    for r in range(1,row+1):
        for c in range(1,col+1):
            G.add_node((r,c))
    
    # create edges
    #print 'Creating edges'
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

def eightNeighbour(row_index, col_index, row, col):
#================================================================================
# Returns 4-neighbour cells of (row_index,col_index) 
# in the biochip of size row X col
#================================================================================
    neighbour = []
    
    if cellInDmfb(row_index, col_index, row, col) == False:
        print 'eightNeighbour: Index out of DMFB'
    
    neighbour += fourNeighbour(row_index, col_index, row, col)
    
    if (cellInDmfb(row_index-1, col_index-1, row, col) == True):
            neighbour.append((row_index-1, col_index-1))
    if (cellInDmfb(row_index-1, col_index+1, row, col) == True):
            neighbour.append((row_index-1, col_index+1))
    if (cellInDmfb(row_index+1, col_index-1, row, col) == True):
            neighbour.append((row_index+1, col_index-1))
    if (cellInDmfb(row_index+1, col_index+1, row, col) == True):
            neighbour.append((row_index+1, col_index+1))
    
    return neighbour
            
def testDropletClause(T,testDropletId, (row,col)):
#================================================================================
# Clauses for test droplet
# in the biochip of size row X col
#================================================================================  
    global G 
    myfile.write('# Test droplet once comes out from reservoir cannot goes back\n')
    '''for t in range(2,T+1):
        condition = "s.add(Implies(And(x_1_1_0_" + str(t-1) + ", x_1_1_1_" + str(t) + "),And("
        for t1 in range(t,T+1):
            condition += "Not(x_1_1_0_" + str(t1) + "), "
        condition = condition[:-2]
        condition += ")))\n"
        myfile.write(condition)'''
    
    #-----------------------------------------------------------------------------------------------------------
    for t in range(1,T):
        condition = "s.add(Implies(x_1_1_1_" + str(t) + ",And("
        for t1 in range(1,t):
            condition += "x_1_1_0_" + str(t1) + ", "
        for t1 in range(t+1,T+1):
            condition += "Not(x_1_1_0_" + str(t1) + "), "
        condition = condition[:-2]
        condition += ")))\n"
        myfile.write(condition)
    #-----------------------------------------------------------------------------------------------------------
    
         
    myfile.write('# Test droplet clause for dropletid %d\n' %testDropletId)
    
    for r in range(1,row+1):
        for c in range(1,col+1):
            neighbour = fourNeighbour(r, c, row, col)
            if (r,c) == (1,1):  #Special processing
                neighbour.append((1,0))
            myfile.write('#Condition for cell (%d,%d)\n'%(r,c))
            for t in range(2,T+1):
                condition = "s.add(Implies(x_" + str(testDropletId) + "_" + str(r) + "_" + str(c) + "_" + str(t) +\
                            ",(Or(x_" + str(testDropletId) + "_" + str(r) + "_" + str(c) + "_" + str(t-1) + "," 
                for (x,y) in neighbour:
                    condition += "x_" + str(testDropletId) + "_" + str(x) + "_" + str(y) + "_" + str(t-1) + ","
                
                condition = condition[:-1]
                condition += "))))\n"
                myfile.write(condition)
                
    '''myfile.write('# Test droplet (Id = %d) consistency condition\n'%testDropletId)
    for t in range(1,T+1):
        # 1 test droplet is present at any time instant
        condition = "s.add(("
        for r in range(1,row+1):
            for c in range(1,col+1):
                condition += "If(x_"+str(testDropletId)+"_"+str(r)+"_"+str(c)+"_"+str(t)+" == True,1,0) + "
        condition += "If(x_1_1_0_" + str(t) + " == True,1,0)"
        condition += ") == 1)\n"
        myfile.write(condition)'''
                
                
def testDropletPresence(T, testDropId,(row,col)):
    #Special case for source location (1,0)
    for t in range(1,T+1):
        condition = "s.add(Implies(x_1_1_0_" + str(t) + ", And("
        for r in range(1,row+1):
            for c in range(1,col+1):
                condition += "Not(x_1_"+str(r)+"_"+str(c)+"_"+str(t)+"),"
        condition = condition[:-1]
        condition += ")))\n"
        myfile.write(condition)
        
    #For remaining cells exclude current cells
    for r in range(1,row+1):
        for c in range(1,col+1):
            for t in range(1,T+1):
                condition = "s.add(Implies(x_1_" + str(r) + "_"+ str(c) + "_" + str(t) + ", And(Not(x_1_1_0_"+str(t)+"),"
                for i in range(1,row+1):
                    for j in range(1,col+1):
                        if (i,j) == (r,c):
                            pass
                        else:
                            condition += "Not(x_1_"+str(i)+"_"+str(j)+"_"+str(t)+"),"
                condition = condition[:-1]
                condition += ")))\n"
                myfile.write(condition)
                
    # At any t test droplet must appear on source or grid
    for t in range(1,T+1):
        condition = "s.add(Or(x_1_1_0_" + str(t)+ ","
        for r in range(1,row+1):
            for c in range(1,col+1):
                condition += "x_1_"+str(r)+"_"+str(c)+"_"+str(t)+","
        condition = condition[:-1]
        condition += "))\n"
        myfile.write(condition)
        

def edgeCoverageClause(T, testDropletId):
# Valid for only one test droplet
    myfile.write("#Edge coverage clauses\n")
    for (u,v) in G.edges():
        edgeVar = G[u][v]['var']                    
        condition = "s.add(" +edgeVar + " == Or("
        for t in range(2,T+1):
            condition += "And(x_" + str(testDropletId) + "_" + str(u[0]) + "_" + str(u[1]) + "_" + str(t-1) +\
                            ", x_" + str(testDropletId) + "_" + str(v[0]) + "_" + str(v[1]) + "_" + str(t) + ")," + \
                            "And(x_" + str(testDropletId) + "_" + str(v[0]) + "_" + str(v[1]) + "_" + str(t-1) +\
                            ", x_" + str(testDropletId) + "_" + str(u[0]) + "_" + str(u[1]) + "_" + str(t) + "),"
        condition = condition[:-1]
        condition += "))\n"
        
        myfile.write(condition)



def createSnapShotDict(assayFile):
    '''Reads snapshots at each time step from an file and stores it into a table
    Note: Snapshot at each time is essential for correct operation''' 
    snapShotDict = dict()
    fp = open(assayFile,'r')
    for line in fp.readlines():
        if line == "end\n":
            break
        occupiedCells = line.split()
        time = int(occupiedCells[0])
        snapShotDict[time] = []
        for i in range(1,len(occupiedCells)):
            cell =  make_tuple(occupiedCells[i])
            snapShotDict[time].append(cell)
    
    return snapShotDict
            
def staticFCforFunctionalDroplets(testDropletId,assayFile, row, col):
    snapShotDict = createSnapShotDict(assayFile)
    for t in sorted(snapShotDict.keys()):
        blockedCells = []
        for cell in snapShotDict[t]:
            blockedCells.append(cell)
        
        # Add more blocked cells due to SFC for each cell in blockedCells
        SFCBlockedCells = []
        for (x,y) in blockedCells:
            SFCBlockedCells.append((x,y))
            neighbour = eightNeighbour(x,y,row,col)
            for cell in neighbour:
                if cell not in SFCBlockedCells:
                    SFCBlockedCells.append(cell)

        # Write clauses for t
        myfile.write('#SFC for functional droplets at t = %d\n'%t)
        condition = "s.add(And("
        for (x,y) in SFCBlockedCells:
            condition += "Not(x_" + str(testDropletId) + "_" + str(x) + "_" + str(y) + "_" + str(t) + "),"
        condition = condition[:-1]
        condition += "))\n"
        myfile.write(condition)

def staticFCandDynamicFCforFunctionalDroplets(testDropletId,assayFile, row, col):
    snapShotDict = createSnapShotDict(assayFile)
    for t in sorted(snapShotDict.keys()):
        blockedCells = []
        # For static FC
        for cell in snapShotDict[t]:
            blockedCells.append(cell)
        # For dynamic FC
        if t-1 in snapShotDict.keys():
            for cell in snapShotDict[t-1]:
                blockedCells.append(cell)
        if t+1 in snapShotDict.keys():
            for cell in snapShotDict[t+1]:
                blockedCells.append(cell)
        
        # Add more blocked cells due to SFC for each cell in blockedCells
        SFCBlockedCells = []
        for (x,y) in blockedCells:
            SFCBlockedCells.append((x,y))
            neighbour = eightNeighbour(x,y,row,col)
            for cell in neighbour:
                if cell not in SFCBlockedCells:
                    SFCBlockedCells.append(cell)

        # Write clauses for t
        myfile.write('#SFC for functional droplets at t = %d\n'%t)
        condition = "s.add(And("
        for (x,y) in SFCBlockedCells:
            condition += "Not(x_" + str(testDropletId) + "_" + str(x) + "_" + str(y) + "_" + str(t) + "),"
        condition = condition[:-1]
        condition += "))\n"
        myfile.write(condition)
        
#----------------------------PCR-------------------------

'''T = 80
(row,col) = (8,15)

init()
varDeclare(T,1,(row,col))
varDeclareForDMFBCellEdges(row,col)

testDropletClause(T,1, (row,col))
testDropletPresence(T, 1,(row,col))
staticFCforFunctionalDroplets(1,'assayPCR8x15.txt', row, col)
#staticFCandDynamicFCforFunctionalDroplets(1,'assayInVitro7x7.txt', row, col)
edgeCoverageClause(T, 1)
# myfile.write('s.add(And(e_1_8_1_9, e_1_9_1_10, e_1_10_1_11, e_1_11_1_12, e_2_2_2_3,\
# e_2_3_2_4, e_2_4_2_5, e_3_1_3_2, e_3_4_3_5, e_3_5_3_6, e_3_6_3_7, e_3_7_3_8, e_3_8_3_9,\
# e_3_9_3_10, e_3_10_3_11, e_3_11_3_12, e_3_14_3_15, e_4_1_4_2, e_5_1_5_2, e_5_10_5_11, \
# e_5_11_5_12, e_5_12_5_13, e_5_13_5_14, e_6_14_6_15, e_7_1_7_2, e_7_2_7_3, e_7_3_7_4, \
# e_7_4_7_5, e_7_5_7_6, e_7_6_7_7, e_7_14_7_15, e_8_13_8_14, e_3_1_4_1, e_4_1_5_1, e_1_2_2_2,\
# e_2_2_3_2, e_3_2_4_2, e_4_2_5_2, e_5_2_6_2, e_6_2_7_2, e_2_4_3_4, e_1_5_2_5, e_2_5_3_5, \
# e_3_7_4_7, e_4_7_5_7, e_5_7_6_7, e_6_7_7_7, e_1_10_2_10, e_2_10_3_10, e_3_10_4_10, \
# e_4_10_5_10, e_1_12_2_12, e_2_12_3_12, e_3_12_4_12, e_4_12_5_12, e_1_14_2_14, \
# e_2_14_3_14, e_3_14_4_14, e_4_14_5_14, e_5_14_6_14, e_6_14_7_14, e_7_14_8_14, e_6_15_7_15))\n')
myfile.write('s.add(And(e_1_8_1_9, e_1_9_1_10, e_1_10_1_11, e_1_11_1_12, e_2_2_2_3,\
e_2_3_2_4, e_2_4_2_5, e_3_1_3_2, e_3_4_3_5, e_3_5_3_6, e_3_6_3_7, e_3_7_3_8, e_3_8_3_9,\
e_3_9_3_10, e_3_10_3_11, e_3_11_3_12, e_3_14_3_15, e_4_1_4_2, e_5_1_5_2, e_5_10_5_11, \
e_5_11_5_12, e_5_12_5_13, e_5_13_5_14, e_6_14_6_15, e_7_1_7_2, e_7_2_7_3, e_7_3_7_4,\
e_7_4_7_5, e_7_5_7_6, e_7_6_7_7, e_7_14_7_15, e_8_13_8_14, e_3_1_4_1, e_4_1_5_1, e_1_2_2_2))\n')

myfile.write('s.add(x_1_1_0_1)\n')
myfile.write('s.add(x_1_%d_%d_%d)\n'%(row,col,T))
finish()'''





#------------------In-Vito----------------------------        
T = 45
(row,col) = (7,7)

init()
varDeclare(T,1,(row,col))
varDeclareForDMFBCellEdges(row,col)

testDropletClause(T,1, (row,col))
testDropletPresence(T, 1,(row,col))
#staticFCforFunctionalDroplets(1,'assayInVitro7x7.txt', row, col)
staticFCandDynamicFCforFunctionalDroplets(1,'assayInVitro7x7.txt', row, col)
edgeCoverageClause(T, 1)
myfile.write('s.add(And(e_3_1_3_2, e_3_2_3_3, e_3_3_3_4, e_3_4_3_5, e_3_5_3_6, e_3_6_3_7,\
e_3_3_4_3, e_4_3_5_3, e_5_3_5_4, e_5_4_5_5, e_5_5_6_5, e_6_5_7_5,\
e_3_6_4_6, e_4_6_5_6, e_5_6_6_6, e_6_6_7_6, e_7_5_7_6,\
e_5_5_5_6, e_6_5_6_6, e_7_5_7_6))\n')

myfile.write('s.add(x_1_1_0_1)\n')
myfile.write('s.add(x_1_%d_%d_%d)\n'%(row,col,T))
finish()


#-----------------REMIA----------------------------

''''T = 85
(row,col) = (10,10)

init()
varDeclare(T,1,(row,col))
varDeclareForDMFBCellEdges(row,col)

testDropletClause(T,1, (row,col))
testDropletPresence(T, 1,(row,col))
#staticFCforFunctionalDroplets(1,'assayREMIA10x10.txt', row, col)
staticFCandDynamicFCforFunctionalDroplets(1,'assayREMIA10x10.txt', row, col)
edgeCoverageClause(T, 1)
myfile.write('s.add(And(e_6_1_6_2, e_6_2_6_3, e_6_3_6_4, e_6_4_6_5, e_6_5_6_6, e_6_6_6_7, e_6_7_6_8,\
e_6_8_6_9, e_6_9_6_10, e_6_4_7_4, e_7_4_8_4, e_8_4_9_4, e_9_4_9_5,  e_9_5_9_6, e_9_6_9_7,\
e_6_7_7_7, e_7_7_8_7, e_8_7_9_7, e_9_7_10_7, e_1_4_2_4, e_2_4_3_4, e_3_4_4_4, e_4_4_5_4, \
e_5_4_6_4, e_2_7_3_7, e_3_7_4_7, e_4_7_5_7, e_5_7_6_7, e_2_4_2_5, e_2_5_2_6, e_2_6_2_7))\n')

myfile.write('s.add(x_1_1_0_1)\n')
myfile.write('s.add(x_1_%d_%d_%d)\n'%(row,col,T))
finish()
'''
