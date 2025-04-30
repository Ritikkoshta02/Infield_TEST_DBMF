'''
Created on 04-Jul-2013
@author: sukanta
'''
import sys
import re
import networkx as nx
import subprocess

def V_make_list(size):
    mylist = []
    for i in range(size):
        mylist.append(droplet())
    return mylist

def V_create_matrix(rows, cols):
    matrix = []
    for i in range(rows):
        matrix.append(V_make_list(cols))
    return matrix

class droplet:
    def __init__(self):
        self.id = None      # None implies no droplet
        self.conc = []      # Stores the concentration ratio
        
class mixer:
    def __init__(self,mixer_type,start,end,r1,c1,r2,c2):
        self.mtype = mixer_type # mtype is the type of mixer horizontal(14) = 1 * 4, vertical(41) = 4 * 1
        self.s_time = start     # start time of mixer
        self.e_time = end       # end time of mixer
        self.d1r = r1           # location of first droplet  
        self.d1c = c1
        self.d2r = r2           # location of first droplet  
        self.d2c = c2
    def show(self):
        print ('-----------------mixer----------------------')
        print ('mixer_type = %d'%self.mtype)
        print ('start time = %d end time = %d' %(self.s_time,self.e_time))
        print ('droplet- 1 (%d,%d)'%(self.d1r,self.d1c))
        print ('droplet- 2 (%d,%d)'%(self.d2r,self.d2c))
        print ('---------------------------------------------')

class Biochip_V:
    def __init__(self,r,c,n):
        # Biochip Dimension
        self.row = r
        self.col = c
        # Accuracy value
        self.accuracy = n
        # Different Reserviors
        self.op_reservior = []
        self.ip_reservior = []
        self.waste_reservior = []
        # Current time - Used to keep track clock cycle number
        # time when last verification done
        self.c_time = 0
        # Biochip matrix of droplets
        self.biochip = V_create_matrix(r+2,c+2)
        # mixer_table stores the cuuently active mixers
        self.mixer_table = []
        # __ID is the intermediate droplet ID
        self.__ID = (r+c)  
        # ID of reserviors - it denotes the ratio index of a sample - __RID denotes the sample position in ratio 
        self.__RID = -1     
        # Incrementally generates mixing DAG
        self.mixing_graph = nx.DiGraph()
        
        
    def __get_new_ID(self):
        self.__ID = self.__ID + 1
        return self.__ID
    
    def __get_new_RID(self):
        self.__RID = self.__RID + 1
        return self.__RID
    
    # Checks whether droplet location (x,y) is outside of biochip    
    def __droplet_loc_is_valid(self,x,y):
        if x not in range(1,self.row+1):
            return False
        if y not in range(1,self.col+1):
            return False
    
    # Checks fulidic constraints between two droplets    
    def __FC_between_2_droplets(self,x1,y1,x2,y2):
            if  abs(x1 - x2) >= 2 or abs(y1-y2) >=2:
                return True
            else:
                return False
            
    def verify_set_reagent_reservior(self,reagent_dispenser_list,name):
        if name == None:
            print ('set_reservoir_V - 6: reagent name should be present')
            sys.exit()
        # one RID for each reagent
        RID = self.__get_new_RID()
        #creating graph node for sample, conc can not be set at this time as no of reagents is not yet determined completely          
        self.mixing_graph.add_node(RID,type = 'reagent',sample_name = name,conc=[])
        # Now verify
        for (r,c) in reagent_dispenser_list:
            if self.__droplet_loc_is_valid(r,c) == False :
                print ('set_resevoir_V - 1: Cannot set reservoir at wrong location (%d,%d)\n' %(r,c))
                sys.exit()
        
            # Check whether reservior location is on the biochip boundaries
            if (r not in [1,self.row]) and (c not in [1,self.col]):
                print ('set_resevoir_V - 2: Cannot set reservoir at wrong location (%d,%d)\n' %(r,c))
                sys.exit()
                
            # Check for Fluidic Constraint (FC) violation with other reserviors
            for reservior in self.op_reservior:
                if self.__FC_between_2_droplets(reservior[0],reservior[1],r,c) == False:
                    print ('set_resevoir_V - 4: Fluidic constraint violaton between (%d,%d) and (%d,%d)\n' %(reservior[0],reservior[1],r,c))
                    sys.exit()
            for reservior in self.waste_reservior:
                if self.__FC_between_2_droplets(reservior[0],reservior[1],r,c) == False:
                    print ('set_resevoir_V - 5: Fluidic constraint violaton between (%d,%d) and (%d,%d)\n' %(reservior[0],reservior[1],r,c))
                    sys.exit()                
            for reservior in self.ip_reservior:
                if self.__FC_between_2_droplets(reservior[0],reservior[1],r,c) == False:
                    print ('set_resevior_V - 3: Fluidic constraint violaton between (%d,%d) and (%d,%d)\n' %(reservior[0],reservior[1],r,c))
                    sys.exit()
            self.ip_reservior.append((r,c,'reagent',name,RID))
        
            
    # Put appropriate waste reservoirs at (r,c) with type "reservoir_type" and name for sample only
    def verify_set_resevior(self,r,c,reservior_type):        
        if self.__droplet_loc_is_valid(r,c) == False :
            print ('set_resevior_V - 1: Cannot set reservoir at wrong location (%d,%d)\n' %(r,c))
            sys.exit()
        
        # Check whether reservior location is on the biochip boundaries
        if (r not in [1,self.row]) and (c not in [1,self.col]):
            print ('set_resevior_V - 2: Cannot set reservoir at wrong location (%d,%d)\n' %(r,c))
            sys.exit()
            
        # Check for Fluidic Constraint (FC) violation with other reserviors
        for reservior in self.op_reservior:
            if self.__FC_between_2_droplets(reservior[0],reservior[1],r,c) == False:
                print ('set_resevoir_V - 4: Fluidic constraint violaton between (%d,%d) and (%d,%d)\n' %(reservior[0],reservior[1],r,c))
                sys.exit()
        for reservior in self.waste_reservior:
            if self.__FC_between_2_droplets(reservior[0],reservior[1],r,c) == False:
                print ('set_resevoir_V - 5: Fluidic constraint violaton between (%d,%d) and (%d,%d)\n' %(reservior[0],reservior[1],r,c))
                sys.exit()
        for reservior in self.ip_reservior:
                if self.__FC_between_2_droplets(reservior[0],reservior[1],r,c) == False:
                    print ('set_resevior_V - 3: Fluidic constraint violaton between (%d,%d) and (%d,%d)\n' %(reservior[0],reservior[1],r,c))
                    sys.exit()
           
        # Store reservior location           
        if reservior_type == 'waste_reservoir':             #waste reservior
            ID = self.__get_new_ID()
            self.waste_reservior.append((r,c,'waste',ID))   # register as waste_reservior in biochip
            self.mixing_graph.add_node(ID,type = 'waste')   # add node in graph
            
        elif reservior_type == 'op_reservoir':              #output reservoir
            ID = self.__get_new_ID()
            self.op_reservior.append((r,c,'output',ID))
            self.mixing_graph.add_node(ID,type = 'output')
            #self.curr_reserviors[ID]= ['output']            
        else:
            print ('set_reservior_V - 7: Invalid command' )
            sys.exit()
            
    def verify_dispense_insrt(self, dispense_instr, insrtuction_line):
        # verifying set of dispense(r,c) operation in the current instruction_line
        for instr in dispense_instr:
            #checking for valid reagent dispenser
            flag = 0
            for reagent_dispr in self.ip_reservior:
                if instr == (reagent_dispr[0],reagent_dispr[1]):
                    flag =  1
                    RID = reagent_dispr[4]      # ID of the valid reagent dispensor
                    break
            if flag == 0:       # valid reagent dispensor is not found in biochip
                print ('verify_dispense_insrt - 1: Trying to dispense from invalid input reservoir - %s' %insrtuction_line)
                sys.exit()
            
            # dispenser location is valid now
            # test for presence of droplet at dispense location
            (r,c) = (instr[0], instr[1])
            if self.biochip[r][c].id != None:
                print ('verify_dispense_insrt - 2: Droplet present - can not dispense in (%d,%d) - %s' %(r,c,insrtuction_line))
                sys.exit()
                
            #Setting concentration ratio - self.__RID+1 denotes the no of samples
            reagent_conc = [0]*(self.__RID+1)   
            reagent_conc[RID] = 2**self.accuracy 
            # instantiate droplet with new ID and check FC
            self.biochip[r][c].id = RID
            self.biochip[r][c].conc = reagent_conc[:]
            #Update concentration attribute in Graph node denoting reagent with RID
            self.mixing_graph.nodes[RID]['conc'] = reagent_conc[:]
            if self.check_FC(r, c) == False:
                print ('verify_dispense_insrt - 3: Fluidic constraint violated in dispensing - %s' %insrtuction_line)
                sys.exit()
                
    def verify_mix_split_insrt(self, mix_split_instr, insrtuction_line):
        for instr in mix_split_instr:
            # parameters of a move
            (d1r,d1c,d2r,d2c,mixing_time)= instr
            # verifying droplet source and destination for current locations
            if self.__droplet_loc_is_valid(d1r, d1c) == False or self.__droplet_loc_is_valid(d2r, d2c) == False:
                print ('verify_mix_split_insrt - 1: Invalid droplet location - %s' % insrtuction_line)
                sys.exit()
            if self.droplet_in_active_mixers(d1r, d1c) == True or self.droplet_in_active_mixers(d2r, d2c) == True:
                print ('verify_mix_split_insrt - 2: Droplet is in active mixer - %s' %insrtuction_line)
                sys.exit()
            if self.biochip[d1r][d1c].id == None or self.biochip[d2r][d2c].id == None:
                print ('verify_mix_split_insrt - 3: Droplet is not present - %s' %insrtuction_line)
                sys.exit() 
            if mixing_time % 6 != 0:        #mixing time should be multiple of 6
                print ('verify_mix_split_insrt - 4: Invalid mixing time (mixing time should be multiple of 6) - %s' %insrtuction_line)
                sys.exit()
                    
            # Instantiate mixers - FC need not be checked as starting positions two droplets already ensures the FC of mixer also
            if d1r == d2r and abs(d1c - d2c) == 3:      # 1*4 mixer
                if d1c < d2c:
                    m = mixer(14,self.c_time,self.c_time + mixing_time,d1r,d1c,d2r,d2c)   #instantiate
                else:
                    m = mixer(14,self.c_time,self.c_time + mixing_time,d2r,d2c,d1r,d1c)
                self.mixer_table.append(m)              #register mixer
            elif d1c == d2c and abs(d1r - d2r) == 3:    # 4*1 mixer
                if d1r < d2r:
                    m = mixer(41,self.c_time,self.c_time + mixing_time,d1r,d1c,d2r,d2c) 
                else:
                    m = mixer(41,self.c_time,self.c_time + mixing_time,d2r,d2c,d1r,d1c)
                self.mixer_table.append(m)              #register mixer
            else:
                print ('verify_mix_split_insrt - 5: Mixer cannot be instantiated - %s' %insrtuction_line)
                sys.exit()
                
    def verify_move_instr(self,move_instr,insrtuction_line):
        
        for instr in move_instr:
            (d1r,d1c,d2r,d2c)= instr        # get parameters
            # check valid droplet movenent
            if self.__droplet_loc_is_valid(d1r, d1c) == False or self.__droplet_loc_is_valid(d2r, d2c) == False:
                print ('verify_move_instr - 1: Invalid droplet location - %s' % insrtuction_line)
                sys.exit()
            if self.droplet_in_active_mixers(d1r, d1c) == True:
                print ('verify_move_instr - 2: Droplet (%d,%d) is in active mixer - %s' %(d1r,d1c,insrtuction_line))
                sys.exit()
            if self.biochip[d1r][d1c].id == None:
                print ('verify_move_instr - 3: Droplet (%d,%d) is not present - %s' %(d1r,d1c,insrtuction_line))
                sys.exit() 
            if abs(d1r - d2r) > 1 or abs(d1c - d2c) > 1:
                print ('verify_move_instr - 4: Invalid movement from (%d,%d) -> (%d,%d) - %s' %(d1r,d1c,d2r,d2c,insrtuction_line))
                sys.exit()
            if self.biochip[d2r][d2c].id != None:
                print ('verify_move_instr - 5: cannot move to an occupied location(%d,%d) - %s' %(d2r,d2c,insrtuction_line)   )
                sys.exit()
            if self.droplet_in_active_mixers(d2r, d2c) == True:
                print ('verify_move_instr - 6: Destination (%d,%d) is in active mixer - %s' %(d2r,d2c,insrtuction_line))
                sys.exit()
            
            # save id of D-1
            ID = self.biochip[d1r][d1c].id
            # dummy move
            self.biochip[d1r][d1c].id = None
            self.biochip[d2r][d2c].id = ID
            # check DFC
            if self.check_FC(d2r,d2c) == False:
                print ('verify_move_instr - (D-7): Dynamic fluidic constraint violated - %s'%insrtuction_line)
                sys.exit()
            # reset movement
            self.biochip[d2r][d2c].id = None
            self.biochip[d1r][d1c].id = ID
            
        # check static FC
        for instr in move_instr:
            (d1r,d1c,d2r,d2c)= instr
            
            # original move
            self.biochip[d2r][d2c].id = self.biochip[d1r][d1c].id
            self.biochip[d2r][d2c].conc =  self.biochip[d1r][d1c].conc[:]
            
            self.biochip[d1r][d1c].id = None
            self.biochip[d1r][d1c].conc = []
            
            # check SFC
            if self.check_FC(d2r,d2c) == False:
                print ('verify_move_instr - 8: fluidic constraint violated - %s'%insrtuction_line)
                sys.exit()
                
    # verifying dispense(r,c) operation            
    def verify_waste_insrt(self, waste_instr, insrtuction_line):
        for instr in waste_instr:
            #checking for valid reagent dispenser
            flag = 0
            for waste_dispr in self.waste_reservior:
                if instr == (waste_dispr[0],waste_dispr[1]):
                    flag =  1
                    WID = waste_dispr[3]
            if flag == 0:           # No valid waste dispensior found 
                print ('verify_waste_insrt - 1: Trying to dispense from invalid waste reservoir - %s' %insrtuction_line)
                sys.exit()
            
            # dispenser location is valid now            
            (r,c) = (instr[0], instr[1])
            # check for the presence of waste droplet
            if self.biochip[r][c].id == None:
                print ('verify_waste_insrt - 2: No droplet in (%d,%d) - %s' %(r,c,insrtuction_line))
                sys.exit()            
            
            # add edge to mixing DAG
            self.mixing_graph.add_edge(self.biochip[r][c].id, WID,time = self.c_time)
            # dispense waste - deleting droplet from biochip
            self.biochip[r][c].id = None
            self.biochip[r][c].conc = []
            
    # verifying dispense(r,c) operation
    def verify_op_insrt(self, op_instr, insrtuction_line):
        for instr in op_instr:
            #checking for valid reagent dispenser
            flag = 0
            for op_dispr in self.op_reservior:
                if instr == (op_dispr[0],op_dispr[1]):
                    OPID = op_dispr[3]
                    flag =  1
            if flag == 0:
                print ('verify_op_insrt - 1: Trying to dispense from invalid output reservoir - %s' %insrtuction_line)
                sys.exit()
            
            # dispenser location is valid now            
            (r,c) = (instr[0], instr[1])
            # check for the presence of waste droplet
            if self.biochip[r][c].id == None:
                print ('verify_op_insrt - 2: No droplet in (%d,%d) - %s' %(r,c,insrtuction_line))
                sys.exit()
            
            # add edge to mixing DAG
            self.mixing_graph.add_edge(self.biochip[r][c].id, OPID,time = self.c_time)
            # dispense output - deleting droplet from biochip
            self.biochip[r][c].id = None
            self.biochip[r][c].conc = []            
        
    # verifying the correctness of each instruction line        
    def verify_line(self,line):
        # get operation time
        time = re.compile('\d+').match(line)
        if time == None:
            print ('verify_line - 0: Invalid syntax: ' + line)
            sys.exit()
        
        op_time = int(time.group())     #operation execution time
        if self.c_time > op_time:       # c_time can not be more than op_time
            print ('verify_line - 1: Timing violation in :%s' %line)
            sys.exit()
        
        self.c_time = op_time   # Set current time as operation time
        self.delete_expired_mixers(self.c_time)    #delete all expired mixers upto c_time
        
        #group instructions into different categories
        (dispense_instr, mix_split_instr, move_instr, waste_instr, op_instr) = self.group_instructions(line)
        # verify each operation - order is important
        #----------------------------verifying mix-split operation-----------------------------------------
        self.verify_mix_split_insrt(mix_split_instr,line)                
        #----------------------------verifying move operation----------------------------------------------      
        self.verify_move_instr(move_instr,line)       
        #----------------------------verifying dispense(r,c) operation-------------------------------------        
        self.verify_dispense_insrt(dispense_instr,line)        
        #----------------------------verifying waste operation---------------------------------------------
        self.verify_waste_insrt(waste_instr, line)
        #----------------------------verifying output operation--------------------------------------------
        self.verify_op_insrt(op_instr, line)               
        
        # all operation verified - increment current time
        self.c_time = self.c_time + 1
        return
    
    def droplet_in_active_mixers(self,r,c):
        for mixer in self.mixer_table:
            if (mixer.d1r,mixer.d1c) == (r,c) or (mixer.d2r,mixer.d2c) == (r,c):
                return True
        return False
    
    #Checks violation of FC of droplet (r,c) with other droplets currently present in biochip - mixers are treated as two droplets        
    def check_FC(self,r,c):
        if self.__droplet_loc_is_valid(r,c) == False :
            print ('check_FC - 1: Droplet location (%d,%d) is outside of Biochip\n' %(r,c))
            sys.exit()
                
        for x in range(1,self.row + 1):
            for y in range(1,self.col + 1):
                if self.biochip[x][y].id == None:     # None implies no droplet
                    pass
                elif (x,y) != (r,c):                  # discard droplet at location (r,c)
                    if self.__FC_between_2_droplets(x,y,r,c) == False:  # check for same droplet and violation of FC
                        return False
                else:
                    pass
        return True
    
    # grouping instructions in line into severatl categories                    
    def group_instructions(self,line):
        dispense_instr = []
        mix_split_instr = []
        move_instr = []
        waste_instr = []
        op_instr = []
        
        # separate each instruction
        instr_line = re.compile('[a-z_]+\s*\([\s*\d+\s*,\s*]+\s*\w+\s*\)').findall(line)
        
        for instr in instr_line:
            obj = re.compile('[a-z_]+').match(instr)
            if obj == None:
                print ('group_instruction: Invalid syntax: ' + instr)
                sys.exit() 
            
            # get opcode and operands
            opcode = obj.group()    
            operands = re.compile('(\d+|\w+)').findall(instr[obj.end() + 1 :])
            
            if opcode == 'dispense' and len(operands) == 2:
                r = int(operands[0].strip())
                c = int(operands[1].strip())
                dispense_instr.append((r,c))
            elif opcode == 'mix_split' and len(operands) == 5:
                r1 = int(operands[0].strip())
                c1 = int(operands[1].strip())
                r2 = int(operands[2].strip())
                c2 = int(operands[3].strip())
                t = int(operands[4].strip())
                mix_split_instr.append((r1, c1, r2, c2, t))            
            elif opcode == 'move' and len(operands) == 4:
                rold = int(operands[0].strip())
                cold = int(operands[1].strip())
                rnew = int(operands[2].strip())
                cnew = int(operands[3].strip())
                move_instr.append((rold, cold, rnew, cnew))
            elif opcode == 'waste' and len(operands) == 2:
                r = int(operands[0].strip())
                c = int(operands[1].strip())
                waste_instr.append((r,c))
            elif opcode == 'output' and len(operands) == 2:
                r = int(operands[0].strip())
                c = int(operands[1].strip())
                op_instr.append((r,c))
            elif opcode == 'end':
                pass  
            else:
                print ('group_instruction: Invalid Command:' + instr)
                sys.exit()  
                
        return (dispense_instr, mix_split_instr, move_instr, waste_instr, op_instr)
    
    # create new droplets (change id)  and delete expired mixers and update mixing graph
    def delete_expired_mixers(self,curr_time):
        active_mixers = []
        for m in self.mixer_table:                 
            if curr_time > m.e_time:    # mixer - m is expired
                # get new ID of newly created droplets
                new_id = self.__get_new_ID()
                # new concentration ratio after mixing
                new_conc = self.conc_ratio_after_mixing(self.biochip[m.d1r][m.d1c].conc,self.biochip[m.d2r][m.d2c].conc)
                # add new intermediate node denoting the mix-split step and two edges
                self.mixing_graph.add_node(new_id,type = 'intermediate',conc = new_conc[:],s_time = m.s_time,e_time = m.e_time)
                self.mixing_graph.add_edge(self.biochip[m.d1r][m.d1c].id, new_id)
                self.mixing_graph.add_edge(self.biochip[m.d2r][m.d2c].id, new_id) 
                # create D-1               
                self.biochip[m.d1r][m.d1c].id = new_id
                self.biochip[m.d1r][m.d1c].conc = new_conc[:]
                # create D-2
                self.biochip[m.d2r][m.d2c].id = new_id 
                self.biochip[m.d2r][m.d2c].conc = new_conc[:]  
            else:
                active_mixers.append(m)
        
        # end for
        self.mixer_table = active_mixers
    
    # returns new concentration ratio after mixing
    def conc_ratio_after_mixing(self,l,m):
        if len(l) != len(m):
            print ('conc_ratio_after_mixing: size mismatch')
        res = []
        for i in range(len(l)):
            res.append((l[i]+m[i])/2)
        return res
    
    # generate graphviz layout for current mixing graph    
    def show_mixing_graph(self):
        reagent_node = []
        op_waste_node = []
        fp = open('mg.dot','w')
        string = 'digraph "DD" { \n node [fontsize = 8];\n' 
        fp.write(string)
        for e in self.mixing_graph.edges():
            fp.write(str(e[0])+' -> '+str(e[1])+' [arrowhead = open, arrowsize = .5];\n')
            if self.mixing_graph.nodes[e[1]]['type'] in ['output','waste'] and e[1] not in op_waste_node:
                op_waste_node.append(e[1])
        
        for v in self.mixing_graph.nodes():
            if self.mixing_graph.nodes[v]['type'] not in ['reagent','intermediate','output','waste']:
                print ('show_mixing_graph: Invalid type of node')
                sys.exit()
            
            if self.mixing_graph.nodes[v]['type'] == 'reagent':
                #fp.write('%d [label = "%s\\n %s",  shape = octagon]\n' %(v,self.mixing_graph.node[v]['sample_name'],str(self.mixing_graph.node[v]['conc'])))
                fp.write('%d [label = "%s",  shape = octagon]\n' %(v,self.mixing_graph.nodes[v]['sample_name']))
                reagent_node.append(v)
            elif self.mixing_graph.nodes[v]['type'] == 'intermediate':
                #fp.write('%d [label = "s=%d e=%d\\n%s", shape = oval]\n' %(v,self.mixing_graph.node[v]['s_time'],self.mixing_graph.node[v]['e_time'],str(self.mixing_graph.node[v]['conc'])))
                fp.write('%d [label = "s=%d e=%d", shape = oval]\n' %(v,self.mixing_graph.nodes[v]['s_time'],self.mixing_graph.nodes[v]['e_time']))
            elif self.mixing_graph.nodes[v]['type'] == 'waste' and v in op_waste_node:
                fp.write('%d [label="waste",fontcolor=white,width=.3,shape = invhouse,fontsize = 12, style=filled, fillcolor=black]\n' %v)
                        
            elif self.mixing_graph.nodes[v]['type'] == 'output' and v in op_waste_node:
                fp.write('%d [label="Output",width=.3,shape = invhouse,fontsize = 12, style=filled, fontcolor=white,fillcolor=blue]\n' %v)
                
            else:
                pass                
        
        # reagents are in same level
        fp.write('{ rank = same;')        
        for v in reagent_node:
            fp.write('%d;'%v)
        fp.write('}\n') 
        
        #output and wastes are in same level
        fp.write('{ rank = same;')        
        for v in op_waste_node:
            fp.write('%d;'%v)
        fp.write('}\n') 
        
        fp.write('}\n') #Ending dot file           
        fp.close() 
        subprocess.call(["dot", "-Tpdf", "mg.dot", "-o", "mg.pdf"])         





