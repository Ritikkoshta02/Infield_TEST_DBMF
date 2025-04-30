'''
Created on 07-Jun-2016
@author: sukanta
'''

import subprocess
import networkx as nx
from ast import literal_eval as make_tuple

subprocess.call(["rm","multiDropletClauses.py"])
myfile = open("multiDropletClauses.py","w+")

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
    
def varDeclare(T,dropId,(startRow,startCol),(endRow,endCol),(sourceRow,sourceCol)):
    '''Grid is defined by (startRow,startCol),(endRow,endCol)
    (sourceRow,sourceCol) denotes the test droplet dispenser e.g., (1,0)'''
    #Special variables for test droplet dispenser variables
    varString = ""
    for t in range(1,T+1):
        varString += "x_"+str(dropId)+"_"+str(sourceRow)+"_"+str(sourceCol)+"_"+str(t) +\
                    " = Bool('x_"+str(dropId)+"_"+str(sourceRow)+"_"+str(sourceCol)+"_"+str(t) + "')\n"
    myfile.write(varString)
    
    for r in range(startRow,endRow+1):
        for c in range(startCol,endCol+1):
            varString = ""
            for t in range(1,T+1):
                varString += "x_" + str(dropId) + "_" + str(r) + "_" + \
                         str(c) + "_" + str(t) + " = Bool('" + "x_" +  \
                         str(dropId) + "_" + str(r) + "_" + str(c) +   \
                         "_" + str(t) + "')\n" 
            myfile.write(varString)
    
    
 
def cellInDmfb(row_index, col_index, (startRow,startCol),(endRow,endCol)):
    return ((row_index in range(startRow,endRow+1)) and (col_index in range(startCol,endCol+1)))

def fourNeighbour(row_index, col_index, (startRow,startCol),(endRow,endCol)):
#================================================================================
# Returns 4-neighbour cells of (row_index,col_index) 
# in the biochip defined by (startRow,startCol) and (endRow,endCol)
#================================================================================
    neighbour = []
    
    if cellInDmfb(row_index, col_index, (startRow,startCol),(endRow,endCol)) == False:
        print 'fourNeighbour: Index out of DMFB'
    else:
        if (cellInDmfb(row_index-1, col_index, (startRow,startCol),(endRow,endCol)) == True):
            neighbour.append((row_index-1, col_index))
            
        if (cellInDmfb(row_index, col_index-1, (startRow,startCol),(endRow,endCol)) == True):
            neighbour.append((row_index, col_index-1))
            
        if (cellInDmfb(row_index, col_index+1, (startRow,startCol),(endRow,endCol)) == True ):
            neighbour.append((row_index, col_index+1))
            
        if (cellInDmfb(row_index+1, col_index, (startRow,startCol),(endRow,endCol)) == True):
            neighbour.append((row_index+1, col_index))
        
    return neighbour

def eightNeighbour(row_index, col_index, (startRow,startCol),(endRow,endCol)):
#================================================================================
# Returns 4-neighbour cells of (row_index,col_index) 
# in the biochip defined by (startRow,startCol) and (endRow,endCol)
#================================================================================
    neighbour = []
    
    if cellInDmfb(row_index, col_index, (startRow,startCol),(endRow,endCol)) == False:
        print 'eightNeighbour: Index out of DMFB'
    
    neighbour += fourNeighbour(row_index, col_index, (startRow,startCol),(endRow,endCol))
    
    if (cellInDmfb(row_index-1, col_index-1, (startRow,startCol),(endRow,endCol)) == True):
            neighbour.append((row_index-1, col_index-1))
    if (cellInDmfb(row_index-1, col_index+1, (startRow,startCol),(endRow,endCol)) == True):
            neighbour.append((row_index-1, col_index+1))
    if (cellInDmfb(row_index+1, col_index-1, (startRow,startCol),(endRow,endCol)) == True):
            neighbour.append((row_index+1, col_index-1))
    if (cellInDmfb(row_index+1, col_index+1, (startRow,startCol),(endRow,endCol)) == True):
            neighbour.append((row_index+1, col_index+1))
    
    return neighbour
            
def testDropletClause(T,dropId,(sourceRow,sourceCol),(dispenseRow,dispenseCol), \
                                                            (startRow,startCol),(endRow,endCol)):
#================================================================================
# Clauses for test droplet
# in the biochip defined by (startRow,startCol) and (endRow,endCol)
# Test droplet dispenser is (sourceRow,sourceCol) and
# test droplet is dispensed in (dispenseRow,dispenseCol)
#================================================================================  
    myfile.write('# Test droplet (id = %d) once comes out from reservoir cannot goes back\n'%dropId)
    #-----------------------------------------------------------------------------------------------------------
    for t in range(1,T):
        condition = "s.add(Implies(x_"+str(dropId)+"_"+str(dispenseRow)+"_"+str(dispenseCol)+"_"+str(t)+ ",And("
        for t1 in range(1,t):
            condition += "x_"+str(dropId)+"_"+str(sourceRow)+"_"+str(sourceCol)+"_"+str(t1) + ", "
        for t1 in range(t+1,T+1):
            condition += "Not(x_"+str(dropId)+"_"+str(sourceRow)+"_"+str(sourceCol)+"_"+str(t1)+ "), "
        condition = condition[:-2]
        condition += ")))\n"
        myfile.write(condition)
    #-----------------------------------------------------------------------------------------------------------
    
    myfile.write('# Test droplet clause for droplet id = %d\n'%dropId)
    
    for r in range(startRow,endRow+1):
        for c in range(startCol,endCol+1):
            neighbour = fourNeighbour(r, c, (startRow,startCol),(endRow,endCol))
            if (r,c) == (dispenseRow,dispenseCol):  #Special processing for test droplet dispensing position
                neighbour.append((sourceRow,sourceCol))
            myfile.write('#Condition for cell (%d,%d) for test drop id = %d\n'%(r,c,dropId))
            for t in range(2,T+1):
                condition = "s.add(Implies(x_" + str(dropId) + "_" + str(r) + "_" + str(c) + "_" + str(t) +\
                            ",(Or(x_" + str(dropId) + "_" + str(r) + "_" + str(c) + "_" + str(t-1) + "," 
                for (x,y) in neighbour:
                    condition += "x_" + str(dropId) + "_" + str(x) + "_" + str(y) + "_" + str(t-1) + ","
                
                condition = condition[:-1]
                condition += "))))\n"
                myfile.write(condition)
                
    myfile.write('# Test droplet (Id = %d) consistency condition\n'%dropId)
    testDropletConsistency(T,dropId,(startRow,startCol),(endRow,endCol),(sourceRow,sourceCol))
    
    '''for t in range(1,T+1):
        # 1 test droplet is present at any time instant
        condition = "s.add(("
        for r in range(startRow,endRow+1):
            for c in range(startCol,endCol+1):
                condition += "If(x_"+str(dropId)+"_"+str(r)+"_"+str(c)+"_"+str(t)+" == True,1,0) + "
        condition += "If(x_"+str(dropId)+"_"+str(sourceRow)+"_"+str(sourceCol)+"_" + str(t) + " == True,1,0)"
        condition += ") == 1)\n"
        myfile.write(condition)'''
        
def testDropletConsistency(T,dropId,(startRow,startCol),(endRow,endCol),(sourceRow,sourceCol)):
    '''This function ensures that only one test droplet must be present 
    on the grid or dispense reservoir (sourceRow,sourceCol)'''
    #Special case for source location (sourceRow,sourceCol)
    for t in range(1,T+1):
        condition = "s.add(Implies(x_"+str(dropId)+"_"+str(sourceRow)+"_"+str(sourceCol)+"_"+ str(t) + ", And("
        for r in range(startRow,endRow+1):
            for c in range(startCol,endCol+1):
                condition += "Not(x_"+str(dropId)+"_"+str(r)+"_"+str(c)+"_"+str(t)+"),"
        condition = condition[:-1]
        condition += ")))\n"
        myfile.write(condition)
        
    # At any t, if test droplet appears on a cell, it must not appear other cells    
    for r in range(startRow,endRow+1):
        for c in range(startCol,endCol+1):
            for t in range(1,T+1):
                condition = "s.add(Implies(x_"+str(dropId)+"_"+ str(r) + "_"+ str(c) + "_" + str(t) + ", And("
                for i in range(startRow,endRow+1):
                    for j in range(startCol,endCol+1):
                        if (i,j) == (r,c): # Exclude current cells
                            pass
                        else:
                            condition += "Not(x_"+str(dropId)+"_"+str(i)+"_"+str(j)+"_"+str(t)+"),"
                condition = condition[:-1]
                condition += ")))\n"
                myfile.write(condition)
                
    # At any t, test droplet must appear on source or grid
    for t in range(1,T+1):
        condition = "s.add(Or(x_"+str(dropId)+"_"+str(sourceRow)+"_"+str(sourceCol)+"_"+ str(t)+ ","
        for r in range(startRow,endRow+1):
            for c in range(startCol,endCol+1):
                condition += "x_"+str(dropId)+"_"+str(r)+"_"+str(c)+"_"+str(t)+","
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
            
def staticFCforFunctionalDroplets(dropId,assayFile, (startRow,startCol),(endRow,endCol)):
    global ROW,COL
    snapShotDict = createSnapShotDict(assayFile)
    for t in sorted(snapShotDict.keys()):
        blockedCells = []
        for cell in snapShotDict[t]:
            blockedCells.append(cell)
        
        # Add more blocked cells due to SFC for each cell in blockedCells
        SFCBlockedCells = []
        # case 1. At each time step t, for each blocked cell (x,y) (by functional droplets), 
        # we first check whether (x,y) belongs to current grid. If yes, block this cell for test droplet
        # case 2. Next, we need to check whether any cell in the eight neighbourhood of (x,y)
        # belongs to current grid. If yes, block
        # Note: In the above two cases we successfully block 8-neighbour of a blocked cell appearing on 
        # the current grid and any cell on the current grid that is blocked by the FC of an 
        # functional droplet appearing outside of the current grid 
        for (x,y) in blockedCells:
            if (cellInDmfb(x,y, (startRow,startCol),(endRow,endCol)) == True) and ((x,y) not in SFCBlockedCells):
                # case 1: (x,y) belongs to the current grid
                SFCBlockedCells.append((x,y))
            neighbour = eightNeighbour(x,y,(1,1),(ROW,COL)) 
            #case 2: checking for the presence of 8-neighbouring cells on current grid 
            for cell in neighbour:
                if (cell not in SFCBlockedCells) and \
                            (cellInDmfb(cell[0], cell[1], (startRow,startCol),(endRow,endCol)) == True):
                    # dropId is defined for cell; hence add its corresponding variables 
                    SFCBlockedCells.append(cell)
        
        # If there exists any blocked cell for t, block it
        if len(SFCBlockedCells) > 0:
            myfile.write('#SFC for test droplet (id = %d) at t = %d\n'%(dropId,t))
            condition = "s.add(And("
            for (x,y) in SFCBlockedCells:
                condition += "Not(x_" + str(dropId) + "_" + str(x) + "_" + str(y) + "_" + str(t) + "),"
            condition = condition[:-1]
            condition += "))\n"
            myfile.write(condition)

def staticFCbetweenTestDroplets(T,dropId1,(startRow1,startCol1),(endRow1,endCol1), dropId2,(startRow2,startCol2),\
                                                                                                (endRow2,endCol2)):
    ''' Test droplet (id=dropId1) is moving on the rectangle defined by (startRow1,startCol1),(endRow1,endCol1)
        Test droplet (id=dropId2) is moving on the rectangle defined by (startRow2,startCol2),(endRow2,endCol2)'''
    
    #(sr,sc) denotes the top-left co-ordinate of interference region
    (sr,sc) = (startRow2,startCol2)
    #(er,ec) denotes the bottom-right co-ordinate of interference region    
    (er,ec) = (endRow1,endCol1)
    
    for r in range(sr,er+1):
        for c in range(sc,ec+1):
            for t in range(1,T+1):
                condition1 = "s.add(Implies(x_"+str(dropId1)+"_"+str(r)+"_"+str(c)+"_"+str(t)+\
                                        ", And(Not(x_"+str(dropId2)+"_"+str(r)+"_"+str(c)+"_"+str(t)+"),"
                condition2 = "s.add(Implies(x_"+str(dropId2)+"_"+str(r)+"_"+str(c)+"_"+str(t)+\
                                        ", And(Not(x_"+str(dropId1)+"_"+str(r)+"_"+str(c)+"_"+str(t)+"),"
                neighbour1 = eightNeighbour(r,c,(startRow2,startCol2),(endRow2,endCol2))
                for (x,y) in neighbour1:
                    condition1 += "Not(x_"+str(dropId2)+"_"+str(x)+"_"+str(y)+"_"+str(t)+"),"
                    
                neighbour2 = eightNeighbour(r,c,(startRow1,startCol1),(endRow1,endCol1))
                for (x,y) in neighbour2:
                    condition2 += "Not(x_"+str(dropId1)+"_"+str(x)+"_"+str(y)+"_"+str(t)+"),"
                condition1 = condition1[:-1] + ")))\n"
                condition2 = condition2[:-1] + ")))\n"
                myfile.write('# SFC between Test droplets [%d,%d] at Time = %d for cell (%d,%d)\n'\
                                                                %(dropId1,dropId2,t,r,c))
                myfile.write(condition1)
                myfile.write(condition2)


def edgeCoverage(T,dropId,(x1,y1),(x2,y2)):
    '''Writes a clause that ensure traversal of test droplet dropId on (x1,y1),(x2,y2)'''
    condition = "s.add(Or("
    for t in range(2,T+1):
        condition += "And(x_"+str(dropId)+"_"+str(x1)+"_"+str(y1)+"_"+str(t-1)+\
                        ",x_"+str(dropId)+"_"+str(x2)+"_"+str(y2)+"_"+str(t)+"),"
        condition += "And(x_"+str(dropId)+"_"+str(x2)+"_"+str(y2)+"_"+str(t-1)+\
                        ",x_"+str(dropId)+"_"+str(x1)+"_"+str(y1)+"_"+str(t)+"),"
    condition = condition[:-1]+"))\n"
    
    myfile.write(condition)
                    
    

        
#------------------PCR---------------------------------
ROW = 8         #Dimension of the Biochip
COL = 15
T = 67
init()

#Specific for left block
dropId=1
(startRow,startCol) = (1,1)
(endRow,endCol) = (8,9)
(sourceRow,sourceCol) = (8,0)
(dispenseRow,dispenseCol) = (8,1)
varDeclare(T,dropId,(startRow,startCol),(endRow,endCol),(sourceRow,sourceCol))
testDropletClause(T,dropId,(sourceRow,sourceCol),(dispenseRow,dispenseCol), (startRow,startCol),(endRow,endCol))
staticFCforFunctionalDroplets(dropId,'assayPCR8x15.txt', (startRow,startCol),(endRow,endCol))
myfile.write('s.add(x_%d_%d_%d_1)\n'%(dropId,sourceRow,sourceCol))
myfile.write('s.add(x_%d_%d_%d_%d)\n'%(dropId,dispenseRow,dispenseCol,T))

#Specific for right block
dropId=2
(startRow,startCol) = (1,7)
(endRow,endCol) = (8,15)
(sourceRow,sourceCol) = (8,16)
(dispenseRow,dispenseCol) = (8,15)
varDeclare(T,dropId,(startRow,startCol),(endRow,endCol),(sourceRow,sourceCol))
testDropletClause(T,dropId,(sourceRow,sourceCol),(dispenseRow,dispenseCol), (startRow,startCol),(endRow,endCol))
staticFCforFunctionalDroplets(dropId,'assayPCR8x15.txt', (startRow,startCol),(endRow,endCol))
myfile.write('s.add(x_%d_%d_%d_1)\n'%(dropId,sourceRow,sourceCol))
myfile.write('s.add(x_%d_%d_%d_%d)\n'%(dropId,dispenseRow,dispenseCol,T))

# Interference constraint between dropId = 1,2
staticFCbetweenTestDroplets(T,1,(1,1),(8,9), 2,(1,7),(8,15))

# Edge coverage constraints
edgeCoverage(T,1,(2,2),(2,3))
edgeCoverage(T,1,(2,3),(2,4))
edgeCoverage(T,1,(2,4),(2,5))
edgeCoverage(T,1,(3,1),(3,2))
edgeCoverage(T,1,(3,4),(3,5))
edgeCoverage(T,1,(3,5),(3,6))
edgeCoverage(T,1,(3,6),(3,7))
edgeCoverage(T,1,(4,1),(4,2))
edgeCoverage(T,1,(5,1),(5,2))
edgeCoverage(T,1,(7,1),(7,2))
edgeCoverage(T,1,(7,2),(7,3))
edgeCoverage(T,1,(7,3),(7,4))
edgeCoverage(T,1,(7,4),(7,5))
edgeCoverage(T,1,(7,5),(7,6))
edgeCoverage(T,1,(7,6),(7,7))
#----------------------------
edgeCoverage(T,1,(3,1),(4,1))
edgeCoverage(T,1,(4,1),(5,1))
edgeCoverage(T,1,(1,2),(2,2))
edgeCoverage(T,1,(2,2),(3,2))
edgeCoverage(T,1,(3,2),(4,2))
edgeCoverage(T,1,(4,2),(5,2))
edgeCoverage(T,1,(5,2),(6,2))
edgeCoverage(T,1,(6,2),(7,2))
edgeCoverage(T,1,(2,4),(3,4))
edgeCoverage(T,1,(1,5),(2,5))
edgeCoverage(T,1,(2,5),(3,5))
edgeCoverage(T,1,(3,7),(4,7))
edgeCoverage(T,1,(4,7),(5,7))
edgeCoverage(T,1,(5,7),(6,7))
edgeCoverage(T,1,(6,7),(7,7))
#++++++++++++++++++++++++++++
edgeCoverage(T,2,(1,8),(1,9))
edgeCoverage(T,2,(1,9),(1,10))
edgeCoverage(T,2,(1,10),(1,11))
edgeCoverage(T,2,(1,11),(1,12))
edgeCoverage(T,2,(3,7),(3,8)) #cross edge between two partition
edgeCoverage(T,2,(3,8),(3,9))
edgeCoverage(T,2,(3,9),(3,10))
edgeCoverage(T,2,(3,10),(3,11))
edgeCoverage(T,2,(3,11),(3,12))
edgeCoverage(T,2,(3,14),(3,15))
edgeCoverage(T,2,(5,10),(5,11))
edgeCoverage(T,2,(5,11),(5,12))
edgeCoverage(T,2,(5,12),(5,13))
edgeCoverage(T,2,(5,13),(5,14))
edgeCoverage(T,2,(6,14),(6,15))
edgeCoverage(T,2,(7,14),(7,15))
edgeCoverage(T,2,(8,13),(8,14))
#----------------------------
edgeCoverage(T,2,(1,10),(2,10))
edgeCoverage(T,2,(2,10),(3,10))
edgeCoverage(T,2,(3,10),(4,10))
edgeCoverage(T,2,(4,10),(5,10))
edgeCoverage(T,2,(1,12),(2,12))
edgeCoverage(T,2,(2,12),(3,12))
edgeCoverage(T,2,(3,12),(4,12))
edgeCoverage(T,2,(4,12),(5,12))
edgeCoverage(T,2,(1,14),(2,14))
edgeCoverage(T,2,(2,14),(3,14))
edgeCoverage(T,2,(3,14),(4,14))
edgeCoverage(T,2,(4,14),(5,14))
edgeCoverage(T,2,(5,14),(6,14))
edgeCoverage(T,2,(6,14),(7,14))
edgeCoverage(T,2,(7,14),(8,14))
edgeCoverage(T,2,(6,15),(7,15))

finish()








#----------------------------------------------------------Dump----------
# def varDeclareForDMFBCellEdges((startRow,startCol),(endRow,endCol)):
#     '''Edges are created row wise first i.e., (1,1)--(1,2)--(1,3)
#     then column wise (1,1)
#                        |
#                      (2,1)
#                        |
#                      (3,1)
#     Note1: For edge coverage edges must be given in this order
#     Note2: edge variables is not dependent upon test droplet
#            and each test droplet must ensure correct edge traversal'''
#     
#     global G
#     # create vertices
#     for r in range(startRow,endRow+1):
#         for c in range(startCol,endCol+1):
#             G.add_node((r,c))
#     
#     # create edges
#     #print 'Creating edges'
#     for r in range(startRow,endRow+1):
#         for c in range(startCol+1,endCol+1):
#             G.add_edge((r,c-1),(r,c))
#             #print "(%d,%d)--(%d,%d)"%(r,c-1,r,c)
#             varName = 'e_%d_%d_%d_%d'%(r,c-1,r,c)
#             G[(r,c-1)][(r,c)]['var'] = varName
#     for r in range(startRow+1,endRow+1):
#         for c in range(startCol,endCol+1):
#             G.add_edge((r-1,c),(r,c))
#             #print "(%d,%d)--(%d,%d)"%(r-1,c,r,c)
#             varName = 'e_%d_%d_%d_%d'%(r-1,c,r,c)
#             G[(r-1,c)][(r,c)]['var'] = varName
#             
#     myfile.write('#Edge variables\n')
#     for (u,v) in G.edges():
#         edgeVar = G[u][v]['var']
#         myfile.write(edgeVar + " = Bool('" + edgeVar + "')\n")



# def edgeCoverageClause(T, dropId,(startRow,startCol),(endRow,endCol)):
# # Valid for only one test droplet
#     myfile.write("#Edge coverage clauses\n")
#     for (u,v) in G.edges():
#         edgeVar = G[u][v]['var']   
#         if (cellInDmfb(u[0],u[1], (startRow,startCol),(endRow,endCol)) == True) and \
#             (cellInDmfb(v[0],v[1], (startRow,startCol),(endRow,endCol)) == True):                
#             condition = "s.add(" +edgeVar + " == Or("
#             for t in range(2,T+1):
#                 condition += "And(x_" + str(dropId) + "_" + str(u[0]) + "_" + str(u[1]) + "_" + str(t-1) +\
#                                 ", x_" + str(dropId) + "_" + str(v[0]) + "_" + str(v[1]) + "_" + str(t) + ")," + \
#                                 "And(x_" + str(dropId) + "_" + str(v[0]) + "_" + str(v[1]) + "_" + str(t-1) +\
#                                 ", x_" + str(dropId) + "_" + str(u[0]) + "_" + str(u[1]) + "_" + str(t) + "),"
#             condition = condition[:-1]
#             condition += "))\n"
#             
#             myfile.write(condition)



