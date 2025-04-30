'''
Created on 30 Oct, 2018
@author: sukanta
'''

import subprocess
#from openpyxl.chart.data_source import NumVal
import csv
__Id = 1



# DMFB specification
(numRows, numCols) = (8,15)
dropletDispenserDict = {2:(3,1), 7:(1,5), 10:(1,11), 6:(3,15), 5:(1,14), 1:(1,2), 8:(1,11), 4:(1,8), 3:(1,8), 13:(1,11), 11:(1,11), 12:(1,11), 9:(1,11)}  #Id: dispense locations (x,y)
outputLocationList = [(7,1), (7,15), (8,3), (8,8), (8,13)]


T = 74   #Assay time


def init(clauseFile):
#===============================================================================
# init() appends the initial conditions for the z3 solver to analyze the clauses
# clauseFile is the file descriptor of SAT instance file
#===============================================================================
    clauseFile.write("import sys\n")
    clauseFile.write("import time\n")
    clauseFile.write("sys.path.append(\"/home/sukanta/App/z3-master/build\")\n")
    clauseFile.write("from z3 import *\n")
    clauseFile.write("s = Optimize()\n")
    
def finish(clauseFile):
    clauseFile.write("\n\n")    
    clauseFile.write('start = time.time()\n')
    clauseFile.write("print s.check()\n")
    clauseFile.write("print time.time()-start \n")
    #For printing SAT assignments 
    clauseFile.write("fp = open(\'op\',\'w\')\n")
    clauseFile.write("M = s.model()\n")
    clauseFile.write("for i in M:\n")
    clauseFile.write("    fp.write(str(i) + \" = \" + str(s.model()[i]) + '\\n')\n")    
    
   
    clauseFile.close()
    

def varDeclare(clauseFile, dropletIdList):
#===============================================================================
# dropletIdList is the list of droplet IDs that may appear in the grid  
# T is the assay time -- known from existing synthesis
# (numRows x numCols) is the dimension of biochip
# (1,1) -> top left cell and (numRows, numCols) -> bottom right cell
#===============================================================================
    global numRows, numCols, T, dropletDispenserDict, outputLocationList
    
    for d in dropletIdList:  
        clauseFile.write("#================================================================================================\n") 
        clauseFile.write("# Variables for droplet %d \n"%d) 
        clauseFile.write("#================================================================================================\n") 
        for t in range(0,T+1):
            for x in range(1, numRows+1):
                for y in range(1,numCols+1):
                    clauseFile.write("a_%d_%d_%d_%d = Bool('a_%d_%d_%d_%d')\n"%(x,y,d,t,x,y,d,t))
                    
    #Declare variables for denoting input operations
    for Id in dropletDispenserDict.keys():
        clauseFile.write("#================================================================================================\n") 
        clauseFile.write("# Variables for droplet dispenser (Id =  %d) \n"%Id) 
        clauseFile.write("#================================================================================================\n") 
        (x,y) = dropletDispenserDict[Id]
        for t in range(0,T+1):
            clauseFile.write("ip_%d_%d_%d = Bool('ip_%d_%d_%d')\n"%(x,y,t,x,y,t))
    
    #Declare variables for denoting output operations
    for (x,y) in outputLocationList:
        clauseFile.write("#================================================================================================\n") 
        clauseFile.write("# Variables for droplet output at location (%d,%d) \n"%(x,y)) 
        clauseFile.write("#================================================================================================\n") 
        for t in range(0,T+1):
            clauseFile.write("op_%d_%d_%d = Bool('op_%d_%d_%d')\n"%(x,y,t,x,y,t))
            
    
                    

def dropletUniqnessConstraint(clauseFile, dropletIdList):
#===============================================================================
# each droplet d may occur in at most one cell per time step -- uniqness
#===============================================================================
    global numRows, numCols, T
    
    clauseFile.write("#================================================================================================\n") 
    clauseFile.write("# Droplet uniqness constraint -- at most one instance of a droplet can appear on the grid at any t\n")
    clauseFile.write("#================================================================================================\n") 
    for d in dropletIdList:   
        clauseFile.write("# consistency clauses (uniqueness) for droplet %d \n"%d) 
        for t in range(0,T+1):
            constraint = "s.add(("
            for x in range(1, numRows+1):
                for y in range(1,numCols+1):
                    constraint += "If(a_" + str(x) + "_" + str(y) + "_" + str(d) + "_" + str(t) + " == True, 1, 0) + "
                    
            constraint = constraint[:-3] + ") <= 1)\n"
            clauseFile.write(constraint)
        
                    
                    
def cellOccupancyConstraint(clauseFile, dropletIdList):
#===============================================================================
# each cell can contain only one droplet at any time instant
# This may be relaxed for simulating more sophisticated attacks -- TO DO
#===============================================================================
    global numRows, numCols, T
    
    clauseFile.write("#================================================================================================\n") 
    clauseFile.write("# Cell occupancy constraint -- one cell can contain atmost one droplet at any t\n")
    clauseFile.write("#================================================================================================\n") 
    for t in range(0,T+1):
        clauseFile.write("# consistency clauses (occupancy) at time %d \n"%t)   
        for x in range(1, numRows+1):
            for y in range(1,numCols+1):
                constraint = "s.add(("
                for d in dropletIdList:
                    constraint += "If(a_" + str(x) + "_" + str(y) + "_" + str(d) + "_" + str(t) + " == True, 1, 0) + "
                
                constraint = constraint[:-3] + ") <= 1)\n"
                clauseFile.write(constraint) 
                 
                
def cellInDmfb(row_index, col_index):
    global  numRows, numCols
    
    return ((row_index in range(1,numRows+1)) and (col_index in range(1,numCols+1)))

def fourNeighbour(row_index, col_index):
#================================================================================
# Returns 4-neighbour cells of (row_index,col_index)
# in the biochip of size (numRows x numCols)
#================================================================================
    global numRows, numCols
    
    neighbour = []
    
    if cellInDmfb(row_index, col_index) == False:
        print 'fourNeighbour: Index out of DMFB'
    else:
        if (cellInDmfb(row_index-1, col_index) == True):
            neighbour.append((row_index-1, col_index))
            
        if (cellInDmfb(row_index, col_index-1) == True):
            neighbour.append((row_index, col_index-1))
            
        if (cellInDmfb(row_index, col_index+1) == True):
            neighbour.append((row_index, col_index+1))
            
        if (cellInDmfb(row_index+1, col_index) == True):
            neighbour.append((row_index+1, col_index))
        
    return neighbour 


def eightNeighbour(row_index, col_index):
#================================================================================
# Returns 8-neighbour cells of (row_index,col_index)
# in the biochip of size (numRows x numCols)
#================================================================================
    global numRows, numCols
    
    neighbour = []
    
    if cellInDmfb(row_index, col_index) == False:
        print 'eightNeighbour: Index out of DMFB'
    else:
        if (cellInDmfb(row_index-1, col_index-1) == True):
            neighbour.append((row_index-1, col_index-1))
            
        if (cellInDmfb(row_index-1, col_index) == True):
            neighbour.append((row_index-1, col_index))
            
        if (cellInDmfb(row_index-1, col_index+1) == True):
            neighbour.append((row_index-1, col_index+1))
            
        #----------------------------------------            
        if (cellInDmfb(row_index, col_index-1) == True):
            neighbour.append((row_index, col_index-1))
            
        if (cellInDmfb(row_index, col_index+1) == True):
            neighbour.append((row_index, col_index+1))
        #----------------------------------------
            
        if (cellInDmfb(row_index+1, col_index-1) == True):
            neighbour.append((row_index+1, col_index-1))
            
        if (cellInDmfb(row_index+1, col_index) == True):
            neighbour.append((row_index+1, col_index))
            
        if (cellInDmfb(row_index+1, col_index+1) == True):
            neighbour.append((row_index+1, col_index+1))
        
    return neighbour 
                

def dropletMovementConstraint(clauseFile, dropletId): 
#==================================================================================
# (A droplet on (x,y) at t) IMPLIES (It was already on (x,y) at t-1 OR 
# any of its four neighbour at t-1 OR dispensed from the reservoir at t)  
#==================================================================================    
    global numRows, numCols, dropletDispenserDict
    
    clauseFile.write("#================================================================================================\n") 
    clauseFile.write("# Movement constraint for droplet Id = %d\n"%dropletId)
    clauseFile.write("#================================================================================================\n")  
    for x in range(1, numRows+1):
        for y in range(1, numCols+1):
            (dropletId_x, dropletId_y) = dropletDispenserDict[dropletId]
            fourNeighbourCells = fourNeighbour(x, y)
            for t in range(1, T+1):
                constraint = "s.add(Implies(a_%d_%d_%d_%d, Or(a_%d_%d_%d_%d, "%(x,y,dropletId,t, x,y,dropletId,t-1) 
                # Find dispensor location from dropletId
                
                for (r,c) in fourNeighbourCells:
                    constraint += "a_%d_%d_%d_%d, "%(r,c,dropletId,t-1)
                    
                constraint = constraint[:-2]
                
                if (dropletId_x, dropletId_y) == (x,y):    
                    # A dispenser cell for dropletId exists at the current location and that dispense a droplet at t  
                    constraint += ", ip_%d_%d_%d"%(dropletId_x, dropletId_y,t)
                
                constraint += ")))\n"
                clauseFile.write(constraint)
            clauseFile.write("#---------------------------------------------------------------------------------------\n")
            
            
def dropletDisappearenceConstraint(clauseFile, dropletId): 
#==================================================================================
# A droplet may disappear if it comes to a output reservoir cell 
#==================================================================================    
    global numRows, numCols, outputLocationList, T
    
    clauseFile.write("#================================================================================================\n")  
    clauseFile.write("# Disappearence constraint for droplet Id = %d\n"%dropletId)
    clauseFile.write("#================================================================================================\n") 
    
    for x in range(1, numRows+1):
        for y in range(1, numCols+1):
            for t in range(1, T+1):
                constraint = "s.add(Implies(And(a_%d_%d_%d_%d, Not(a_%d_%d_%d_%d), "%(x,y,dropletId,t-1, x,y,dropletId, t)
                
                fourNeighbourCells = fourNeighbour(x, y)
                for (r,c) in fourNeighbourCells:
                    constraint += "Not(a_%d_%d_%d_%d), "%(r,c,dropletId,t)
                    
                constraint = constraint[:-2] + "), " 
                
                # Check whether the current cell has sink
                if (x,y) in outputLocationList:                
                    constraint +=  "op_%d_%d_%d))\n" %(x,y,t)
                else:
                    constraint += "False))\n"
                    
                clauseFile.write(constraint)
                
                
            clauseFile.write("#--------------------------------------------------------------------------------------\n")
            
            
def insertCheckpoint1X(clauseFile, (x,y), t, dropletIdList): 
#==================================================================================
# A droplet (1X) must appear on (x,y) at t
#==================================================================================    
    if cellInDmfb(x, y) == False:
        print 'insertCheckpoint: cell (%d,%d) is not in DMFB'%(x,y)
        return
    else:
        clauseFile.write("#================================================================================================\n") 
        clauseFile.write("# Checkpoint (1X) on (%d,%d) at %d \n"%(x,y,t))
        clauseFile.write("#================================================================================================\n") 
        
        constraint = "s.add("
        for d in dropletIdList:
            constraint += "If(a_%d_%d_%d_%d == True, 1, 0) + "%(x,y,d,t)
        constraint = constraint[:-2] + "== 1)\n"
        clauseFile.write(constraint)
        

def getNewTempVar():
    # Returns a new temporary variable
    global __Id
    newVar = "t"+str(__Id)
    __Id = __Id + 1
    return newVar
        

def enforceMixing(clauseFile, (x1,y1), (x2,y2), start_t, t_mix, dropletIdList):
#==================================================================================
# A 1x4 or 4x1 mixer (i/o location (x1,y1), (x2,y2)) must instantiate at start_t
# and must run for t_mix cycles
# NOTE: (x1,y1) must be leftmost (topmost) cell for (1x4) ((4x1)) mixer  
#================================================================================== 
    if not ((x1==x2 and abs(y1-y2) == 3) or (y1==y2 and abs(x1-x2) == 3)):
        print "enforceMixing: check mixer specification."
        return
    
    clauseFile.write("#================================================================================================\n") 
    clauseFile.write("# Instantiate mixer [(%d,%d),(%d,%d)] at %d that runs for %d cycles\n"%(x1,y1,x2,y2,start_t,t_mix))
    clauseFile.write("#================================================================================================\n") 
    
    # processing for mixing cell (x1,y1)
    tmpVarList = []
    for d in dropletIdList:
        newTmpVar = getNewTempVar()
        tmpVarList.append(newTmpVar)
        clauseFile.write("%s = Bool('%s')\n"%(newTmpVar,newTmpVar))
        constraint = "s.add(%s == And("%newTmpVar
        for t in range(start_t, start_t+t_mix):
            constraint += "a_%d_%d_%d_%d, "%(x1,y1,d,t)
        constraint = constraint[:-2] + "))\n"
        clauseFile.write(constraint)
        
    # Enforce droplet at (x1,y1)
    constraint = "s.add("
    for var in tmpVarList:
        constraint += "If(%s == True, 1, 0) + "%var
    constraint = constraint[:-2] + " == 1)\n"
    clauseFile.write(constraint)
    clauseFile.write("#-------------------------------------------------------------------------------------------------\n")
    
    # processing for mixing cell (x2,y2)
    tmpVarList = []
    for d in dropletIdList:
        newTmpVar = getNewTempVar()
        tmpVarList.append(newTmpVar)
        clauseFile.write("%s = Bool('%s')\n"%(newTmpVar,newTmpVar))
        constraint = "s.add(%s == And("%newTmpVar
        for t in range(start_t, start_t+t_mix):
            constraint += "a_%d_%d_%d_%d, "%(x2,y2,d,t)
        constraint = constraint[:-2] + "))\n"
        clauseFile.write(constraint)
        
    # Enforce droplet at (x2,y2)
    constraint = "s.add("
    for var in tmpVarList:
        constraint += "If(%s == True, 1, 0) + "%var
    constraint = constraint[:-2] + " == 1)\n"
    clauseFile.write(constraint)
    clauseFile.write("#-------------------------------------------------------------------------------------------------\n")
    
    # For the remaning two cells in the mixer, ensure that no droplet must appear during the mixing period
    
    if (x1==x2 and abs(y1-y2) == 3):
        (r1,c1) = (x1,y1+1)
        (r2,c2) = (x1,y1+2)
    else:
        (r1,c1) = (x1+1,y1)
        (r2,c2) = (x1+2,y2)
        
    # processing for mixing cell (r1,c1) and (r2,c2)
    for t in range(start_t, start_t+t_mix):
        constraint1 = "s.add(And("
        constraint2 = "s.add(And("
        for d in dropletIdList:
            constraint1 += "Not(a_%d_%d_%d_%d), "%(r1,c1,d,t)
            constraint2 += "Not(a_%d_%d_%d_%d), "%(r2,c2,d,t)
        constraint1 = constraint1[:-2] + "))\n"
        constraint2 = constraint2[:-2] + "))\n"
        
        clauseFile.write(constraint1)
        clauseFile.write(constraint2)   

def proximityCondition_at_t(clauseFile, dropletIdList, t):
#==================================================================================
# This function ensures proximity at t
#==================================================================================
    global numRows, numCols

    tmpVarList = []

    clauseFile.write("#-------------------------------------------------------------------------------------------------\n")
    clauseFile.write("# Proximity condition clause at time %d\n"%t)
    clauseFile.write("#-------------------------------------------------------------------------------------------------\n")

    for x in range(1,numRows+1):
        for y in range(1,numCols+1):
            constraint = "s.add(Implies(("
            for d in dropletIdList:
                constraint += "If(a_%d_%d_%d_%d == True, 1, 0) + "%(x,y,d,t)
            constraint = constraint[:-2] + " == 1), And("

            #For RHS
            neighbors_8 = eightNeighbour(x,y)
            for (r,c) in neighbors_8:
                for d in dropletIdList:
                    constraint += "Not(a_%d_%d_%d_%d), "%(r,c,d,t)

            constraint = constraint[:-2] + ")))\n"


            clauseFile.write(constraint)


def proximityCondition(clauseFile, dropletIdList):
#==================================================================================
# This function generates prominity clause for all time
#==================================================================================
    global T
    for t in range(1,T+1):
        proximityCondition_at_t(clauseFile, dropletIdList, t)        
        
        
def proximityAttack_at_t(clauseFile, dropletIdList, t):
#==================================================================================
# This function checks whether a poximity attack is possible at time t
#==================================================================================     
    global numRows, numCols
    
    tmpVarList = []
    
    clauseFile.write("#-------------------------------------------------------------------------------------------------\n")
    clauseFile.write("# Proximity attack clause at time %d\n"%t)
    clauseFile.write("#-------------------------------------------------------------------------------------------------\n")
    
    for x in range(1,numRows+1):
        for y in range(1,numCols+1):
            clauseFile.write("# Proximity attack clause for (%d,%d)\n"%(x,y))
            newTmpVar = getNewTempVar()
            tmpVarList.append(newTmpVar)
            clauseFile.write("%s = Bool('%s')\n"%(newTmpVar,newTmpVar))
            constraint = "s.add(%s == Implies(("%newTmpVar
            for d in dropletIdList:
                constraint += "If(a_%d_%d_%d_%d == True, 1, 0) + "%(x,y,d,t)
            constraint = constraint[:-2] + " == 1), And("
            
            #For RHS
            neighbors_8 = eightNeighbour(x,y)
            for (r,c) in neighbors_8:
                for d in dropletIdList:
                    constraint += "Not(a_%d_%d_%d_%d), "%(r,c,d,t)
            
            constraint = constraint[:-2] + ")))\n"
            
            
            clauseFile.write(constraint)
            
    # Now enforece attack
    clauseFile.write("#-------------------------------Enforce attack---------------------------------------------------\n")
    clauseFile.write("e_%d = Bool('e_%d')\n"%(t,t)) 
    constraint = "s.add(e_%d == Or("%t
    for tmpVar in tmpVarList:
        constraint += "Not(%s), "%tmpVar
    
    constraint = constraint[:-2] + "))\n"
    
    clauseFile.write(constraint)
                
        
def proximityAttack(clauseFile, dropletIdList):
#==================================================================================
# This function generates prominity clause for all time  
#==================================================================================
    global T    
    for t in range(1,T+1):
        proximityAttack_at_t(clauseFile, dropletIdList, t)
    
    constraint = "s.add(Or("
    for t in range(1,T+1):
        constraint += "e_%d, "%t

    constraint = constraint[:-2] + "))\n"

    clauseFile.write(constraint)            
# -------------------------------------------------------------------------------------------------------
#-------------------------------Setup conditions---------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
 
def initialConfiguration(clauseFile, dropletIdList):
#===============================================================================
# No droplet present at t = 0
#===============================================================================
    global numRows, numCols
    
    clauseFile.write("#================================================================================================\n") 
    clauseFile.write("# No droplet should present at time step 0\n")
    clauseFile.write("#================================================================================================\n") 
    
    for Id in dropletIdList:
        constraint = "s.add(And("
        for x in range(1,numRows+1):
            for y in range(1,numCols+1):
                constraint += "Not(a_%d_%d_%d_0), "%(x,y,Id)
        
        constraint = constraint[:-2] + "))\n"
        
        clauseFile.write(constraint)
        
def finalConfiguration(clauseFile, dropletIdList):
#===============================================================================
# No droplet present at t = 0
#===============================================================================
    global numRows, numCols, T
    
    clauseFile.write("#================================================================================================\n") 
    clauseFile.write("# No droplet should present at time step T\n")
    clauseFile.write("#================================================================================================\n") 
    
    for Id in dropletIdList:
        constraint = "s.add(And("
        for x in range(1,numRows+1):
            for y in range(1,numCols+1):
                constraint += "Not(a_%d_%d_%d_%d), "%(x,y,Id,T)
        
        constraint = constraint[:-2] + "))\n"
        
        clauseFile.write(constraint)
        

def enforceDropletDispense(clauseFile, (x, y), t_list):
#========================================================================================
# A droplet is dispensed on location (x,y) at each time t belongs to t_list 
# Note: Also enforce correct droplet Id by adding s.add(a_x_y_d_t)
# d is known from existing synthesis, t belongs to t_list (known from existing synthesis)
#========================================================================================
    global dropletDispenserDict
    
    # Check whether a valid dispenser is available at that location or not
    
    if (x,y) not in dropletDispenserDict.values():
        print "dropletDispense: no dispenser is available to dispense a droplet on (%d,%d)"%(x,y)
        exit()
        
    clauseFile.write("#================================================================================================\n") 
    clauseFile.write("# Droplet dispensing constraint on (%d,%d) at %s\n"%(x,y,str(t_list)))
    clauseFile.write("#================================================================================================\n") 
    
    constraint = "s.add(And("
    
    for t in range(0, T+1):
        if t in t_list:
            constraint += "ip_%d_%d_%d, "%(x,y,t)
        else:
            constraint += "Not(ip_%d_%d_%d), "%(x,y,t)
    
    constraint = constraint[:-2] + "))\n"
    clauseFile.write(constraint)
    

def enforceDropletDisappearence(clauseFile, (x, y), t_list, dropletIdList):
#===============================================================================
# A droplet disappears on location (x,y) at each time t belongs to t_list
# This constraint guarantees droplet disappearance 
#=============================================================================== 
    global T
   
    clauseFile.write("#================================================================================================\n")  
    clauseFile.write("# A droplet on (%d,%d) may go to output at time %s \n"%(x,y,str(t_list))) 
    clauseFile.write("#================================================================================================\n") 
    constraint = "s.add(And("
    for t in range(0,T+1):
        if t in t_list:
            constraint += "op_%d_%d_%d, "%(x,y,t)
        else:
            constraint += "Not(op_%d_%d_%d), "%(x,y,t)
    
    constraint = constraint[:-2] + "))\n"        
    clauseFile.write(constraint)
    
    # Guarantee droplet disappearance
    for t in t_list:
        if t < T:
            tmpVarList = []
            for d in dropletIdList:
                newTmpVar = getNewTempVar()
                tmpVarList.append(newTmpVar)
                clauseFile.write("%s = Bool('%s')\n"%(newTmpVar,newTmpVar))
                constraint = "s.add(%s == And(a_%d_%d_%d_%d, Not(a_%d_%d_%d_%d), "%(newTmpVar, x,y,d,t-1, x,y,d,t)
                fourNeighbourCells = fourNeighbour(x, y)
                for (r,c) in fourNeighbourCells:
                    constraint += "Not(a_%d_%d_%d_%d), "%(r,c,d,t)
                
                constraint = constraint[:-2] + "))\n"
                clauseFile.write(constraint)
    
            constraint = "s.add("
            for var in tmpVarList:
                constraint += "If(%s == True, 1, 0) + "%var
            constraint = constraint[:-2] + " == 1)\n"
            clauseFile.write(constraint)            

         
    
def main():
    global numRows, numCols, T

    clauseFile = open('clause.py','w')
    
    dropletIdList = (1,2,3,4,5,6,7,8,9,10,11,12,13)
    
    init(clauseFile)
    
    varDeclare(clauseFile, dropletIdList)
    dropletUniqnessConstraint(clauseFile, dropletIdList)
    cellOccupancyConstraint(clauseFile, dropletIdList)
    for d in dropletIdList:
        dropletMovementConstraint(clauseFile, d)
        
    for d in dropletIdList:
        dropletDisappearenceConstraint(clauseFile, d)
    
    initialConfiguration(clauseFile, dropletIdList)
    
    enforceDropletDispense(clauseFile, (3,1), [1])
    clauseFile.write("s.add(a_3_1_2_1)\n")
    clauseFile.write("s.add(a_1_5_7_1)\n")
    clauseFile.write("s.add(a_1_11_10_1)\n")
    clauseFile.write("s.add(a_3_15_6_1)\n")
    clauseFile.write("s.add(a_1_14_5_4)\n")
    clauseFile.write("s.add(a_1_2_1_8)\n")
    clauseFile.write("s.add(a_1_11_8_11)\n")
    clauseFile.write("s.add(a_1_8_4_17)\n")
    clauseFile.write("s.add(a_1_8_3_21)\n")
    clauseFile.write("s.add(a_1_11_13_29)\n")
    clauseFile.write("s.add(a_1_11_11_41)\n")
    clauseFile.write("s.add(a_1_11_12_53)\n")
    clauseFile.write("s.add(a_1_11_9_58)\n")
    enforceDropletDispense(clauseFile, (1,5), [1])
    enforceDropletDispense(clauseFile, (1,11), [1,11,29,41,53,58])
    enforceDropletDispense(clauseFile, (1,8), [17,21])
    enforceDropletDispense(clauseFile, (1,2), [8])
    enforceDropletDispense(clauseFile, (3,15), [1])
    enforceDropletDispense(clauseFile, (1,14), [4])
    
    #clauseFile.write("s.add(a_2_6_2_1)\n")
    #Output Swap attacks
    clauseFile.write("sw = Bool('sw')\n")
    clauseFile.write("s.add(sw == Or(Not(a_7_15_5_30), Not(a_7_15_3_51), Not(a_8_13_4_64), Not(a_8_3_2_65), Not(a_8_13_11_67), Not(a_7_15_8_67), Not(a_8_3_10_68), Not(a_8_8_6_69), Not(a_8_3_7_70), Not(a_8_13_1_70), Not(a_8_3_13_72), Not(a_8_8_12_72), Not(a_8_13_9_72)))\n")
 
    enforceMixing(clauseFile, (3,11), (3,14), 6, 6, dropletIdList)
    enforceMixing(clauseFile, (3,2), (3,5), 13, 6, dropletIdList)
    enforceMixing(clauseFile, (3,11), (3,14), 16, 6, dropletIdList)
    enforceMixing(clauseFile, (3,5), (3,8), 19, 6, dropletIdList)
    enforceMixing(clauseFile, (3,11), (6,11), 21, 6, dropletIdList)
    enforceMixing(clauseFile, (3,14), (6,14), 23, 6, dropletIdList)
    #MixSwap aattacks
    clauseFile.write("sm1 = Bool('sm1')\n")
    clauseFile.write("s.add(sm1 == Or(Not(Or(a_3_11_6_6, a_3_11_5_6)), Not(Or(a_3_14_6_6, a_3_14_5_6))))\n")
    clauseFile.write("sm2 = Bool('sm2')\n")
    clauseFile.write("s.add(sm2 == Or(Not(Or(a_3_2_1_13, a_3_2_2_13)), Not(Or(a_3_5_1_13, a_3_5_2_13))))\n")
    clauseFile.write("sm3 = Bool('sm3')\n")
    clauseFile.write("s.add(sm3 == Or(Not(Or(a_3_11_7_16, a_3_11_8_16)), Not(Or(a_3_14_7_16, a_3_14_8_16))))\n")
    clauseFile.write("sm4 = Bool('sm4')\n")
    clauseFile.write("s.add(sm4 == Or(Not(Or(a_3_5_2_19, a_3_5_4_19)), Not(Or(a_3_8_2_19, a_3_8_4_19))))\n")
    clauseFile.write("sm5 = Bool('sm5')\n")
    clauseFile.write("s.add(sm5 == Or(Not(Or(a_3_11_7_21, a_3_11_6_21)), Not(Or(a_6_11_7_21, a_6_11_6_21))))\n")
    clauseFile.write("sm6 = Bool('sm6')\n")
    clauseFile.write("s.add(sm6 == Or(Not(Or(a_3_14_5_23, a_3_14_8_23)), Not(Or(a_6_14_5_23, a_6_14_8_23))))\n")
    
    clauseFile.write("sm7 = Bool('sm7')\n")
    clauseFile.write("s.add(sm7 == Or(Not(Or(a_3_5_7_36, a_3_5_2_36)), Not(Or(a_6_5_7_36, a_6_5_2_36))))\n")
    clauseFile.write("sm8 = Bool('sm8')\n")
    clauseFile.write("s.add(sm8 == Or(Not(Or(a_3_11_1_39, a_3_11_3_39)), Not(Or(a_3_14_1_39, a_3_14_3_39))))\n")
    clauseFile.write("sm9 = Bool('sm9')\n")
    clauseFile.write("s.add(sm9 == Or(Not(Or(a_3_5_13_44, a_3_5_7_44)), Not(Or(a_6_5_13_44, a_6_5_7_44))))\n")
    clauseFile.write("sm10 = Bool('sm10')\n")
    clauseFile.write("s.add(sm10 == Or(Not(Or(a_3_11_1_45, a_3_11_8_45)), Not(Or(a_6_11_1_45, a_6_11_8_45))))\n")
    clauseFile.write("sm11 = Bool('sm11')\n")
    clauseFile.write("s.add(sm11 == Or(Not(Or(a_3_8_6_47, a_3_8_4_47)), Not(Or(a_6_8_6_47, a_6_8_4_47))))\n")
    clauseFile.write("sm12 = Bool('sm12')\n")
    clauseFile.write("s.add(sm12 == Or(Not(Or(a_3_2_2_57, a_3_2_10_57)), Not(Or(a_6_2_2_57, a_6_2_10_57))))\n")
    clauseFile.write("sm13 = Bool('sm13')\n")
    clauseFile.write("s.add(sm13 == Or(Not(Or(a_3_13_11_57, a_3_13_4_57)), Not(Or(a_6_13_11_57, a_6_13_4_57))))\n")
    clauseFile.write("sm14 = Bool('sm14')\n")
    clauseFile.write("s.add(sm14 == Or(Not(Or(a_3_11_1_60, a_3_11_9_60)), Not(Or(a_6_11_1_60, a_6_11_9_60))))\n")
    clauseFile.write("sm15 = Bool('sm15')\n")
    clauseFile.write("s.add(sm15 == Or(Not(Or(a_3_8_12_62, a_3_8_6_62)), Not(Or(a_3_8_12_62, a_3_8_6_62))))\n")
    clauseFile.write("s.add(Or(sm1, sm2, sm3, sm4, sm5, sm6, sm7, sm8, sm9, sm10, sm11, sm12, sm13, sm14, sm15, sw))\n")


    enforceMixing(clauseFile, (3,5), (6,5), 36, 6, dropletIdList)
    enforceMixing(clauseFile, (3,11), (3,14), 39, 6, dropletIdList)
    enforceMixing(clauseFile, (3,5), (6,5), 44, 6, dropletIdList)
    enforceMixing(clauseFile, (3,11), (6,11), 45, 6, dropletIdList)
    enforceMixing(clauseFile, (3,8), (6,8), 47, 6, dropletIdList)
    enforceMixing(clauseFile, (3,2), (6,2), 57, 6, dropletIdList)
    enforceMixing(clauseFile, (3,13), (6,13), 57, 6, dropletIdList)
    enforceMixing(clauseFile, (3,11), (6,11), 60, 6, dropletIdList)
    enforceMixing(clauseFile, (3,8), (6,8), 62, 6, dropletIdList)
 
    enforceDropletDisappearence(clauseFile, (8,3), [66, 69, 71, 73], dropletIdList)
    enforceDropletDisappearence(clauseFile, (8,8), [70, 73], dropletIdList)
    enforceDropletDisappearence(clauseFile, (8,13), [65, 68, 71, 73], dropletIdList)
    enforceDropletDisappearence(clauseFile, (7,15), [31, 52, 68], dropletIdList)
    #enforceDropletDisappearence(clauseFile, (7,1), [71], dropletIdList)
    
    with open('trycplist.txt') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            #x=int(row[0])
            #y=int(row[1])
            #t=int(row[2])
            insertCheckpoint1X(clauseFile, (int(row[0]),int(row[1])), int(row[2]), dropletIdList)

    #insertCheckpoint1X(clauseFile, (1,5), 18, dropletIdList)
    #Output Swap attacks
    #clauseFile.write("sw = Bool('sw')\n")
    #clauseFile.write("s.add(sw == Or(Not(a_9_6_4_30), Not(a_1_3_5_32), Not(a_1_6_6_32), Not(a_1_3_1_38), Not(a_1_6_2_38), Not(a_9_6_3_38)))\n")
    
    #MixSwap aattacks
    #clauseFile.write("sm1 = Bool('sm1')\n")
    #clauseFile.write("s.add(sm1 == Or(Not(Or(a_5_3_1_12, a_8_3_1_12)), Not(Or(a_5_3_3_12, a_8_3_3_12))))\n") 
    #clauseFile.write("sm2 = Bool('sm2')\n")
    #clauseFile.write("s.add(sm2 == Or(Not(Or(a_5_6_2_12, a_8_6_2_12)), Not(Or(a_5_6_4_12, a_8_6_4_12))))\n")
    #clauseFile.write("sm3 = Bool('sm3')\n")
    #clauseFile.write("s.add(sm3 == Or(Not(Or(a_8_3_3_22, a_8_6_3_22)), Not(Or(a_8_3_4_22, a_8_6_4_22))))\n")
    #clauseFile.write("sm4 = Bool('sm4')\n")
    #clauseFile.write("s.add(sm4 == Or(Not(Or(a_5_3_1_23, a_2_3_1_23)), Not(Or(a_5_3_5_23, a_2_3_5_23))))\n")
    #clauseFile.write("sm5 = Bool('sm5')\n")
    #clauseFile.write("s.add(sm5 == Or(Not(Or(a_5_6_2_23, a_2_6_2_23)), Not(Or(a_5_6_6_23, a_2_6_6_23))))\n")  
    #clauseFile.write("s.add(Or(sm1, sm2, sm3, sm4, sm5, sw))\n")
    #for t in range(0,T+1):
    proximityAttack(clauseFile, dropletIdList)
    #constraint = "s.add(Or(Not(a_3_1_1_1), Not(a_3_5_2_1), Not(a_3_1_1_2), Not(a_3_4_2_2), Not(a_4_1_1_6), Not(a_3_3_2_6), Not(a_5_1_1_7), Not(a_3_2_2_7), Not(a_3_5_3_7)"
    #constraint += "Not(a_5_1_1_8), Not(a_5_1_1_9), Not(a_5_1_1_10), Not(a_5_1_1_11), Not(a_5_1_1_11), Not(a_5_1_1_12), Not(a_5_1_1_13), Not(a_5_1_1_14), Not(a_5_1_1_15), Not(a_5_1_1_16), Not(a_5_1_1_17), Not(a_5_1_1_18), Not(a_5_1_1_19), Not(a_5_1_1_20), Not(a_5_2_1_21), Not(a_5_2_1_22), Not(a_5_2_1_23), Not(a_5_2_1_24), Not(a_5_2_1_25), Not(a_5_2_1_26), Not(a_2_2_2_11), Not(a_1_2_2_12), Not(a_3_4_3_11), Not(a_3_3_3_12), Not(a_1_1_2_13), Not(a_1_1_2_14), Not(a_1_1_2_15), Not(a_2_1_2_17), Not(a_3_2_3_13), Not(a_5_1_4_13), Not(a_3_3_3_17), Not(a_2_5_4_17), "
    #constraint += "Not(a_3_1_2_18), Not(a_3_4_3_18), Not(a_1_5_4_18), Not(a_3_1_2_19), Not(a_3_5_3_19), Not(a_1_4_4_19), Not(a_2_1_2_20), Not(a_2_5_3_20), Not(a_1_3_4_20),"
    #constraint += "Not(a_2_2_2_21), Not(a_2_5_3_21), Not(a_3_2_2_25), Not(a_1_5_3_25), Not(a_3_3_2_26), Not(a_1_4_3_26), Not(a_1_3_3_27), Not(a_4_2_1_27), Not(a_3_4_2_27),"
    #constraint += "Not(a_3_2_1_28), Not(a_3_5_2_28), Not(a_2_2_1_29), Not(a_2_5_2_29), Not(a_3_2_1_33), Not(a_2_4_2_33), Not(a_4_2_1_34), Not(a_1_4_2_34), Not(a_5_2_1_35), Not(a_1_3_2_35), Not(a_5_3_1_36)))\n"
    #clauseFile.write(constraint)


    finalConfiguration(clauseFile, dropletIdList)
    finish(clauseFile)                    
                    
if __name__ == "__main__":
    main()  
    
    subprocess.call(["python","clause.py"])                  
    
