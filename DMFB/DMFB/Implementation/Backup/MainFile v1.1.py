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
	ip_f = open(filename,'r')
	clock = 0
	global T
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
	d = 1						#To assign a number for droplets
	for line in ip_f:
		arr = [[0]*col for _ in range(row)]
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
				continue
			#print(tk[0:3])
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
				arr[r - 1][c - 1] = 1
				droplet[(clock, r - 1, c - 1)] = d
				locMap[(d, clock)] = (r - 1, c - 1)
				dropletList[clock].append(d)
				#if clock in dropletList:
				#	dropletList[clock].append(d)
				#else:
				#	dropletList[clock] = list(d)
				d = d + 1
			elif tk[0:3] == 'mov':
				i = 5
				r1 = 0; c1 = 0
				while tk[i] != ',':
					r1 = r1*10 + int(tk[i])
					i = i + 1
				i = i + 1
				while tk[i] != ',':
					c1 = c1*10 + int(tk[i])
					i = i + 1
				i = i + 1
				r2=0
				c2=0
				while tk[i] != ',':
					r2 = r2*10 + int(tk[i])
					i = i + 1
				i = i + 1
				while tk[i] != ')':
					c2 = c2*10 + int(tk[i])
					i = i + 1
				arr[r2 - 1][c2 - 1] = 1
				temp_droplet = droplet[(clock, r2 - 1, c2 - 1)] = droplet[(clock-1, r1 - 1, c1 - 1)]
				droplet.pop((clock-1, r1 - 1, c1 - 1))
				locMap[(temp_droplet, clock)] = (r2 - 1, c2 - 1)
				dropletList[clock].append(temp_droplet)
			#elif tk[0:3] == 'mix':
			#	continue
			#elif tk[0:3] == 'was':
			#	continue
			#elif tk[0:3] == 'out':
			#	continue
			elif tk[0:3] == 'end':
				T = clock
				ip_f.close()
				return
			#else:
			#	continue
		#print("At clock " + str(clock) + " Golden Map is : ")
		#for temp in arr:
		#	print(temp)
		#print("********************************************")
		DropletMap.append(arr)
		clock = clock + 1
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