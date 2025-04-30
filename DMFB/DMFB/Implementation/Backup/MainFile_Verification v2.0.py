from collections import defaultdict
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

def isProximityAttack(t1, t2):
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
		for j in range(i + 2, len(dropt1t2)):
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
						#Checking that is golden assay actually perfrom mixing or not
						if DropletMap[t_][p1[0]][p1[1]] and DropletMap[t_][p2[0]][p2[1]] is True:
							continue
						#------------------------------------------------------------
						#If not mixing operation
						e = ((dis(locMap[(d1, t1)], p1) <= abs(t_ - t1)) and (dis(locMap[(d2, t1)], p2) <= abs(t_ - t1)) and (dis(p1, p2) <= 2) and (dis(p1, locMap[(d1, t2)]) <= abs(t2 - t_)) and (dis(p2, locMap[(d2, t2)]) <= abs(t2 - t_)))
						if e is True:
							ListCP.add((t_, p1, p2))
							SizeOfCP = SizeOfCP + 1
						#-----------------------
	if SizeOfCP == 0:
		return -1
	return ListCP
				
def isSwapAttack(t1, t2):
	#print("Hello we are cheking for swap attack")
	dropt1 = []		#list of droplet which are present at t1 timestamp
	dropt2 = []		#list of droplet which are present at t2 timestamp
	
	dropt1t2 = []	#List of droplets which are present at both timestamp t1, t2
	
	dropt1 = dropletList[t1]
	dropt2 = dropletList[t2]
	#print("Droplets at timestamp t1 : ")
	#print(dropt1)
	#print("Droplets at timestamp t2 : ")
	#print(dropt2)
	for d1 in dropt1:
		if d1 in dropt2:
			dropt1t2.append(d1)
	for i in range(0, len(dropt1t2)):
		for j in range(i + 2, len(dropt1t2)):
			d1 = dropt1t2[i]
			d2 = dropt1t2[j]
			#Checking if in golden assay droplet d1 and d2 is actually swaping or not
			if locMap[(d1, t1)] == locMap[(d2, t2)] and locMap[(d2, t1)] == locMap[(d1, t2)]:
				continue
			#If in golden assay droplet d1 and d2 is actually not swaping
			e = ((dis(locMap[(d1, t1)], locMap[(d2, t2)]) - dis(locMap[(d1, t2)], locMap[(d2, t1)])) <= (abs(t1 - t2)))
			if e is True:
				return 0
	return -1

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
def scan_input(filename):
	global IntermediateDroplet
	global T
	global ActiveMixer
	global DispanceList
	global DisappearenceList
	global TotalDroplet
	global dropletDispenserDict
	global outputLocationList
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
		#print("Before Clk is : " + str(clk))
		while clk != clock:
			if clk != 0:
				for d_temp in dropletList[clk - 1]:
					(x_temp, y_temp) = locMap[(d_temp, clk - 1)]
					if not isPartOfMixing(clk - 1, x_temp, y_temp):
						#print("Catch---------------" + " Clock " + str(clk) + " " + str(d_temp))
						dropletList[clk].append(d_temp)
						(r_temp, c_temp) = locMap[(d_temp, clk)] = locMap[(d_temp, clk - 1)]
						droplet[(clk, r_temp, c_temp)] = d_temp
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
			#---------------------Indetify old droplet----------------------
			if f == 0:
				if clock != 0:
					#print("Inter droplet ")
					#print(IntermediateDroplet)
					#DropletMap[clock] = DropletMap[clock - 1]
					for d_temp in dropletList[clock - 1] :
						(x_temp, y_temp) = locMap[(d_temp, clock - 1)]
						if not isPartOfMixing(clock - 1, x_temp, y_temp):
							old_droplets.append(d_temp)
					#print("Size is : " + str(len(dropletList[clock - 1])))
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
				dropletList[clock].append(D_new)
				DispanceList.append([clock, r - 1, c - 1])
				dropletDispenserDict[D_new] = (r - 1, c - 1)
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
				
				
				#Delete old droplet such that it not consider the droplets which are about to mixing
				
				#Trying to reserve 4 cell for mixing
				"""
				p = 0
				while p != c - 1:
					#If mixing size is 4 and vertical then r1 == r2
					if r1 == r2:
						l = 0
						while l != 4:
							DropletMap[clock + p][r1 - 1][c1 - 1 + l] = 1
							droplet[(clock + p, r1 - 1, c1 - 1 + l)] = D
							locMap[(D, clock + p)] = (r1 - 1, c1 - 1 + l)
							l = l + 1
					#If mixing size is 4 and horizental then c1 == c2
					else:
						l = 0
						while l != 4:
							DropletMap[clock + p][r1 - 1 + l][c1 - 1] = 1
							droplet[(clock + p, r1 - 1 + l, c1 - 1)] = D
							locMap[(D, clock + p)] = (r1 - 1 + l, c1 - 1)
							l = l + 1
					dropletList[clock + p].append(D)
					p = p + 1
				D = D + 1
				if r1 == r2:
					DropletMap[clock + p][r1 - 1][c1 - 1] = 1
					DropletMap[clock + p][r2 - 1][c2 - 1] = 1
					droplet[(clock + p, r1 - 1, c1 - 1)] = D
					locMap[(D, clock + p)] = (r1 - 1, c1 - 1)
					dropletList[clock + p].append(D)
					D = D + 1
					droplet[(clock + p, r2 - 1, c2 - 1)] = D
					locMap[(D, clock + p)] = (r2 - 1, c2 - 1)
					dropletList[clock + p].append(D)
					D = D + 1
				else:
					DropletMap[clock + p][r1 - 1][c1 - 1] = 1
					DropletMap[clock + p][r2 - 1][c2 - 1] = 1
					droplet[(clock + p, r1 - 1, c1 - 1)] = D
					locMap[(D, clock + p)] = (r1 - 1, c1 - 1)
					dropletList[clock + p].append(D)
					D = D + 1
					droplet[(clock + p, r2 - 1, c2 - 1)] = D
					locMap[(D, clock + p)] = (r2 - 1, c2 - 1)
					dropletList[clock + p].append(D)
					D = D + 1
				"""
				
				#Trying not by reserving cells
				m = c // 6
				l = 1
				#Copy all droplet thta re not part of mixing
				for d_temp in old_droplets:
					(x_temp, y_temp) = locMap[(d_temp, clock - 1)]
					if not isPartOfMixing(clock - 1, x_temp, y_temp):
						droplet[clock, x_temp, y_temp] = d_temp
						locMap[(d_temp, clock)] = (x_temp, y_temp)
						dropletList[clock].append(d_temp)
				#Copy ending
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
						DispanceList.append([clock + l, x1, y1 + 1])
						DisappearenceList.append((clock + l, x1, y1 + 1))
						DisappearenceList.append((clock + l, x1, y1 + 2))
						dropletDispenserDict[d_new] = (x1, y1 + 1)
						
						
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
						DispanceList.append([clock + l, x1, y1 + 1])
						DisappearenceList.append((clock + l, x1, y1 + 1))
						dropletDispenserDict[d_new] = (x1, y1 + 1)
						#Step 5.2 : Split 2x droplet and create right droplet
						#print("We use " + str(D) + "th droplet")
						d_new = D
						D = D + 1
						#DropletMap[clock + l][x1][y1 + 2] = 1
						droplet[(clock + l, x1, y1 + 2)] = d_new
						locMap[(d_new, clock + l)] = (x1, y1 + 2)
						dropletList[clock + l].append(d_new)
						DispanceList.append([clock + l, x1, y1 + 2])
						dropletDispenserDict[d_new] = (x1, y1 + 2)
						
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
						DispanceList.append([clock + l, x1 + 1, y1])
						DisappearenceList.append((clock + l, x1 + 1, y1))
						DisappearenceList.append((clock + l, x1 + 2, y1))
						dropletDispenserDict[d_new] = (x1 + 1, y1)
						
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
						DispanceList.append([clock + l, x1 + 1, y1])
						DisappearenceList.append((clock + l, x1 + 1, y1))
						dropletDispenserDict[d_new] = (x1 + 1, y1)
						#Step 5.2 : Split 2x droplet and create top droplet
						#print("We use " + str(D) + "th droplet")
						d_new = D
						D = D + 1
						#DropletMap[clock + l][x1 + 2][y1] = 1
						droplet[(clock + l, x1 + 2, y1)] = d_new
						locMap[(d_new, clock + l)] = (x1 + 2, y1)
						dropletList[clock + l].append(d_new)
						DispanceList.append([clock + l, x1 + 2, y1])
						dropletDispenserDict[d_new] = (x1 + 2, y1)
						
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
				DisappearenceList.append((clock, r1 - 1, c1 - 1))
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
				DisappearenceList.append((clock, r1 - 1, c1 - 1))
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
	clauseFile.write("print(s.check())\n")
	clauseFile.write("print(time.time()-start) \n")
	#For printing SAT assignments 
	clauseFile.write("fp = open(\'op\',\'w\')\n")
	clauseFile.write("M = s.model()\n")
	clauseFile.write("for i in M:\n")
	clauseFile.write("    fp.write(str(i) + \" = \" + str(s.model()[i]) + '\\n')\n")    


	clauseFile.close()
    


def varDeclare(clauseFile):
#===============================================================================
# dropletIdList is the list of droplet IDs that may appear in the grid  
# T is the assay time -- known from existing synthesis
# (numRows x numCols) is the dimension of biochip
# (1,1) -> top left cell and (numRows, numCols) -> bottom right cell
#===============================================================================
	global row, col, T, TotalDroplet, DispanceList, DisappearenceList
	
	for d in range(1, TotalDroplet + 1):   
		clauseFile.write("# Variables for droplet %d \n"%d)
		for t in range(0, T + 1):
			for x in range(1, row + 1):
				for y in range(1, col + 1):
					clauseFile.write("a_%d_%d_%d_%d = Bool('a_%d_%d_%d_%d')\n"%(x,y,d,t,x,y,d,t))
	
	#Declare variables for denoting input operations
	for tuple in DispanceList:
		#clauseFile.write("# Variables for droplet dispenser (Id =  %d) \n"%Id)
		x = tuple[1] + 1		#We are convertine 0 index to 1 index
		y = tuple[2] + 1
		for t in range(0, T + 1):
			clauseFile.write("ip_%d_%d_%d = Bool('ip_%d_%d_%d')\n"%(x,y,t,x,y,t))

	#Declare variables for denoting output operations
	for tuple in DisappearenceList:
		x = tuple[1] + 1
		y = tuple[2] + 1
		clauseFile.write("# Variables for droplet output at location (%d,%d) \n"%(x,y)) 
		for t in range(0, T + 1):
			clauseFile.write("op_%d_%d_%d = Bool('op_%d_%d_%d')\n"%(x,y,t,x,y,t))


def dropletUniqnessConstraint(clauseFile):
#===============================================================================
# each droplet d may occur in at most one cell per time step -- uniqness
#===============================================================================
	global row, col, T, TotalDroplet
    
	clauseFile.write("# ------------------------------------------------------------------------------------------------\n") 
	clauseFile.write("# Droplet uniqness constraint -- at most one instance of a droplet can appear on the grid at any t\n")
	clauseFile.write("# ------------------------------------------------------------------------------------------------\n") 
	for d in range(1, TotalDroplet + 1):   
		clauseFile.write("# consistency clauses (uniqueness) for droplet %d \n"%d) 
		for t in range(0, T + 1):
			constraint = "s.add(("
			for x in range(1, row + 1):
				for y in range(1, col +1 ):
					constraint += "If(a_" + str(x) + "_" + str(y) + "_" + str(d) + "_" + str(t) + " == True, 1, 0) + "
                    
			constraint = constraint[:-3] + ") <= 1)\n"
			clauseFile.write(constraint)


      
def cellOccupancyConstraint(clauseFile):
#===============================================================================
# each cell can contain only one droplet at any time instant
# This may be relaxed for simulating more sophisticated attacks -- TO DO
#===============================================================================
	global row, col, T
	
	clauseFile.write("# -----------------------------------------------------------------------------\n") 
	clauseFile.write("# Cell occupancy constraint -- one cell can contain atmost one droplet at any t\n")
	clauseFile.write("# -----------------------------------------------------------------------------\n") 
	for t in range(0, T + 1):
		clauseFile.write("# consistency clauses (occupancy) at time %d \n"%t)   
		for x in range(1, row + 1):
			for y in range(1, col + 1):
				constraint = "s.add(("
				for d in range(1, TotalDroplet + 1):
					constraint += "If(a_" + str(x) + "_" + str(y) + "_" + str(d) + "_" + str(t) + " == True, 1, 0) + "
                
				constraint = constraint[:-3] + ") <= 1)\n"
				clauseFile.write(constraint) 



def cellInDmfb(row_index, col_index):
	global  row, col
	
	return ((row_index in range(1, row + 1)) and (col_index in range(1, col + 1)))

def fourNeighbour(row_index, col_index):
#================================================================================
# Returns 4-neighbour cells of (row_index,col_index)
# in the biochip of size (numRows x numCols)
#================================================================================
	global row, col
	
	neighbour = []
	
	if cellInDmfb(row_index, col_index) == False:
		print("fourNeighbour: Index out of DMFB")
	else:
		if (cellInDmfb(row_index - 1, col_index) == True):
			neighbour.append((row_index - 1, col_index))
			
		if (cellInDmfb(row_index, col_index -  1) == True):
			neighbour.append((row_index, col_index-1))
			
		if (cellInDmfb(row_index, col_index + 1) == True):
			neighbour.append((row_index, col_index+1))
			
		if (cellInDmfb(row_index + 1, col_index) == True):
			neighbour.append((row_index + 1, col_index))
		
	return neighbour 


def dropletMovementConstraint(clauseFile, dropletId): 
#==================================================================================
# (A droplet on (x,y) at t) IMPLIES (It was already on (x,y) at t-1 OR 
# any of its four neighbour at t-1 OR dispensed from the reservoir at t)  
#==================================================================================    
	global row, col, dropletDispenserDict, T
    
	clauseFile.write("# Movement constraint for droplet = %d\n"%dropletId)
	for x in range(1, row + 1):
		for y in range(1, col + 1):
			(dropletId_x, dropletId_y) = dropletDispenserDict[dropletId]
			dropletId_x += 1		#Convert 0 index to 1 index
			dropletId_y += 1
			fourNeighbourCells = fourNeighbour(x, y)
			for t in range(1, T + 1):
				constraint = "s.add(Implies(a_%d_%d_%d_%d, Or(a_%d_%d_%d_%d,"%(x, y, dropletId, t, x, y, dropletId, t - 1) 
				# Find dispensor location from dropletId
				
				for (r,c) in fourNeighbourCells:
					constraint += "a_%d_%d_%d_%d, "%(r , c, dropletId, t - 1)
					
				constraint = constraint[:-2]
				
				if (dropletId_x, dropletId_y) == (x,y):    
					# A dispenser cell for dropletId exists at the current location and that dispense a droplet at t  
					constraint += ", ip_%d_%d_%d"%(dropletId_x, dropletId_y, t)
				
				constraint += ")))\n"
				clauseFile.write(constraint)
			clauseFile.write("#---------------------------------------------------------\n")



def dropletDisappearenceConstraint(clauseFile, dropletId): 
#==================================================================================
# A droplet may disappear if it comes to a output reservoir cell 
#==================================================================================    
	global row, col, outputLocationList, T
	
	clauseFile.write("#================================================================================================\n")
	clauseFile.write("# Disappearence constraint for droplet = %d\n"%dropletId)
	clauseFile.write("#================================================================================================\n")
	for x in range(1, row + 1):
		for y in range(1, col + 1):
			for t in range(1, T + 1):
				constraint = "s.add(Implies(And(a_%d_%d_%d_%d, "%(x, y, dropletId, t)
				
				fourNeighbourCells = fourNeighbour(x, y)
				for (r,c) in fourNeighbourCells:
					constraint += "Not(a_%d_%d_%d_%d), "%(r, c, dropletId, t - 1)
				
				constraint = constraint[:-2] + "), " 
				
				# Check whether the current cell has sink
				if (x,y) in outputLocationList:                
					constraint +=  "op_%d_%d_%d))\n" %(x,y,t)
				else:
					constraint += "False))\n"
					
				clauseFile.write(constraint)
  
			clauseFile.write("#---------------------------------------------------------\n")


def eightNeighbour(row_index, col_index):
#================================================================================
# Returns 8-neighbour cells of (row_index,col_index)
# in the biochip of size (numRows x numCols)
#================================================================================
	global row, col
	
	neighbour = []
	
	if cellInDmfb(row_index, col_index) == False:
		print("eightNeighbour: Index out of DMFB")
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

def getNewTempVar():
	# Returns a new temporary variable
	global __Id
	newVar = "t"+str(__Id)
	__Id = __Id + 1
	return newVar


def proximityAttack_at_t(clauseFile, t):
#==================================================================================
# This function checks whether a poximity attack is possible at time t
#==================================================================================     
	global row, col, TotalDroplet
	
	tmpVarList = []
	
	clauseFile.write("#-------------------------------------------------------------------------------------------------\n")
	clauseFile.write("# Proximity attack clause at time %d\n"%t)
	clauseFile.write("#-------------------------------------------------------------------------------------------------\n")
	
	for x in range(1, row + 1):
		for y in range(1, col + 1):
			clauseFile.write("# Proximity attack clause for (%d,%d)\n"%(x,y))
			newTmpVar = getNewTempVar()
			tmpVarList.append(newTmpVar)
			clauseFile.write("%s = Bool('%s')\n"%(newTmpVar,newTmpVar))
			constraint = "s.add(%s == Implies(("%newTmpVar
			for d in range(1, TotalDroplet + 1):
				constraint += "If(a_%d_%d_%d_%d == True, 1, 0) + "%(x,y,d,t)
			constraint = constraint[:-2] + " == 1), And("
			
			#For RHS
			neighbors_8 = eightNeighbour(x,y)
			for (r,c) in neighbors_8:
				for d in range(1, TotalDroplet + 1):
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


def proximityAttack(clauseFile):
#==================================================================================
# This function generates prominity clause for all time  
#==================================================================================
	global T
	for t in range(1, T + 1):
		proximityAttack_at_t(clauseFile, t)
	
	constraint = "s.add(Or("
	for t in range(1, T + 1):
		constraint += "e_%d, "%t
		
	constraint = constraint[:-2] + "))\n"
	
	clauseFile.write(constraint) 


# -------------------------------------------------------------------------------------------------------
#-------------------------------Setup conditions---------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
 
def initialConfiguration(clauseFile):
#===============================================================================
# No droplet present at t = 0
#===============================================================================
	global row, col, TotalDroplet
	
	clauseFile.write("# ----------------------------------------\n") 
	clauseFile.write("# No droplet should present at time step 0\n")
	clauseFile.write("# ----------------------------------------\n") 
	
	for Id in range(1, TotalDroplet + 1):
		constraint = "s.add(And("
		for x in range(1, row + 1):
			for y in range(1, col + 1):
				constraint += "Not(a_%d_%d_%d_0), "%(x, y, Id)
		
		constraint = constraint[:-2] + "))\n"
		
		clauseFile.write(constraint)

def finalConfiguration(clauseFile):
#===============================================================================
# No droplet present at t = 0
#===============================================================================
	global row, col, T, TotalDroplet
	
	clauseFile.write("#================================================================================================\n") 
	clauseFile.write("# No droplet should present at time step T\n")
	clauseFile.write("#================================================================================================\n") 
	
	for Id in range(1, TotalDroplet + 1):
		constraint = "s.add(And("
		for x in range(1, row + 1):
			for y in range(1, col + 1):
				constraint += "Not(a_%d_%d_%d_%d), "%(x,y,Id,T)
		
		constraint = constraint[:-2] + "))\n"
		
		clauseFile.write(constraint)


def dropletDispense(clauseFile, p, t_list):
#===============================================================================
# A droplet is dispensed on location (x,y) at each time t belongs to t_list 
#===============================================================================
	global DispanceList, T
	x = p[0] + 1
	y = p[1] + 1
	# Check whether a valid dispenser is available at that location or not
    

	clauseFile.write("# -------------------------------------------------\n") 
	clauseFile.write("# Droplet dispensing constraint")
	clauseFile.write("# -------------------------------------------------\n")
	
	constraint = "s.add(And("
	
	for t in range(0, T + 1):
		if t in t_list:
			constraint += "ip_%d_%d_%d, "%(x,y,t)
		else:
			constraint += "Not(ip_%d_%d_%d), "%(x,y,t)
	
	constraint = constraint[:-2] + "))\n"
	clauseFile.write(constraint)
    

def dropletDisappearence(clauseFile, p, t_list):
#===============================================================================
# A droplet can disappear on location (x,y) at each time t belongs to t_list 
#=============================================================================== 
	global dropletDispenserDict, TotalDroplet
	x = p[0] + 1
	y = p[1] + 1
	
	clauseFile.write("# A droplet on (%d,%d) may go to output at time %s \n"%(x,y,str(t_list))) 
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
			for d in range(1, TotalDroplet + 1):
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


def insertCheckpoint1X(clauseFile, p, t): 
#==================================================================================
# A droplet (1X) must appear on (x,y) at t
#================================================================================== 
	global TotalDroplet
	x = p[0]
	y = p[1]
	
	clauseFile.write("# Checkpoint (1X) on (%d,%d) at %d \n"%(x,y,t))
	constraint = "s.add("
	for d in range(1, TotalDroplet + 1):
		for x in range(1, row + 1):
			for y in range(1, col + 1):
				constraint += "If(a_%d_%d_%d_%d == True, 1, 0) + "%(x,y,d,t)
	constraint = constraint[:-2] + "== 1)\n"
	clauseFile.write(constraint)

def  main():
	global cp
	global outputLocationList
	global T
	print("Enter File name : ")
	file = input()
	scan_input(file)
	#print(DropletMap)
	
	
	cp.append(0)
	cp.append(T)
	print(T)
	print("Checking for proximity attack ")
	SizeOfCPForProximityAttack = 0
	CPForProximityAttack = defaultdict(set)
	for t1 in range(0,T - 2):
		for t2 in range(t1 + 1, T):
			print("P For time ",t1, t2)
			p = isProximityAttack(t1,t2)
			if p != -1:
				for ts in p:
					CPForProximityAttack[ts[0]].add(ts[1])
					CPForProximityAttack[ts[0]].add(ts[2])
					cp.append(ts[0])
				
	for _ in range(T):
		for i in CPForProximityAttack[_]:
			SizeOfCPForProximityAttack = SizeOfCPForProximityAttack + 1
	cp.sort()
	cp = [*set(cp)]
	NoOfCPforProximmityAttack = len(cp)
	print("Checking for Swap attack ")
	#t1 = 0; t2 = 2
	#while t2 < T - 2:
	#	p = isSwapAttack(t1, t2)
	#	if p != -1:
	#		if not inBetween(t1, t2):
	#			cp.append([(t1 + t2) // 2, 1])
	#			t1 = t2
	#			t2 = t2 + 2
	#	t2 = t2 + 1
	SwapAttack = []
	for t1 in range(0,T - 2):
		for t2 in range(t1 + 1, T):
			print("S For time ",t1, t2)
			p = isSwapAttack(t1, t2)
			if p != -1:
				if not inBetween(t1, t2):
					SwapAttack.append([t1, t2])
	SwapAttack.sort(key = lambda x:(x[1], x[0]))
	end = -1
	Timestamp = []
	for s, e in SwapAttack:
		if s >= end:
			Timestamp.append(e - 1)
			end = e - 1
		elif e < end:
			continue
		else:
			Timestamp.append(end - 1)
			end = s - 1
	for t in Timestamp:
		cp.append(t)
	cp.sort()
	cp = [*set(cp)]
	cp.sort()
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
	
	
	print("Size check point of proximity attack " + str(SizeOfCPForProximityAttack))
	NumberOfCellCheck = (SizeOfCPForProximityAttack + (len(cp) - NoOfCPforProximmityAttack) * row * col)
	NumberOfCellCheckPersentageWise = ( NumberOfCellCheck / (row * col * T)) * 100
	print("Optimize if we consider cell wise ", end=" ")
	print(str(100 - NumberOfCellCheckPersentageWise) + " %")
	
	#========================================================
	#===============Checkpoint verification==================
	#========================================================
	
	clauseFile = open('Myclause.py','w')
	init(clauseFile)
	varDeclare(clauseFile)
	dropletUniqnessConstraint(clauseFile)
	cellOccupancyConstraint(clauseFile)
	for d in range(1, TotalDroplet + 1):
		dropletMovementConstraint(clauseFile, d)
	for d in range(1, TotalDroplet + 1):
		dropletDisappearenceConstraint(clauseFile, d)
	initialConfiguration(clauseFile)
	DispanceDic = defaultdict(list)
	for tuple in DispanceList:
		t = tuple[0]
		x = tuple[1]
		y = tuple[2]
		DispanceDic[(x, y)].append(t)
	DisappearenceDic = defaultdict(list)
	for tuple in DisappearenceList:
		t = tuple[0]
		x = tuple[1]
		y = tuple[2]
		DisappearenceDic[(x, y)].append(t)
		if (x, y) not in outputLocationList:
			outputLocationList.append((x, y))
	for (x, y) in DispanceDic:
		dropletDispense(clauseFile, (x, y), DispanceDic[(x, y)])
	for (x, y) in DisappearenceDic:
		dropletDisappearence(clauseFile, (x, y), DisappearenceDic[(x, y)])
	proximityAttack(clauseFile)
	for t in cp:
		for x in range(1, row + 1):
			for y in range(1, col + 1):
				if DropletMap[t][x - 1][y - 1] != 0:
					insertCheckpoint1X(clauseFile, (x, y), t)
	finalConfiguration(clauseFile)
	finish(clauseFile)
	print("Run clause file")
if __name__ == '__main__':
    main()