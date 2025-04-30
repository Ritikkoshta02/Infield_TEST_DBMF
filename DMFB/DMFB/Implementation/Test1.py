from collections import defaultdict
import subprocess
import time
row, col = 0, 0
DropletMap = []		#To store droplet map
droplet = {}	#key would be tuple of (clock, x, y) and value would be droplet number
locMap = {}		#Key is tuple of (droplet, timestamp) and value is location (x,y)
IntermediateDroplet = []
dropletList = defaultdict(list)#Key is timestamp and value is list of droplet numbers
dropletDispenserDict = {} #To store dropletDispense key is Id and value is location as tuple (x, y)
T = 0
cp = []			#To store the check points
ActiveMixer = []	#To store current mixter in the formate of list [start_time, end_time, x1, y1, x2, y2]
accuracy = 0
TotalDroplet = 0	# To store total Droplet
DispanceList = [] #Will be store in tuple like (timestamp, x, y)
DisappearenceList = []	#Will be store like in tuple like (timestamp, x, y)
outputLocationList = [] # Store output location
extraCPDispense= [] #To store dispense droplet
extraCPDisappernece = [] #To store output/weast time
DispanceTime = []	#To store droplet dispance time
__Id = 1
#========================================================
#Please put it manually for eash test cases
#List of location that are output
#========================================================
def inBetween(t1, t2):
	for t in cp:
		if t > t1 and t < t2:
			return True
	return False
def dis(p1, p2):
	(x1, y1) = p1
	(x2, y2) = p2
	return abs(x1 - x2) + abs(y1 - y2)
def isProximity(p1, p2):
	(x1, y1) = p1
	(x2, y2) = p2
	if abs(x1 - x2) <= 1  and abs(y1 - y2) <= 1:
		return True
	return False
def isProximityAttack(t1, t2):
	global row, col, LocMap, dropletList
	dropt1 = []		#list of droplet which are present at t1 timestamp
	dropt2 = []		#list of droplet which are present at t2 timestamp
	
	dropt1t2 = []	#List of droplets which are present at both timestamp t1, t2
	
	dropt1 = dropletList[t1]
	dropt2 = dropletList[t2]
	
	for d1 in dropt1:
		if d1 in dropt2:
			dropt1t2.append(d1)
	
	ListCP = set()						#Checkpoints in between t1 and t2
	SizeOfCP = 0
	#print("Number of droplets are ", len(dropt1t2))
	#print("Row is : " + str(row))
	for i in range(0, len(dropt1t2) - 1):
		for j in range(i + 1, len(dropt1t2)):
			#print(str(i + j) + "th iteration...")
			d1 = dropt1t2[i]
			d2 = dropt1t2[j]
			(d1x1, d1y1) = locMap[(d1, t1)]		#Location of droplet d1 at timestamp t1
			(d1x2, d1y2) = locMap[(d1, t2)]		#Location of droplet d1 at timestamp t2
			
			(d2x1, d2y1) = locMap[(d2, t1)]		#Location of droplet d2 at timestamp t1
			(d2x2, d2y2) = locMap[(d2, t2)]		#Location of droplet d2 at timestamp t2
			
			#print("Location of droplet d1 at t1 : {}".format(locMap[(d1,t1)]))
			#print("Location of droplet d2 at t1 : {}".format(locMap[(d2,t1)]))
			#print("Location of droplet d1 at t2 : {}".format(locMap[(d1,t2)]))
			#print("Location of droplet d2 at t2 : {}".format(locMap[(d2,t2)]))
			if isPartOfMixing(t1, d1x1, d1y1) and isPartOfMixing(t1, d2x1, d2y1) is True:
				continue
			for t_ in range(t1 + 1, t2):
				#Reduceing the search space
				Locd1 = []
				Locd2 = []
				for x in range(row):
					for y in range(col):
						if (abs(d1x1 - x) + abs(d1y1 - y) <= abs(t1 - t_)) and (abs(d1x2 - x) + abs(d1y2 - y) <= abs(t2 - t_)) is True:
							Locd1.append((x,y))
						if (abs(d2x1 - x) + abs(d2y1 - y) <= abs(t1 - t_)) and (abs(d2x2 - x) + abs(d2y2 - y) <= abs(t2 - t_)) is True:
							Locd2.append((x,y))
				
				for p1 in Locd1:
					for p2 in Locd2:
						#Checking that is golden assay actually perfrom mixing or not\
						#======================================================
						#commenting for conservative checkpoint
						#======================================================
						#if DropletMap[t_][p1[0]][p1[1]] and DropletMap[t_][p2[0]][p2[1]] is True:
						#	continue
						#------------------------------------------------------------
						#If not mixing operation
						e = ((dis(locMap[(d1, t1)], p1) <= abs(t_ - t1)) and (dis(locMap[(d2, t1)], p2) <= abs(t_ - t1)) and isProximity(p1, p2) and (dis(p1, locMap[(d1, t2)]) <= abs(t2 - t_)) and (dis(p2, locMap[(d2, t2)]) <= abs(t2 - t_)))
						if e is True:
							#ListCP.add((t_, p1, p2))
							return True
							SizeOfCP = SizeOfCP + 1
						#-----------------------
	return False
	'''
	if SizeOfCP == 0:
		return -1
	for l in ListCP:
		if l[0] == 2:
			print("t1 and t2 ",t1, t2)
	return ListCP
	'''
				
def isSwapAttack(t1, t2):
	#print("Hello we are cheking for swap attack")
	dropt1 = []		#list of droplet which are present at t1 timestamp
	dropt2 = []		#list of droplet which are present at t2 timestamp
	
	dropt1t2 = []	#List of droplets which are present at both timestamp t1, t2
	
	dropt1 = dropletList[t1]
	dropt2 = dropletList[t2]
	
	for d1 in dropt1:
		if d1 in dropt2:
			dropt1t2.append(d1)
	for i in range(0, len(dropt1t2)):
		for j in range(i + 1, len(dropt1t2)):
			d1 = dropt1t2[i]
			d2 = dropt1t2[j]
			(d1x1, d1y1) = locMap[(d1, t1)]		#Location of droplet d1 at timestamp t1
			(d1x2, d1y2) = locMap[(d1, t2)]		#Location of droplet d1 at timestamp t2
			
			(d2x1, d2y1) = locMap[(d2, t1)]		#Location of droplet d2 at timestamp t1
			(d2x2, d2y2) = locMap[(d2, t2)]		#Location of droplet d2 at timestamp t2
			#Checking if in golden assay droplet d1 and d2 is actually swaping or not
			#if locMap[(d1, t1)] == locMap[(d2, t2)] and locMap[(d2, t1)] == locMap[(d1, t2)]:
			#	continue
			if isPartOfMixing(t1, d1x1, d1y1) and isPartOfMixing(t1, d2x1, d2y1) is True:
				continue
			#If in golden assay droplet d1 and d2 is actually not swaping
			e = ((dis(locMap[(d1, t1)], locMap[(d2, t2)]) <= abs(t1 - t2)) and (dis(locMap[(d1, t2)], locMap[(d2, t1)]) <= abs(t1 - t2)))
			if e is True:
				return True
	return False

def MixerList(tk, s):
	i = 10
	r1 = 0; c1 = 0
	print(tk)
	while tk[i] != ',':
		r1 = r1 * 10 + int(tk[i])
		i = i + 1
	i = i + 1
	while tk[i] != ',':
		c1 = c1 * 10 + int(tk[i])
		i = i + 1
	i = i + 1
	r2=0
	c2=0
	while tk[i] != ',':
		r2 = r2 * 10 + int(tk[i])
		i = i + 1
	i = i + 1
	while tk[i] != ',':
		c2 = c2 * 10 + int(tk[i])
		i = i + 1
	i = i + 1
	c = 0;
	while tk[i] != ')':
		c = c * 10 + int(tk[i])
		i = i + 1
	x1 = r1 - 1
	y1 = c1 - 1
				
	x2 = r2 - 1
	y2 = c2 - 1
	
	if x1 == x2:
		if y1 < y2:
			return [s, s + c, x1, y1, x2, y2, c]
		else:
			return [s, s + c, x1, y2, x2, y1, c]
	else:
		if x1 < x2:
			return [s, s + c, x1, y1, x2, y2, c]
		else:
			return [s, s + c, x2, y1, x1, y2, c]
			
def isPartOfMixing(clock, x, y):
	for tuple in ActiveMixer:
		if tuple[0] <= clock and tuple[1] > clock and tuple[2] <= x and tuple[3] <= y and tuple[4] >= x and tuple[5] >= y:
			return True
	return False
	
def MixingIndex(clock, x, y):
	for tuple in ActiveMixer:
		if tuple[0] <= clock and tuple[1] > clock and tuple[2] <= x and tuple[3] <= y and tuple[4] >= x and tuple[5] >= y:
			return tuple
			
def scan_input(filename):
	global IntermediateDroplet
	global T
	global ActiveMixer
	global DispanceList
	global DisappearenceList
	global TotalDroplet
	global dropletDispenserDict
	global outputLocationList
	global extraCP
	global DispanceTime
	global extraCPDisappernece
	global extraCPDispense
	#We are just scan first time to know value of T
	#TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
	ip_f1 = open(filename,'r')
	#--------------------dimension------------------------------------    
	line = ip_f1.readline()
	while not line.strip():
		line = ip_f1.readline()
               
	token = line.split()
	if token[0] != 'dimension' or len(token) != 3:
		print ('First line should be \'dimension m n\'')
		sys.exit()
    #--------------------accuracy-------------------------------------    
	line = ip_f1.readline()    
	while not line.strip():
		line = ip_f1.readline()         
	token = line.split()
	if token[0] != 'accuracy' or len(token) != 2:
		print ('Second line should be \'accuracy n\'')
		sys.exit()
	#-----------------Build 3D array of droplet map-----------------
	line = ip_f1.readline()
	while not line.strip():
		line = ip_f1.readline()
		
	#line = ip_f.readline()		#Skip one line
	
	while not line.strip():
		line = ip_f1.readline()
	temp_d = 1
	for line in ip_f1:
		token = line.split()
		#If blank space then skip
		if len(token) == 0:
			continue
		temp = 0
		for tk in token:
			if tk.isnumeric():
				temp = int(tk)
				continue
			elif tk[0:3] == 'dis':
				temp_d = temp_d + 1	#New droplet will be use next time
			elif tk[0:3] == 'mix':
				print(tk)
				[s, e, x1, y1, x2, y2, c] = MixerList(tk, temp)
				ActiveMixer.append([s, e, x1, y1, x2, y2])
				if c//6 == 1:		#If mixing is 6 cycle then there are 1 intermediate droplet
					for n in range(1):
						IntermediateDroplet.append(temp_d)
						temp_d = temp_d + 1
				elif c//6 == 2:		#If mixing is 12 cycle then there are 6 intermediate droplet
					for n in range(4):
						IntermediateDroplet.append(temp_d)
						temp_d = temp_d + 1
				elif c//18 == 3:	#If mixing is 18 cycle then there are 7 intermediate droplet
					for n in range(7):
						IntermediateDroplet.append(temp_d)
						temp_d = temp_d + 1
			elif tk[0:3] == 'end':
				T = temp
				break
			else:
				continue
	ip_f1.close()	
	#TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
	print("Active mixers are ")
	for tuple in ActiveMixer:
		print(tuple)
	
	print("Cpital T is : " + str(T))
	
	
	
	#---------------------------------------------------------------
	ip_f = open(filename,'r')
	clock = 0
	
	global row
	global col
	global accuracy
	global DropletMap
	global droplet
	global locMap
	global dropletList
    #--------------------dimension------------------------------------    
	line = ip_f.readline()
	while not line.strip():
		line = ip_f.readline()
               
	token = line.split()
	if token[0] != 'dimension' or len(token) != 3:
		print ('First line should be \'dimension m n\'')
		sys.exit()
	else:
		(row,col)= (int(token[1]),int(token[2]))
	print("Row is : " + str(row) + ", Col is : " + str(col))
    #--------------------accuracy-------------------------------------    
	line = ip_f.readline()    
	while not line.strip():
		line = ip_f.readline()         
	token = line.split()
	if token[0] != 'accuracy' or len(token) != 2:
		print ('Second line should be \'accuracy n\'')
		sys.exit()
	else:  
		accuracy = int(token[1])
	#-----------------Build 3D array of droplet map-----------------
	line = ip_f.readline()
	while not line.strip():
		line = ip_f.readline()
		
	#line = ip_f.readline()		#Skip one line
	
	while not line.strip():
		line = ip_f.readline()
	D = 1						#To assign a number for droplets, After using d ,please do update by 1
	clk = 0						#To track previous timestamp
	DropletMap = [[[0]*col for _ in range(row)] for i in range(T + 1)]
	for line in ip_f:
		
		
		token = line.split()
		i = 1
		#If blank space then skip
		if len(token) == 0:
			continue
		#------ synchronize clock--------
		clock = int(token[0])
		print("Before Clk is : " + str(clk))
		while clk != clock:
			if clk != 0:
				print("Droplets are : ", end="")
				print(dropletList[clk - 1])
				for d_temp in dropletList[clk - 1]:
					(x_temp, y_temp) = locMap[(d_temp, clk - 1)]
					#If at clock of clock - 1 droplet is not part of mixing then we will copy it
					if not isPartOfMixing(clk - 1, x_temp, y_temp):
						#print("Catch---------------" + " Clock " + str(clk) + " " + str(d_temp))
						if d_temp not in dropletList[clk]:
							dropletList[clk].append(d_temp)
						(r_temp, c_temp) = locMap[(d_temp, clk)] = locMap[(d_temp, clk - 1)]
						droplet[(clk, r_temp, c_temp)] = d_temp
					print("Clk is " + str(clk))
			clk = clk + 1
		#--------------------------------
		#Here we substact -1 from row and colum because input fromate is 1 indexing
		old_droplets = []
		
		f = 0
		for tk in token:
			#print(tk)
			if tk.isnumeric():
				clock = int(tk)
				continue
			#print(tk[0:3])
			#---------------------Identify old droplet----------------------
			if f == 0:
				if clock != 0:
					#print("Inter droplet ")
					#print(IntermediateDroplet)
					#DropletMap[clock] = DropletMap[clock - 1]
					if clock == 12:
						print("We are debugging")
						print(dropletList[11])
					for d_temp in dropletList[clock - 1] :
						(x_temp, y_temp) = locMap[(d_temp, clock - 1)]
						#If at clock of clock - 1 droplet is not part of mixing then we will copy it
						if not isPartOfMixing(clock - 1, x_temp, y_temp):
							old_droplets.append(d_temp)
					print("Size is : " + str(len(dropletList[clock - 1])))
				f = 1
				#print(old_droplets)
			#----------------------------------------------------------------
			#print("Size of old_droplets : " + str(len(old_droplets)))
			#print(old_droplets)
			#print("Last dropletList is " + str(clock - 1))
			#print(dropletList[clock - 1])
			'''
			if clock == 20:
				print("We printing all droplet timestamp wise ")
				for i in range(20):
					print("In timestamp t = {} droplets are ", i, end = " " )
					print(dropletList[i])
			'''
			if tk[0:3] == 'dis':
				i = 9
				r = 0; c = 0
				while tk[i] != ',':
					r = r * 10 + int(tk[i])
					i = i + 1
				i = i + 1
				while tk[i] != ')':
					c = c * 10 + int(tk[i])
					i = i + 1
				D_new = D
				D = D + 1
				droplet[(clock, r - 1, c - 1)] = D_new
				locMap[(D_new, clock)] = (r - 1, c - 1)
				if D_new not in dropletList[clock]:
					dropletList[clock].append(D_new)
				DispanceList.append([clock, r, c])
				dropletDispenserDict[D_new] = (r, c)
				if clock not in DispanceTime:
					DispanceTime.append(clock)
				extraCPDispense.append(clock)
				#if clock in dropletList:
				#	dropletList[clock].append(D)
				#else:
				#	dropletList[clock] = list(D)
				
				#print("Clock is hehe dis : " + str(clock))
				#for list in DropletMap[clock]:
				#	print(list)
			elif tk[0:3] == 'mov':
				move = []
				i = 5
				r1 = 0; c1 = 0
				while tk[i] != ',':
					r1 = r1 * 10 + int(tk[i])
					i = i + 1
				i = i + 1
				while tk[i] != ',':
					c1 = c1 * 10 + int(tk[i])
					i = i + 1
				i = i + 1
				r2=0
				c2=0
				while tk[i] != ',':
					r2 = r2 * 10 + int(tk[i])
					i = i + 1
				i = i + 1
				while tk[i] != ')':
					c2 = c2 * 10 + int(tk[i])
					i = i + 1
				#print("Clock is : " + str(clock))
				#print(token)
				#print(droplet[(clock - 1, r1 - 1, c1 - 1)])
				
				temp_droplet = droplet[(clock, r2 - 1, c2 - 1)] = droplet[(clock - 1, r1 - 1, c1 - 1)]
				
				locMap[(temp_droplet, clock)] = (r2 - 1, c2 - 1)
				if temp_droplet not in dropletList[clock]:
					dropletList[clock].append(temp_droplet)
				#If no move is happen so all droplet of previous timestamp should be there
				if temp_droplet in old_droplets:
					old_droplets.remove(temp_droplet)
				#There maybe a case where it need to be delete, if a move operation followed by mix_split operation
				if (clock, r1 - 1, c1 - 1) in droplet:
					droplet.pop((clock, r1 - 1, c1 - 1))
				
			elif tk[0:3] == 'mix':
				i = 10
				r1 = 0; c1 = 0
				while tk[i] != ',':
					r1 = r1 * 10 + int(tk[i])
					i = i + 1
				i = i + 1
				while tk[i] != ',':
					c1 = c1 * 10 + int(tk[i])
					i = i + 1
				i = i + 1
				r2=0
				c2=0
				while tk[i] != ',':
					r2 = r2 * 10 + int(tk[i])
					i = i + 1
				i = i + 1
				while tk[i] != ',':
					c2 = c2 * 10 + int(tk[i])
					i = i + 1
				i = i + 1
				c = 0;
				while tk[i] != ')':
					c = c * 10 + int(tk[i])
					i = i + 1
				x1 = r1 - 1
				y1 = c1 - 1
				
				x2 = r2 - 1
				y2 = c2 - 1
				
				if clock == 17:
					for x in range(row):
						for y in range(col):
							if (clock - 2, x, y) in droplet.keys():
								print(droplet[(clock - 2, x, y)], end=" ")
							else:
								print(0, end=" ")
						print("")
				#Delete old droplet such that it not consider the droplets which are about to mixing
				'''
				#Trying to reserve 4 cell for mixing
				#Copy all droplet thta re not part of mixing
				for d_temp in old_droplets:
					(x_temp, y_temp) = locMap[(d_temp, clock - 1)]
					if not isPartOfMixing(clock - 1, x_temp, y_temp):
						droplet[(clock, x_temp, y_temp)] = d_temp
						locMap[(d_temp, clock)] = (x_temp, y_temp)
						if d_temp not in dropletList[clock]:
							dropletList[clock].append(d_temp)
				
				p = 0
				d1 = droplet[(clock - 1, x1, y1)]
				d2 = droplet[(clock - 1, x2, y2)]
				if r1 == r2:
					if y1 > y2:
						y1, y2 = y2, y1
				else:
					if x1 > x2:
						x1, x2 = x2, x1
				while p != c:
					droplet[(clock + p, x1, y1)] = d1
					locMap[(d1, clock + p)] = (x1, y1)
					droplet[(clock + p, x2, y2)] = d2
					locMap[(d2, clock + p)] = (x2, y2)
					if d1 not in dropletList[clock + p]:
						dropletList[clock + p].append(d1)
					if d2 not in dropletList[clock + p]:
						dropletList[clock + p].append(d2)
					p = p + 1
				'''
				
				#Trying not by reserving cells
				m = c // 6
				l = 1
				#Copy all droplet thta re not part of mixing
				for d_temp in old_droplets:
					(x_temp, y_temp) = locMap[(d_temp, clock - 1)]
					#If at clock of clock - 1 droplet is not part of mixing then we will copy it
					if not isPartOfMixing(clock - 1, x_temp, y_temp) and not isPartOfMixing(clock, x_temp, y_temp):
						droplet[(clock, x_temp, y_temp)] = d_temp
						locMap[(d_temp, clock)] = (x_temp, y_temp)
						dropletList[clock].append(d_temp)
				#Copy ending
				if r1 == r2:
					if y1 > y2:
						y1, y2 = y2, y1
				elif c1 == c2:
					if x1 > x2:
						x1, x2 = x2, x1
				#Step 0: 
				temp_droplet = droplet[(clock, x1, y1)] = droplet[(clock - 1, x1, y1)]
				locMap[(temp_droplet, clock)] = (x1, y1)
				dropletList[clock].append(temp_droplet)
				temp_droplet = droplet[(clock, x2, y2)] = droplet[(clock - 1, x2, y2)]
				locMap[(temp_droplet, clock)] = (x2, y2)
				dropletList[clock].append(temp_droplet)
				while m != 0:
					#code for 6 cycle mixing
					if r1 == r2:	#If mixing size is 4 and vertical then r1 == r2
						if y1 > y2:
							y1, y2 = y2, y1
						#Step 1.1 : Moving left droplet by one cell right
						#DropletMap[clock + l][x1][y1 + 1] = 1
						#DropletMap[clock + l][x1][y1] = 0
						temp_droplet = droplet[(clock + l, x1, y1 + 1)] = droplet[(clock + l - 1, x1, y1)]
						locMap[(temp_droplet, clock + l)] = (x1, y1 + 1)
						dropletList[clock + l].append(temp_droplet)
						#Step 1.2 : Moving right droplet by one cell left
						#DropletMap[clock + l][x2][y2 - 1] = 1
						#DropletMap[clock + l][x2][y2] = 0
						temp_droplet = droplet[(clock + l, x2, y2 - 1)] = droplet[(clock + l - 1, x2, y2)]
						locMap[(temp_droplet, clock + l)] = (x2, y2 - 1)
						dropletList[clock + l].append(temp_droplet)
						
						#Increase timestamp
						l = l + 1
						
						#Step 2 : Right droplet move left and make 2x droplet
						#print("We use " + str(D) + "th droplet")
						d_new = D
						D = D + 1
						#DropletMap[clock + l][x1][y1 + 1] = 2
						droplet[(clock + l, x1, y1 + 1)] = d_new
						locMap[(d_new, clock + l)] = (x1, y1 + 1)
						dropletList[clock + l].append(d_new)
						#DispanceList.append([clock + l, x1, y1 + 1])
						#DisappearenceList.append((clock + l, x1, y1 + 1))
						#DisappearenceList.append((clock + l, x1, y1 + 2))
						#dropletDispenserDict[d_new] = (x1, y1 + 1)
						
						
						#Increase timestamp
						l = l + 1
						
						#Setp 3 : Move 2x droplet by one cell right
						#DropletMap[clock + l][x1][y1 + 2] = 2
						temp_droplet = droplet[(clock + l, x1, y1 + 2)] = droplet[(clock + l - 1, x1, y1 + 1)]
						locMap[(temp_droplet, clock + l)] = (x1, y1 + 2)
						dropletList[clock + l].append(temp_droplet)
						
						#Increase timestamp
						l = l + 1
						
						#Step 4 : Move 2x droplet by one cell left
						#DropletMap[clock + l][x1][y1 + 1] = 2
						temp_droplet = droplet[(clock + l, x1, y1 + 1)] = droplet[(clock + l - 1, x1, y1 + 2)]
						locMap[(temp_droplet, clock + l)] = (x1, y1 + 1)
						dropletList[clock + l].append(temp_droplet)
						
						#Increase timestamp
						l = l + 1
						
						#Step 5.1 : Split 2x droplet and create left droplet
						#print("We use " + str(D) + "th droplet")
						d_new = D
						D = D + 1
						#DropletMap[clock + l][x1][y1 + 1] = 1
						droplet[(clock + l, x1, y1 + 1)] = d_new
						locMap[(d_new, clock + l)] = (x1, y1 + 1)
						dropletList[clock + l].append(d_new)
						#DispanceList.append([clock + l, x1, y1 + 1])
						#DisappearenceList.append((clock + l, x1, y1 + 1))
						#dropletDispenserDict[d_new] = (x1, y1 + 1)
						#Step 5.2 : Split 2x droplet and create right droplet
						#print("We use " + str(D) + "th droplet")
						d_new = D
						D = D + 1
						#DropletMap[clock + l][x1][y1 + 2] = 1
						droplet[(clock + l, x1, y1 + 2)] = d_new
						locMap[(d_new, clock + l)] = (x1, y1 + 2)
						dropletList[clock + l].append(d_new)
						#DispanceList.append([clock + l, x1, y1 + 2])
						#dropletDispenserDict[d_new] = (x1, y1 + 2)
						
						#Increase timestamp
						l = l + 1
						
						#Step 6.1 : Move left droplet by one cell left
						#DropletMap[clock + l][x1][y1] = 1
						
						temp_droplet = droplet[(clock + l, x1, y1)] = droplet[(clock + l - 1, x1, y1 + 1)]
						locMap[(temp_droplet, clock + l)] = (x1, y1)
						dropletList[clock + l].append(temp_droplet)
						#print("HEHE" + " " + str(clock + l) + " " + str(x1) + " " + str(y1) + " and droplet number is = " + str(droplet[(clock + l, x1, y1)]))
						#Step 6.2 : Move right droplet by one cell right
						#DropletMap[clock + l][x1][y1 + 3] = 1
						temp_droplet = droplet[(clock + l, x1, y1 + 3)] = droplet[(clock + l - 1, x1, y1 + 2)]
						locMap[(temp_droplet, clock + l)] = (x1, y1 + 3)
						dropletList[clock + l].append(temp_droplet)
						#print("HEHE" + " " + str(clock + l) + " " + str(x2) + " " + str(y2) + " and droplet number is = " + str(droplet[(clock + l, x2, y2)]))
						#Increase timestamp
						l = l + 1
						
					elif c1 == c2:
						if x1 > x2:
							x1, x2 = x2, x1
						#Step 1.1 : Moving top droplet by one cell down
						#DropletMap[clock + l][x1 + 1][y1] = 1
						#DropletMap[clock + l][x1][y1] = 0
						temp_droplet = droplet[(clock + l, x1 + 1, y1)] = droplet[(clock + l - 1, x1, y1)]
						locMap[(temp_droplet, clock + l)] = (x1 + 1, y1)
						dropletList[clock + l].append(temp_droplet)
						#Step 1.2 : Moving buttom droplet by one cell up
						#DropletMap[clock + l][x2 - 1][y2] = 1
						#DropletMap[clock + l][x2][y2] = 0
						temp_droplet = droplet[(clock + l, x2 - 1, y2)] = droplet[(clock + l - 1, x2, y2)]
						locMap[(temp_droplet, clock + l)] = (x2 - 1, y2)
						dropletList[clock + l].append(temp_droplet)
						
						#Increase timestamp
						l = l + 1
						
						#Step 2 : Buttom droplet move up and make 2x droplet
						#print("We use " + str(D) + "th droplet")
						d_new = D
						D = D + 1
						#DropletMap[clock + l][x1 + 1][y1] = 2
						droplet[(clock + l, x1 + 1, y1)] = d_new
						locMap[(d_new, clock + l)] = (x1 + 1, y1)
						dropletList[clock + l].append(d_new)
						IntermediateDroplet.append(d_new)
						#DispanceList.append([clock + l, x1 + 1, y1])
						#DisappearenceList.append((clock + l, x1 + 1, y1))
						#DisappearenceList.append((clock + l, x1 + 2, y1))
						#dropletDispenserDict[d_new] = (x1 + 1, y1)
						
						#Increase timestamp
						l = l + 1
						
						#Setp 3 : Move 2x droplet by one cell down
						#DropletMap[clock + l][x1 + 2][y1] = 2
						temp_droplet = droplet[(clock + l, x1 + 2, y1)] = droplet[(clock + l - 1, x1 + 1, y1)]
						locMap[(temp_droplet, clock + l)] = (x1 + 2, y1)
						dropletList[clock + l].append(temp_droplet)
						
						#Increase timestamp
						l = l + 1
						
						#Step 4 : Move 2x droplet by one cell up
						#DropletMap[clock + l][x1 + 1][y1] = 2
						temp_droplet = droplet[(clock + l, x1 + 1, y1)] = droplet[(clock + l - 1, x1 + 2, y1)]
						locMap[(temp_droplet, clock + l)] = (x1 + 1, y1)
						dropletList[clock + l].append(temp_droplet)
						
						#Increase timestamp
						l = l + 1
						
						#Step 5.1 : Split 2x droplet and create down droplet
						#print("We use " + str(D) + "th droplet")
						d_new = D
						D = D + 1
						#DropletMap[clock + l][x1 + 1][y1] = 1
						droplet[(clock + l, x1 + 1, y1)] = d_new
						locMap[(d_new, clock + l)] = (x1 + 1, y1)
						dropletList[clock + l].append(d_new)
						#DispanceList.append([clock + l, x1 + 1, y1])
						#DisappearenceList.append((clock + l, x1 + 1, y1))
						#dropletDispenserDict[d_new] = (x1 + 1, y1)
						#Step 5.2 : Split 2x droplet and create top droplet
						#print("We use " + str(D) + "th droplet")
						d_new = D
						D = D + 1
						#DropletMap[clock + l][x1 + 2][y1] = 1
						droplet[(clock + l, x1 + 2, y1)] = d_new
						locMap[(d_new, clock + l)] = (x1 + 2, y1)
						dropletList[clock + l].append(d_new)
						#DispanceList.append([clock + l, x1 + 2, y1])
						#dropletDispenserDict[d_new] = (x1 + 2, y1)
						
						#Increase timestamp
						l = l + 1
						
						#Step 6.1 : Move left droplet by one cell up
						#DropletMap[clock + l][x1][y1] = 1
						temp_droplet = droplet[(clock + l, x1, y1)] = droplet[(clock + l - 1, x1 + 1, y1)]
						locMap[(temp_droplet, clock + l)] = (x1, y1)
						dropletList[clock + l].append(temp_droplet)
						#Step 6.2 : Move right droplet by one cell down
						#DropletMap[clock + l][x1 + 3][y1] = 1
						temp_droplet = droplet[(clock + l, x1 + 3, y1)] = droplet[(clock + l - 1, x1 + 2, y1)]
						locMap[(temp_droplet, clock + l)] = (x1 + 3, y1)
						dropletList[clock + l].append(temp_droplet)
						
						#Increase timestamp
						l = l + 1
					m = m - 1
				
			elif tk[0:3] == 'was':
				i = 6
				r = 0; c = 0
				while tk[i] != ',':
					r = r * 10 + int(tk[i])
					i = i + 1
				i = i + 1
				while tk[i] != ')':
					c = c * 10 + int(tk[i])
					i = i + 1
				#DropletMap[clock][r - 1][c - 1] = 0
				d_temp = droplet[(clock - 1, r - 1, c - 1)]
				old_droplets.remove(d_temp)
				DisappearenceList.append([clock, r, c])
				extraCPDisappernece.append(clock)
				if [r, c] not in outputLocationList:
					outputLocationList.append([r, c])
			elif tk[0:3] == 'out':
				i = 7
				r = 0; c = 0
				while tk[i] != ',':
					r = r * 10 + int(tk[i])
					i = i + 1
				i = i + 1
				while tk[i] != ')':
					c = c * 10 + int(tk[i])
					i = i + 1
				#DropletMap[clock][r - 1][c - 1] = 0
				d_temp = droplet[(clock - 1, r - 1, c - 1)]
				old_droplets.remove(d_temp)
				DisappearenceList.append([clock, r, c])
				extraCPDisappernece.append(clock)
				if [r, c] not in outputLocationList:
					outputLocationList.append([r, c])
			elif tk[0:3] == 'end':
				continue
			else:
				continue
		
		clk = clk + 1
		#print("At clock " + str(clock) + " Golden Map is : ")
		#for temp in arr:
		#	print(temp)
		#print("********************************************")
		#clock = clock + 1
		#print("List of droplets that are old : ")
		#print(old_droplets)
		#print("List of droplets that are present current clock : " + str(clock))
		#print(dropletList[clock])

		if len(old_droplets) != 0:
			#print("Old")
			for d_temp in old_droplets:
				if d_temp not in dropletList[clock]:
					#print("Droplet is : " + str(d_temp))
					if d_temp not in dropletList[clock]:
						dropletList[clock].append(d_temp)
					(r_temp, c_temp) = locMap[(d_temp, clock)] = locMap[(d_temp, clock - 1)]
					droplet[(clock, r_temp, c_temp)] = d_temp
		#print("CLOCK IS " + str(clock))
	#T = clock
	ip_f.close()
	print("*******************Finally done**************************")
	#for i in range(T):
	#	print("In timestamp t = {} droplets are ", i, end = " " )
	#	print(dropletList[i])
	for t in range(T):
		for d_temp in dropletList[t]:
			(x1, y1) = locMap[(d_temp, t)]
			DropletMap[t][x1][y1] = d_temp
		print("At time = ", t)
		for tuple in DropletMap[t]:
			print(tuple)
	TotalDroplet = D - 1

	

def  main():
	global cp
	global outputLocationList
	global T
	global dropletDispenserDict
	global extraCPDisappernece
	global extraCPDispense
	global DispanceTime
	print("Enter File name : ")
	CPType = []
	file = input()
	scan_input(file)
	cf = open('op','w')
	for t in range(T + 1):
		for x in range(1, row + 1):
			for y in range(1, col + 1):
				if DropletMap[t][x - 1][y - 1]:
					cf.write("a_" + str(x) + "_" + str(y) + "_" + str(DropletMap[t][x - 1][y - 1]) + "_" + str(t) +" = True\n")
	cf.close()
	#print(DropletMap)
	dis = 0
	extraCPDispense = [*set(extraCPDispense)]
	extraCPDisappernece = [*set(extraCPDisappernece)]
	start = time.time()
	for t in extraCPDispense:
		cp.append(t)
		dis += 1
	disa = 0
	
	for t in extraCPDisappernece:
		cp.append(t-1)
		disa += 1
	
	mixi = 0
	mixingCP = []
	
	for mix in ActiveMixer:
		cycle = (mix[1] - mix[0]) // 6
		l= 0
		cp.append(mix[0])
		mixingCP.append(mix[0])
		mixi += 1
		while l != cycle:
			cp.append(mix[0] + 2 + l*6)
			cp.append(mix[0] + 3 + l*6)
			cp.append(mix[0] + 4 + l*6)
			cp.append(mix[0] + 6 + l*6)
			mixingCP.append(mix[0] + 2 + l*6)
			mixingCP.append(mix[0] + 3 + l*6)
			mixingCP.append(mix[0] + 4 + l*6)
			mixingCP.append(mix[0] + 6 + l*6)
			mixi += 4
			l = l + 1
	
	mixingCP = [*set(mixingCP)]
	#cp.append(0)
	#cp.append(T)
	print(T)
	print("Checking for proximity attack ")
	SizeOfCPForProximityAttack = 0
	CPForProximityAttack = defaultdict(set)
	rou = 0
	roumix = 0
	vulnerablePair = []
	cp = [*set(cp)]
	cp.sort()
	
	for i in range(0, len(cp) - 1):
		cp1 = cp[i]
		cp2 = cp[i + 1]
		for t1 in range(cp1, cp2 + 1):
			for t2 in range(t1 + 2, cp2 + 1):
				p = isProximityAttack(t1, t2)
				if p:
					vulnerablePair.append((t1, t2))
				else:
					s = isSwapAttack(t1, t2)
					if s:
						vulnerablePair.append((t1, t2))
					
	
	'''
	for t1 in range(0, T + 1):
		for t2 in range(t1 + 2, T + 1):
			p = isProximityAttack(t1, t2)
			if p:
				vulnerablePair.append((t1, t2))
			else:
				s = isSwapAttack(t1, t2)
				if s:
					vulnerablePair.append((t1, t2))
	'''
	'''
	t1 = 0; t2 = 2
	while t1 < T - 1:
		t2 = t1 + 2
		expected_t1 = t1 + 1
		while t2 <= T and t1 + 2 <= t2:
			p = isProximityAttack(t1, t2)
			if p != -1:
				print("t1 = %d, t2 = %d and t' = %d", t1, t2, p[0])
				vulnerablePair.append((t1, t2))
				CPForProximityAttack[p[0]].add(p[1])
				CPForProximityAttack[p[0]].add(p[2])
				#cp.append(t1)
				#cp.append(t2)
				#if p[0] in mixingCP:
				#	roumix.add(p[0])
				#
				#cp.append(p[0])
				#
				#rou.add(p[0])
				CPType.append((t1, t2, p[0]))
				t1 = p[0]
				t2 = t1 + 2
			else:
				t2 = t2 + 1
		t1 = expected_t1
	'''
	'''
	for t1 in range(0,T - 2):
		for t2 in range(t1 + 1, T):
			#print("P For time ",t1, t2)
			p = isProximityAttack(t1,t2)
			if t1 == 31 and t2 == 33:
				for tp in DropletMap[31]:
					print(tp)
				print(p)
				for tp in DropletMap[31]:
					print(tp)
				print(p)
				for tp in DropletMap[31]:
					print(tp)
			if p != -1:
				for ts in p:
					CPForProximityAttack[ts[0]].add(ts[1])
					CPForProximityAttack[ts[0]].add(ts[2])
					cp.append(ts[0])
					#cp.append(t1)
					#cp.append(t2)
	'''
	for _ in range(T):
		for i in CPForProximityAttack[_]:
			SizeOfCPForProximityAttack = SizeOfCPForProximityAttack + 1
	cp.sort()
	cp = [*set(cp)]
	cp.sort()
	print(cp)
	NoOfCPforProximmityAttack = len(cp)
	print("Checking for Swap attack ")
	t1 = 0; t2 = 2
	'''
	while t1 < T - 1:
		t2 = t1 + 2
		expected_t1 = t1 + 1
		while t2 <= T and t1 + 2 <= t2:
			p = isSwapAttack(t1, t2)
			if p != -1:
				print("t1 = %d, t2 = %d and t' = %d", t1, t2)
				vulnerablePair.append((t1, t2))
				
				#if not inBetween(t1, t2):
				#	#cp.append(t1)
				#	#cp.append(t2)
				#	cp.append(t2 - 1)
				#	if p[0] in mixingCP:
				#		roumix.add(p[0])
				#	rou.add(p[0])
				#	CPType.append((t1, t2, t2 - 1))
				
				t1 = t2 - 1
				t2 = t1 + 2
			else:
				t2 = t2 + 1
		t1 = expected_t1
	'''
	'''
	SwapAttack = []
	for t1 in range(0,T - 2):
		for t2 in range(t1 + 1, T):
			#print("S For time ",t1, t2)
			p = isSwapAttack(t1, t2)
			if p != -1:
				if not inBetween(t1, t2):
					SwapAttack.append([t1, t2])
					#cp.append(t1)
					#cp.append(t2)
	SwapAttack.sort(key = lambda x:(x[1], x[0]))
	'''
	vulnerablePair.sort(key=lambda x: (x[1],x[0]))
	Timestamp = []
	end = -1
	sp = 0
	for s, e in vulnerablePair:
		'''
		while sp < len(cp) and cp[sp] <= s:
			end = cp[sp]
			sp += 1
		if sp < len(cp) and s < cp[sp] and cp[sp] < e:
			end = cp[sp]
		'''
		if end <= s:
			Timestamp.append(e - 1)
			end = e - 1
		elif end < e:
			continue
	rou = len(Timestamp)
	for t in Timestamp:
		cp.append(t)
	start = time.time() - start
	CPType = [*set(CPType)]
	CPType.sort()
	print(CPType)
	cp.sort()
	cp = [*set(cp)]
	cp.sort()
	print(vulnerablePair)
	print(cp)
	PA_cp = (NoOfCPforProximmityAttack / len(cp)) * 100
	SA_cp = 100 - PA_cp
	PA_T = (NoOfCPforProximmityAttack / T) * 100
	SA_T = ((len(cp) - NoOfCPforProximmityAttack) / T) * 100
	print("Check point for proximity attack ", PA_cp, " %")
	print("Check point for swap attack ", SA_cp, " %")
	print("Out of " + str(T) + " timestamp, " + str(NoOfCPforProximmityAttack) + " are vulnerable for proximity attack, thats mean " + str(PA_T))
	print("Out of " + str(T) + " timestamp, " + str(len(cp) - NoOfCPforProximmityAttack) + " are vulnerable for swap attack, thats mean " + str(SA_T))
	print("Out of " + str(T) + " timestamp, " + str(T - len(cp)) + " are vulnerable free timestamp, thats mean " + str(((T - len(cp)) / T) * 100))
	print("Optimize ", end=" ")
	print(str(((T - len(cp))/T)*100) + " %")
	print("Number of Checkpoint for dispense " + str(dis))
	print("Number of Checkpoint for mixing " + str(len(mixingCP)))
	print("Number of Checkpoint for disappeance " + str(disa))
	print("Number of Checkpoint for routing " + str(rou))
	print("Number of Checkpoint for overlapping routing and dispense " + str(mixi))
	print("Overall checkpoint " + str(len(cp)))
	print("Total time takes " + str(start) + " sec.")
	print("Size check point of proximity attack " + str(SizeOfCPForProximityAttack))
	NumberOfCellCheck = (SizeOfCPForProximityAttack + (len(cp) - NoOfCPforProximmityAttack) * row * col)
	NumberOfCellCheckPersentageWise = ( NumberOfCellCheck / (row * col * T)) * 100
	print("Optimize if we consider cell wise ", end=" ")
	print(str(100 - NumberOfCellCheckPersentageWise) + " %")
	#========================================================
	#===============Checkpoint verification==================
	#========================================================
	#print(DispanceList)
	#print(DisappearenceList)
	DisappearenceDic = defaultdict(list)
	for tuple in DisappearenceList:
		t = tuple[0]
		x = tuple[1]
		y = tuple[2]
		DisappearenceDic[(x, y)].append(t)
		#if [x, y] not in outputLocationList:
		#	outputLocationList.append([x + 1, y + 1])
	#print(outputLocationList)
	#print(dropletDispenserDict)
	'''
	clauseFile = open('Myclause1.py','w')
	dropletIdList = (1, 2, 3, 4)
	init(clauseFile)
	varDeclare(clauseFile, dropletIdList)
	dropletUniqnessConstraint(clauseFile, dropletIdList)
	cellOccupancyConstraint(clauseFile, dropletIdList)
	
	for d in dropletIdList:
		dropletMovementConstraint(clauseFile, d)
	for d in dropletIdList:
		dropletDisappearenceConstraint(clauseFile, d)
	initialConfiguration(clauseFile, dropletIdList)
	DispanceDic = defaultdict(list)
	for tuple in DispanceList:
		t = tuple[0]
		x = tuple[1]
		y = tuple[2]
		DispanceDic[(x, y)].append(t)
	print("DispanceDic :")
	print(DispanceDic)
	print("DisappearenceDic : ")
	print(DisappearenceDic)
	
	for (x, y) in DispanceDic.keys():
		enforceDropletDispense(clauseFile, (x, y), DispanceDic[(x, y)])
		for t in DispanceDic[(x, y)]:
			d = droplet[(t, x - 1, y - 1)]
			clauseFile.write("s.add(a_"+str(x)+"_"+str(y)+"_"+str(d)+"_"+str(t)+")\n")
			#print("s.add(a_"+str(x)+"_"+str(y)+"_"+str(d)+"_"+str(t)+")\n")
	for (x, y) in DisappearenceDic.keys():
		#print(x, y)
		#print(DisappearenceDic[(x, y)])
		enforceDropletDisappearence(clauseFile, (x, y), DisappearenceDic[(x, y)], dropletIdList)
	print("##############################################")
	for tuple in ActiveMixer:
		st = tuple[0]
		et = tuple[1]
		x1 = tuple[2] + 1
		y1 = tuple[3] + 1
		x2 = tuple[4] + 1
		y2 = tuple[5] + 1
		if x1 == x2:
			if y1 > y2:
				y1, y2 = y2, y1
		else:
			if x1 > x2:
				x1, x2 = x2, x1
		print((x1, y1), (x2, y2), st, et - st)
		enforceMixing(clauseFile, (x1, y1), (x2, y2), st, et - st, dropletIdList)
	proximityAttack(clauseFile, dropletIdList)
	'''
	cf = open('Cp.txt','w')

	
	for t in cp:
		for x in range(1, row + 1):
			for y in range(1, col + 1):
				if DropletMap[t][x - 1][y - 1] != 0:
					cf.write("    insertCheckpoint1X(clauseFile, (" + str(x) + ", " + str(y) + "), " + str(t) + ", dropletIdList)\n")
					'''
					if isPartOfMixing(t, x - 1, y - 1):
						tuple = MixingIndex(t, x - 1, y - 1)
						x1 = tuple[2] + 1
						y1 = tuple[3] + 1
						x2 = tuple[4] + 1
						y2 = tuple[5] + 1
						#insertCheckpoint1X(clauseFile, (x1, y1), t, dropletIdList)
						cf.write("    insertCheckpoint1X(clauseFile, (" + str(x1) + ", " + str(y1) + "), " + str(t) + ", dropletIdList)\n")
						#insertCheckpoint1X(clauseFile, (x2, y2), t, dropletIdList)
						cf.write("    insertCheckpoint1X(clauseFile, (" + str(x2) + ", " + str(y2) + "), " + str(t) + ", dropletIdList)\n")
						if x1 == x2 :
							(r1,c1) = (x1,y1+1)
							(r2,c2) = (x1,y1+2)
						else:
							(r1,c1) = (x1+1,y1)
							(r2,c2) = (x1+2,y2)
						cycle = (t - tuple[0]) % 6
						
						
						#if cycle == 5:
						#	#insertCheckpoint1X(clauseFile, (x1, y1), t, dropletIdList)
						#	cf.write("    insertCheckpoint1X(clauseFile, (" + str(x1) + ", " + str(y1) + "), " + str(t) + ", dropletIdList)\n")
						#	#insertCheckpoint1X(clauseFile, (x2, y2), t, dropletIdList)
						#	cf.write("    insertCheckpoint1X(clauseFile, (" + str(x2) + ", " + str(y2) + "), " + str(t) + ", dropletIdList)\n")
						#else:
						#	#insertCheckpoint1X(clauseFile, (x1, y1), t, dropletIdList)
						#	cf.write("    insertCheckpoint1X(clauseFile, (" + str(r1) + ", " + str(c1) + "), " + str(t) + ", dropletIdList)\n")
						#	#insertCheckpoint1X(clauseFile, (x2, y2), t, dropletIdList)
						#	cf.write("    insertCheckpoint1X(clauseFile, (" + str(r2) + ", " + str(c2) + "), " + str(t) + ", dropletIdList)\n")
						
					else:
						#insertCheckpoint1X(clauseFile, (x, y), t, dropletIdList)
						cf.write("    insertCheckpoint1X(clauseFile, (" + str(x) + ", " + str(y) + "), " + str(t) + ", dropletIdList)\n")
					
				#else:
				#	#insertEmptyCheckpoint(clauseFile,(x, y), t, dropletIdList)
				#	cf.write("    insertEmptyCheckpoint(clauseFile, (" + str(x) + ", " + str(y) + "), " + str(t) + ", dropletIdList)\n")
				'''
	cf.close()
	#finalConfiguration(clauseFile, dropletIdList)
	#finish(clauseFile)
	print("Run clause file")
if __name__ == '__main__':
    main()