from collections import defaultdict
row, col = 0, 0
DropletMap = []		#To store droplet map
droplet = {}	#key would be tuple of (clock, x, y) and value would be droplet number
locMap = {}		#Key is droplet, timestamp and value is location (x,y)
dropletList = defaultdict(list)#Key is timestamp and value is list of droplet numbers
T = 0
cp = []			#To store the check points
accuracy = 0
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
	
	ListCP = []						#Checkpoints in between t1 and t2
	#print("Row is : " + str(row))
	for i in range(0, len(dropt1t2)):
		for j in range(i + 1, len(dropt1t2)):
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
			Locd1 = []
			Locd2 = []
			for t_ in range(t1 + 1, t2):
				#Reduceing the search space
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
						e = ((dis(locMap[(d1, t1)], p1) <= abs(t_ - t1)) and (dis(locMap[(d2, t2)], p2) <= abs(t_ - t1)) and (dis(p1, p2) <= 1) and (dis(p1, locMap[(d1, t2)]) <= abs(t2 - t_)) and (dis(p2, locMap[(d2, t2)]) <= abs(t2 - t_)))
						if e is True:
							ListCP.append(t_)
						#-----------------------
	if len(ListCP) == 0:
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
		for j in range(i + 1, len(dropt1t2)):
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
	
def scan_input(filename):
	global T
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
			elif tk[0:3] == 'end':
				T = temp
				break
			else:
				break
	ip_f1.close()	
	#TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
	
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
	d = 1						#To assign a number for droplets, After using d ,please do update by 1
	DropletMap = [[[0]*col for _ in range(row)] for i in range(T)]
	for line in ip_f:
		
		#------ synchronize clock--------
		
		#--------------------------------
		token = line.split()
		i = 1
		#If blank space then skip
		if len(token) == 0:
			continue
		#Here we substact -1 from row and colum because input fromate is 1 indexing
		for tk in token:
			#print(tk)
			if tk.isnumeric():
				clock = int(tk)
				continue
			#print(tk[0:3])
			if clock != 0:
				DropletMap[clock] = DropletMap[clock - 1]
			if tk[0:3] == 'dis':
				i = 9
				r = 0; c = 0
				while tk[i] != ',':
					r = r*10 + int(tk[i])
					i = i + 1
				i = i + 1
				while tk[i] != ')':
					c = c*10 + int(tk[i])
					i = i + 1
				DropletMap[clock][r - 1][c - 1] = 1
				droplet[(clock, r - 1, c - 1)] = d
				locMap[(d, clock)] = (r - 1, c - 1)
				dropletList[clock].append(d)
				#if clock in dropletList:
				#	dropletList[clock].append(d)
				#else:
				#	dropletList[clock] = list(d)
				d = d + 1
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
				DropletMap[clock][r2 - 1][c2 - 1] = 1
				DropletMap[clock - 1][r1 - 1][c1 - 1] = 0
				print("Clock is : " + str(clock))
				print(token)
				print(droplet[(clock - 1, r1 - 1, c1 - 1)])
				temp_droplet = droplet[(clock, r2 - 1, c2 - 1)] = droplet[(clock - 1, r1 - 1, c1 - 1)]
				
				locMap[(temp_droplet, clock)] = (r2 - 1, c2 - 1)
				dropletList[clock].append(temp_droplet)
				#If no move is happen so all droplet of previous timestamp should be there
				
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
				#Trying to reserve 4 cell for mixing
				"""
				p = 0
				while p != c - 1:
					#If mixing size is 4 and vertical then r1 == r2
					if r1 == r2:
						l = 0
						while l != 4:
							DropletMap[clock + p][r1 - 1][c1 - 1 + l] = 1
							droplet[(clock + p, r1 - 1, c1 - 1 + l)] = d
							locMap[(d, clock + p)] = (r1 - 1, c1 - 1 + l)
							l = l + 1
					#If mixing size is 4 and horizental then c1 == c2
					else:
						l = 0
						while l != 4:
							DropletMap[clock + p][r1 - 1 + l][c1 - 1] = 1
							droplet[(clock + p, r1 - 1 + l, c1 - 1)] = d
							locMap[(d, clock + p)] = (r1 - 1 + l, c1 - 1)
							l = l + 1
					dropletList[clock + p].append(d)
					p = p + 1
				d = d + 1
				if r1 == r2:
					DropletMap[clock + p][r1 - 1][c1 - 1] = 1
					DropletMap[clock + p][r2 - 1][c2 - 1] = 1
					droplet[(clock + p, r1 - 1, c1 - 1)] = d
					locMap[(d, clock + p)] = (r1 - 1, c1 - 1)
					dropletList[clock + p].append(d)
					d = d + 1
					droplet[(clock + p, r2 - 1, c2 - 1)] = d
					locMap[(d, clock + p)] = (r2 - 1, c2 - 1)
					dropletList[clock + p].append(d)
					d = d + 1
				else:
					DropletMap[clock + p][r1 - 1][c1 - 1] = 1
					DropletMap[clock + p][r2 - 1][c2 - 1] = 1
					droplet[(clock + p, r1 - 1, c1 - 1)] = d
					locMap[(d, clock + p)] = (r1 - 1, c1 - 1)
					dropletList[clock + p].append(d)
					d = d + 1
					droplet[(clock + p, r2 - 1, c2 - 1)] = d
					locMap[(d, clock + p)] = (r2 - 1, c2 - 1)
					dropletList[clock + p].append(d)
					d = d + 1
				"""
				
				#Trying not by reserving cells
				m = c // 6
				l = 1
				while m != 0:
					#code for 6 cycle mixing
					if r1 == r2:	#If mixing size is 4 and vertical then r1 == r2
						#Step 1.1 : Moving left droplet by one cell right
						DropletMap[clock + l][x1][y1 + 1] = 1
						temp_droplet = droplet[(clock + l, x1, y1 + 1)] = droplet[(clock + l - 1, x1, y1)]
						locMap[(temp_droplet, clock + l)] = (x1, y1 + 1)
						dropletList[clock + l].append(temp_droplet)
						#Step 1.2 : Moving right droplet by one cell left
						DropletMap[clock + l][x2][y2 - 1] = 1
						temp_droplet = droplet[(clock + l, x2, y2 - 1)] = droplet[(clock + l - 1, x2, y2)]
						locMap[(temp_droplet, clock + l)] = (x2, y2 - 1)
						dropletList[clock + l].append(temp_droplet)
						
						#Increase timestamp
						l = l + 1
						
						#Step 2 : Right droplet move left and make 2x droplet
						d_new = d
						d = d + 1
						DropletMap[clock + l][x1][y1 + 1] = 2
						droplet[(clock + l, x1, y1 + 1)] = d_new
						locMap[(d_new, clock + l)] = (x1, y1 + 1)
						dropletList[clock + l].append(d_new)
						
						#Increase timestamp
						l = l + 1
						
						#Setp 3 : Move 2x droplet by one cell right
						DropletMap[clock + l][x1][y1 + 2] = 2
						temp_droplet = droplet[(clock + l, x1, y1 + 2)] = droplet[(clock + l - 1, x1, y1 + 1)]
						locMap[(temp_droplet, clock + l)] = (x1, y1 + 2)
						dropletList[clock + l].append(temp_droplet)
						
						#Increase timestamp
						l = l + 1
						
						#Step 4 : Move 2x droplet by one cell left
						DropletMap[clock + l][x1][y1 + 1] = 2
						temp_droplet = droplet[(clock + l, x1, y1 + 1)] = droplet[(clock + l - 1, x1, y1 + 2)]
						locMap[(temp_droplet, clock + l)] = (x1, y1 + 1)
						dropletList[clock + l].append(temp_droplet)
						
						#Increase timestamp
						l = l + 1
						
						#Step 5.1 : Split 2x droplet and create left droplet
						d_new = d
						d = d + 1
						DropletMap[clock + l][x1][y1 + 1] = 1
						droplet[(clock + l, x1, y1 + 1)] = d_new
						locMap[(d_new, clock + l)] = (x1, y1 + 1)
						dropletList[clock + l].append(d_new)
						#Step 5.2 : Split 2x droplet and create right droplet
						d_new = d
						d = d + 1
						DropletMap[clock + l][x1][y1 + 2] = 1
						droplet[(clock + l, x1, y1 + 1)] = d_new
						locMap[(d_new, clock + l)] = (x1, y1 + 1)
						dropletList[clock + l].append(d_new)
						
						#Increase timestamp
						l = l + 1
						
						#Step 6.1 : Move left droplet by one cell left
						DropletMap[clock + l][x1][y1] = 1
						temp_droplet = droplet[(clock + l, x1, y1)] = droplet[(clock + l - 1, x1, y1 + 1)]
						locMap[(temp_droplet, clock + l)] = (x1, y1)
						dropletList[clock + l].append(temp_droplet)
						#Step 6.2 : Move right droplet by one cell right
						DropletMap[clock + l][x1][y1 + 3] = 1
						temp_droplet = droplet[(clock + l, x1, y1 + 3)] = droplet[(clock + l - 1, x1, y1 + 2)]
						locMap[(temp_droplet, clock + l)] = (x1, y1 + 3)
						dropletList[clock + l].append(temp_droplet)
						
					else:
						
					
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
				DropletMap[clock][r - 1][c - 1] = 0
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
				DropletMap[clock][r - 1][c - 1] = 0
			elif tk[0:3] == 'end':
				ip_f.close()
				return
			#else:
			#	continue
		#print("At clock " + str(clock) + " Golden Map is : ")
		#for temp in arr:
		#	print(temp)
		#print("********************************************")
		#clock = clock + 1
		print("Clock is : " + str(clock))
		for list in DropletMap[clock]:
			print(list)
		print("**************************")
	T = clock
	ip_f.close()
			
def  main():
	global cp
	print("Enter File name : ")
	file = input()
	scan_input(file)
	#print(DropletMap)
	for a in DropletMap:
		for b in a:
			print(b)
		print("*****************")
	
	cp.append(0)
	cp.append(T)
	print(T)
	for t1 in range(0,T):
		for t2 in range(t1 + 1, T):
			p = isProximityAttack(t1,t2)
			if p != -1:
				for ts in p:
					cp.append(ts)
	for t1 in range(0,T):
		for t2 in range(t1 + 1, T):
			p = isSwapAttack(t1, t2)
			if p != -1:
				if not inBetween(t1, t2):
					cp.append((t1 + t2) // 2)
	cp.sort()
	cp = [*set(cp)]
	print(cp)
if __name__ == '__main__':
    main()