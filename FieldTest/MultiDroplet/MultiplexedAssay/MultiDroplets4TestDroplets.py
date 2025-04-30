'''
Created on 23-Jun-2016
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
        condition += "Or(And(x_"+str(dropId)+"_"+str(x1)+"_"+str(y1)+"_"+str(t-1)+\
                        ",x_"+str(dropId)+"_"+str(x2)+"_"+str(y2)+"_"+str(t)+"),"
        condition += "And(x_"+str(dropId)+"_"+str(x2)+"_"+str(y2)+"_"+str(t-1)+\
                        ",x_"+str(dropId)+"_"+str(x1)+"_"+str(y1)+"_"+str(t)+")),"
    condition = condition[:-1]+"))\n"
    
    myfile.write(condition)
                    
    

        
#------------------PCR---------------------------------
ROW = 16         #Dimension of the Biochip
COL = 16
T = 160
init()

#Specific for top-left block
dropId=1
(startRow,startCol) = (1,1)
(endRow,endCol) = (9,9)
(sourceRow,sourceCol) = (1,0)
(dispenseRow,dispenseCol) = (1,1)
varDeclare(T,dropId,(startRow,startCol),(endRow,endCol),(sourceRow,sourceCol))
testDropletClause(T,dropId,(sourceRow,sourceCol),(dispenseRow,dispenseCol), (startRow,startCol),(endRow,endCol))
staticFCforFunctionalDroplets(dropId,'invitro_16x16.txt', (startRow,startCol),(endRow,endCol))
myfile.write('s.add(x_%d_%d_%d_1)\n'%(dropId,sourceRow,sourceCol))
myfile.write('s.add(x_%d_%d_%d_%d)\n'%(dropId,dispenseRow,dispenseCol,T))

#Specific for top-right block
dropId=2
(startRow,startCol) = (1,8)
(endRow,endCol) = (9,16)
(sourceRow,sourceCol) = (1,17)
(dispenseRow,dispenseCol) = (1,16)
varDeclare(T,dropId,(startRow,startCol),(endRow,endCol),(sourceRow,sourceCol))
testDropletClause(T,dropId,(sourceRow,sourceCol),(dispenseRow,dispenseCol), (startRow,startCol),(endRow,endCol))
staticFCforFunctionalDroplets(dropId,'invitro_16x16.txt', (startRow,startCol),(endRow,endCol))
myfile.write('s.add(x_%d_%d_%d_1)\n'%(dropId,sourceRow,sourceCol))
myfile.write('s.add(x_%d_%d_%d_%d)\n'%(dropId,dispenseRow,dispenseCol,T))

#Specific for bottom-left block
dropId=3
(startRow,startCol) = (8,1)
(endRow,endCol) = (16,9)
(sourceRow,sourceCol) = (16,0)
(dispenseRow,dispenseCol) = (16,1)
varDeclare(T,dropId,(startRow,startCol),(endRow,endCol),(sourceRow,sourceCol))
testDropletClause(T,dropId,(sourceRow,sourceCol),(dispenseRow,dispenseCol), (startRow,startCol),(endRow,endCol))
staticFCforFunctionalDroplets(dropId,'invitro_16x16.txt', (startRow,startCol),(endRow,endCol))
myfile.write('s.add(x_%d_%d_%d_1)\n'%(dropId,sourceRow,sourceCol))
myfile.write('s.add(x_%d_%d_%d_%d)\n'%(dropId,dispenseRow,dispenseCol,T))

#Specific for bottom-right block
dropId=4
(startRow,startCol) = (8,8)
(endRow,endCol) = (16,16)
(sourceRow,sourceCol) = (16,17)
(dispenseRow,dispenseCol) = (16,16)
varDeclare(T,dropId,(startRow,startCol),(endRow,endCol),(sourceRow,sourceCol))
testDropletClause(T,dropId,(sourceRow,sourceCol),(dispenseRow,dispenseCol), (startRow,startCol),(endRow,endCol))
staticFCforFunctionalDroplets(dropId,'invitro_16x16.txt', (startRow,startCol),(endRow,endCol))
myfile.write('s.add(x_%d_%d_%d_1)\n'%(dropId,sourceRow,sourceCol))
myfile.write('s.add(x_%d_%d_%d_%d)\n'%(dropId,dispenseRow,dispenseCol,T))

# Interference constraint between dropId = 1,2
staticFCbetweenTestDroplets(T,1,(1,1),(9,9), 2,(1,8),(9,16))
staticFCbetweenTestDroplets(T,3,(8,1),(16,9), 4,(8,8),(16,16))
staticFCbetweenTestDroplets(T,1,(1,1),(9,9), 3,(8,1),(16,9))
staticFCbetweenTestDroplets(T,2,(1,8),(9,16),4,(8,8),(16,16), )

# Edge coverage constraints
edgeCoverage(T,1,(1,3),(1,4))
edgeCoverage(T,1,(1,4),(1,5))
edgeCoverage(T,1,(1,5),(1,6))
edgeCoverage(T,1,(1,6),(1,7))
edgeCoverage(T,1,(1,7),(1,8))
edgeCoverage(T,1,(1,8),(1,9))
edgeCoverage(T,1,(2,2),(2,3))
edgeCoverage(T,1,(2,3),(2,4))
edgeCoverage(T,1,(2,4),(2,5))
edgeCoverage(T,1,(2,5),(2,6))
edgeCoverage(T,1,(2,6),(2,7))
edgeCoverage(T,1,(2,7),(2,8))
edgeCoverage(T,1,(2,8),(2,9))
edgeCoverage(T,1,(3,2),(3,3))
edgeCoverage(T,1,(3,3),(3,4))
edgeCoverage(T,1,(3,8),(3,9))
edgeCoverage(T,1,(4,2),(4,3))
edgeCoverage(T,1,(4,3),(4,4))
edgeCoverage(T,1,(4,6),(4,7))
edgeCoverage(T,1,(4,7),(4,8))
edgeCoverage(T,1,(4,8),(4,9))
edgeCoverage(T,1,(5,1),(5,2))
edgeCoverage(T,1,(5,2),(5,3))
edgeCoverage(T,1,(5,3),(5,4))
edgeCoverage(T,1,(5,4),(5,5))
edgeCoverage(T,1,(5,5),(5,6))
edgeCoverage(T,1,(5,6),(5,7))
edgeCoverage(T,1,(5,7),(5,8))
edgeCoverage(T,1,(5,8),(5,9))
edgeCoverage(T,1,(6,2),(6,3))
edgeCoverage(T,1,(6,3),(6,4))
edgeCoverage(T,1,(6,4),(6,5))
edgeCoverage(T,1,(6,5),(6,6))
edgeCoverage(T,1,(6,8),(6,9))
edgeCoverage(T,1,(7,2),(7,3))
edgeCoverage(T,1,(7,3),(7,4))
edgeCoverage(T,1,(7,4),(7,5))
edgeCoverage(T,1,(7,5),(7,6))
edgeCoverage(T,1,(7,6),(7,7))
edgeCoverage(T,1,(7,7),(7,8))
edgeCoverage(T,1,(7,8),(7,9))
edgeCoverage(T,1,(8,3),(8,4))
edgeCoverage(T,1,(8,4),(8,5))
edgeCoverage(T,1,(8,5),(8,6))
edgeCoverage(T,1,(9,2),(9,3))
edgeCoverage(T,1,(9,3),(9,4))
edgeCoverage(T,1,(9,4),(9,5))
edgeCoverage(T,1,(9,5),(9,6))
edgeCoverage(T,1,(9,6),(9,7))
edgeCoverage(T,1,(9,7),(9,8))
edgeCoverage(T,1,(2,2),(3,2))
edgeCoverage(T,1,(3,2),(4,2))
edgeCoverage(T,1,(4,2),(5,2))
edgeCoverage(T,1,(5,2),(6,2))
edgeCoverage(T,1,(6,2),(7,2))
edgeCoverage(T,1,(1,3),(2,3))
edgeCoverage(T,1,(2,3),(3,3))
edgeCoverage(T,1,(3,3),(4,3))
edgeCoverage(T,1,(4,3),(5,3))
edgeCoverage(T,1,(5,3),(6,3))
edgeCoverage(T,1,(6,3),(7,3))
edgeCoverage(T,1,(7,3),(8,3))
edgeCoverage(T,1,(8,3),(9,3))
edgeCoverage(T,1,(1,4),(2,4))
edgeCoverage(T,1,(2,4),(3,4))
edgeCoverage(T,1,(3,4),(4,4))
edgeCoverage(T,1,(4,4),(5,4))
edgeCoverage(T,1,(5,4),(6,4))
edgeCoverage(T,1,(6,4),(7,4))
edgeCoverage(T,1,(7,4),(8,4))
edgeCoverage(T,1,(8,4),(9,4))
edgeCoverage(T,1,(1,5),(2,5))
edgeCoverage(T,1,(5,5),(6,5))
edgeCoverage(T,1,(6,5),(7,5))
edgeCoverage(T,1,(7,5),(8,5))
edgeCoverage(T,1,(8,5),(9,5))
edgeCoverage(T,1,(1,6),(2,6))
edgeCoverage(T,1,(4,6),(5,6))
edgeCoverage(T,1,(5,6),(6,6))
edgeCoverage(T,1,(6,6),(7,6))
edgeCoverage(T,1,(7,6),(8,6))
edgeCoverage(T,1,(8,6),(9,6))
edgeCoverage(T,1,(1,7),(2,7))
edgeCoverage(T,1,(4,7),(5,7))
edgeCoverage(T,1,(1,8),(2,8))
edgeCoverage(T,1,(2,8),(3,8))
edgeCoverage(T,1,(3,8),(4,8))
edgeCoverage(T,1,(4,8),(5,8))
edgeCoverage(T,1,(5,8),(6,8))
edgeCoverage(T,1,(6,8),(7,8))
edgeCoverage(T,1,(7,8),(8,8))
edgeCoverage(T,1,(8,8),(9,8))
edgeCoverage(T,1,(1,9),(2,9))
edgeCoverage(T,1,(2,9),(3,9))
edgeCoverage(T,1,(3,9),(4,9))
edgeCoverage(T,1,(4,9),(5,9))
edgeCoverage(T,1,(5,9),(6,9))
edgeCoverage(T,1,(6,9),(7,9))


edgeCoverage(T,2,(1,9),(1,10))
edgeCoverage(T,2,(1,10),(1,11))
edgeCoverage(T,2,(1,11),(1,12))
edgeCoverage(T,2,(1,12),(1,13))
edgeCoverage(T,2,(1,13),(1,14))
edgeCoverage(T,2,(1,14),(1,15))
edgeCoverage(T,2,(2,9),(2,10))
edgeCoverage(T,2,(3,9),(3,10))
edgeCoverage(T,2,(4,9),(4,10))
edgeCoverage(T,2,(4,10),(4,11))
edgeCoverage(T,2,(4,11),(4,12))
edgeCoverage(T,2,(5,9),(5,10))
edgeCoverage(T,2,(5,10),(5,11))
edgeCoverage(T,2,(5,11),(5,12))
edgeCoverage(T,2,(5,12),(5,13))
edgeCoverage(T,2,(5,13),(5,14))
edgeCoverage(T,2,(5,14),(5,15))
edgeCoverage(T,2,(5,15),(5,16))
edgeCoverage(T,2,(6,9),(6,10))
edgeCoverage(T,2,(6,10),(6,11))
edgeCoverage(T,2,(6,11),(6,12))
edgeCoverage(T,2,(6,12),(6,13))
edgeCoverage(T,2,(6,15),(6,16))
edgeCoverage(T,2,(7,9),(7,10))
edgeCoverage(T,2,(7,10),(7,11))
edgeCoverage(T,2,(7,11),(7,12))
edgeCoverage(T,2,(7,12),(7,13))
edgeCoverage(T,2,(7,13),(7,14))
edgeCoverage(T,2,(7,14),(7,15))
edgeCoverage(T,2,(7,15),(7,16))
edgeCoverage(T,2,(8,11),(8,12))
edgeCoverage(T,2,(8,15),(8,16))
edgeCoverage(T,2,(9,11),(9,12))
edgeCoverage(T,2,(9,12),(9,13))
edgeCoverage(T,2,(9,13),(9,14))
edgeCoverage(T,2,(9,14),(9,15))
edgeCoverage(T,2,(9,15),(9,16))
edgeCoverage(T,2,(1,9),(2,9))
edgeCoverage(T,2,(2,9),(3,9))
edgeCoverage(T,2,(3,9),(4,9))
edgeCoverage(T,2,(4,9),(5,9))
edgeCoverage(T,2,(5,9),(6,9))
edgeCoverage(T,2,(6,9),(7,9))
edgeCoverage(T,2,(1,10),(2,10))
edgeCoverage(T,2,(2,10),(3,10))
edgeCoverage(T,2,(3,10),(4,10))
edgeCoverage(T,2,(4,10),(5,10))
edgeCoverage(T,2,(5,10),(6,10))
edgeCoverage(T,2,(6,10),(7,10))
edgeCoverage(T,2,(4,11),(5,11))
edgeCoverage(T,2,(5,11),(6,11))
edgeCoverage(T,2,(6,11),(7,11))
edgeCoverage(T,2,(7,11),(8,11))
edgeCoverage(T,2,(8,11),(9,11))
edgeCoverage(T,2,(1,12),(2,12))
edgeCoverage(T,2,(2,12),(3,12))
edgeCoverage(T,2,(3,12),(4,12))
edgeCoverage(T,2,(4,12),(5,12))
edgeCoverage(T,2,(5,12),(6,12))
edgeCoverage(T,2,(6,12),(7,12))
edgeCoverage(T,2,(7,12),(8,12))
edgeCoverage(T,2,(8,12),(9,12))
edgeCoverage(T,2,(5,13),(6,13))
edgeCoverage(T,2,(6,13),(7,13))
edgeCoverage(T,2,(1,15),(2,15))
edgeCoverage(T,2,(2,15),(3,15))
edgeCoverage(T,2,(3,15),(4,15))
edgeCoverage(T,2,(4,15),(5,15))
edgeCoverage(T,2,(5,15),(6,15))
edgeCoverage(T,2,(6,15),(7,15))
edgeCoverage(T,2,(7,15),(8,15))
edgeCoverage(T,2,(8,15),(9,15))
edgeCoverage(T,2,(5,16),(6,16))
edgeCoverage(T,2,(6,16),(7,16))
edgeCoverage(T,2,(7,16),(8,16))
edgeCoverage(T,2,(8,16),(9,16))


edgeCoverage(T,3,(9,2),(9,3))
edgeCoverage(T,3,(9,3),(9,4))
edgeCoverage(T,3,(9,4),(9,5))
edgeCoverage(T,3,(9,5),(9,6))
edgeCoverage(T,3,(9,6),(9,7))
edgeCoverage(T,3,(9,7),(9,8))
edgeCoverage(T,3,(10,4),(10,5))
edgeCoverage(T,3,(10,5),(10,6))
edgeCoverage(T,3,(10,6),(10,7))
edgeCoverage(T,3,(10,7),(10,8))
edgeCoverage(T,3,(10,8),(10,9))
edgeCoverage(T,3,(11,4),(11,5))
edgeCoverage(T,3,(11,5),(11,6))
edgeCoverage(T,3,(11,6),(11,7))
edgeCoverage(T,3,(11,7),(11,8))
edgeCoverage(T,3,(11,8),(11,9))
edgeCoverage(T,3,(12,1),(12,2))
edgeCoverage(T,3,(12,2),(12,3))
edgeCoverage(T,3,(12,3),(12,4))
edgeCoverage(T,3,(12,4),(12,5))
edgeCoverage(T,3,(12,5),(12,6))
edgeCoverage(T,3,(12,6),(12,7))
edgeCoverage(T,3,(12,7),(12,8))
edgeCoverage(T,3,(12,8),(12,9))
edgeCoverage(T,3,(13,3),(13,4))
edgeCoverage(T,3,(13,4),(13,5))
edgeCoverage(T,3,(13,5),(13,6))
edgeCoverage(T,3,(13,8),(13,9))
edgeCoverage(T,3,(14,1),(14,2))
edgeCoverage(T,3,(14,2),(14,3))
edgeCoverage(T,3,(14,3),(14,4))
edgeCoverage(T,3,(14,4),(14,5))
edgeCoverage(T,3,(14,5),(14,6))
edgeCoverage(T,3,(14,6),(14,7))
edgeCoverage(T,3,(14,7),(14,8))
edgeCoverage(T,3,(14,8),(14,9))
edgeCoverage(T,3,(16,4),(16,5))
edgeCoverage(T,3,(16,5),(16,6))
edgeCoverage(T,3,(16,6),(16,7))
edgeCoverage(T,3,(16,7),(16,8))
edgeCoverage(T,3,(16,8),(16,9))
edgeCoverage(T,3,(12,1),(13,1))
edgeCoverage(T,3,(13,1),(14,1))
edgeCoverage(T,3,(9,2),(10,2))
edgeCoverage(T,3,(10,2),(11,2))
edgeCoverage(T,3,(11,2),(12,2))
edgeCoverage(T,3,(12,3),(13,3))
edgeCoverage(T,3,(13,3),(14,3))
edgeCoverage(T,3,(9,4),(10,4))
edgeCoverage(T,3,(10,4),(11,4))
edgeCoverage(T,3,(11,4),(12,4))
edgeCoverage(T,3,(12,4),(13,4))
edgeCoverage(T,3,(13,4),(14,4))
edgeCoverage(T,3,(14,4),(15,4))
edgeCoverage(T,3,(15,4),(16,4))
edgeCoverage(T,3,(9,5),(10,5))
edgeCoverage(T,3,(10,5),(11,5))
edgeCoverage(T,3,(11,5),(12,5))
edgeCoverage(T,3,(12,5),(13,5))
edgeCoverage(T,3,(13,5),(14,5))
edgeCoverage(T,3,(9,6),(10,6))
edgeCoverage(T,3,(10,6),(11,6))
edgeCoverage(T,3,(11,6),(12,6))
edgeCoverage(T,3,(12,6),(13,6))
edgeCoverage(T,3,(13,6),(14,6))
edgeCoverage(T,3,(9,7),(10,7))
edgeCoverage(T,3,(10,7),(11,7))
edgeCoverage(T,3,(11,7),(12,7))
edgeCoverage(T,3,(9,8),(10,8))
edgeCoverage(T,3,(10,8),(11,8))
edgeCoverage(T,3,(11,8),(12,8))
edgeCoverage(T,3,(12,8),(13,8))
edgeCoverage(T,3,(13,8),(14,8))
edgeCoverage(T,3,(10,9),(11,9))
edgeCoverage(T,3,(11,9),(12,9))
edgeCoverage(T,3,(12,9),(13,9))
edgeCoverage(T,3,(13,9),(14,9))


edgeCoverage(T,4,(9,11),(9,12))
edgeCoverage(T,4,(9,12),(9,13))
edgeCoverage(T,4,(9,13),(9,14))
edgeCoverage(T,4,(9,14),(9,15))
edgeCoverage(T,4,(9,15),(9,16))
edgeCoverage(T,4,(10,9),(10,10))
edgeCoverage(T,4,(10,10),(10,11))
edgeCoverage(T,4,(10,11),(10,12))
edgeCoverage(T,4,(10,12),(10,13))
edgeCoverage(T,4,(10,15),(10,16))
edgeCoverage(T,4,(11,9),(11,10))
edgeCoverage(T,4,(11,15),(11,16))
edgeCoverage(T,4,(12,9),(12,10))
edgeCoverage(T,4,(12,10),(12,11))
edgeCoverage(T,4,(12,11),(12,12))
edgeCoverage(T,4,(12,12),(12,13))
edgeCoverage(T,4,(12,13),(12,14))
edgeCoverage(T,4,(12,14),(12,15))
edgeCoverage(T,4,(12,15),(12,16))
edgeCoverage(T,4,(13,11),(13,12))
edgeCoverage(T,4,(13,12),(13,13))
edgeCoverage(T,4,(13,13),(13,14))
edgeCoverage(T,4,(13,14),(13,15))
edgeCoverage(T,4,(14,9),(14,10))
edgeCoverage(T,4,(14,10),(14,11))
edgeCoverage(T,4,(14,11),(14,12))
edgeCoverage(T,4,(14,12),(14,13))
edgeCoverage(T,4,(14,13),(14,14))
edgeCoverage(T,4,(14,14),(14,15))
edgeCoverage(T,4,(14,15),(14,16))
edgeCoverage(T,4,(15,12),(15,13))
edgeCoverage(T,4,(16,9),(16,10))
edgeCoverage(T,4,(16,10),(16,11))
edgeCoverage(T,4,(16,11),(16,12))
edgeCoverage(T,4,(16,12),(16,13))
edgeCoverage(T,4,(10,9),(11,9))
edgeCoverage(T,4,(11,9),(12,9))
edgeCoverage(T,4,(12,9),(13,9))
edgeCoverage(T,4,(13,9),(14,9))
edgeCoverage(T,4,(10,10),(11,10))
edgeCoverage(T,4,(11,10),(12,10))
edgeCoverage(T,4,(9,11),(10,11))
edgeCoverage(T,4,(12,11),(13,11))
edgeCoverage(T,4,(13,11),(14,11))
edgeCoverage(T,4,(9,12),(10,12))
edgeCoverage(T,4,(12,12),(13,12))
edgeCoverage(T,4,(13,12),(14,12))
edgeCoverage(T,4,(14,12),(15,12))
edgeCoverage(T,4,(15,12),(16,12))
edgeCoverage(T,4,(9,13),(10,13))
edgeCoverage(T,4,(10,13),(11,13))
edgeCoverage(T,4,(11,13),(12,13))
edgeCoverage(T,4,(12,13),(13,13))
edgeCoverage(T,4,(13,13),(14,13))
edgeCoverage(T,4,(14,13),(15,13))
edgeCoverage(T,4,(15,13),(16,13))
edgeCoverage(T,4,(12,14),(13,14))
edgeCoverage(T,4,(13,14),(14,14))
edgeCoverage(T,4,(9,15),(10,15))
edgeCoverage(T,4,(10,15),(11,15))
edgeCoverage(T,4,(11,15),(12,15))
edgeCoverage(T,4,(12,15),(13,15))
edgeCoverage(T,4,(13,15),(14,15))
edgeCoverage(T,4,(14,15),(15,15))
edgeCoverage(T,4,(15,15),(16,15))
edgeCoverage(T,4,(9,16),(10,16))
edgeCoverage(T,4,(10,16),(11,16))
edgeCoverage(T,4,(11,16),(12,16))

finish()