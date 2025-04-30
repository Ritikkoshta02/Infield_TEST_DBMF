import csv
kgd = {}
prv = {}
tdict = {}
ip =[]
op =[]
mix =[]
dlst = []
nlst = []
step=0
def ismix((x,y),t):
	for (r1,c1), (r2,c2), ts, td in mix:
		if(((x,y) == (r1,c1) or (x,y) == (r2,c2)) and (ts<t<ts+td)):
			return(1)
	return(0)

with open('remimix.txt') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
		#print(row[0])
		#print(row[1])
		#`print(row[3])
		if(row[0]=="enforceMixingclauseFile"):
			row[0]=4
			#row.replace("),",")")
			row = map(int,row)
			mix.append(((row[1],row[2]),(row[3],row[4]),row[5],row[6]))

print(mix)

file1 = open("newcplist.txt","a")
with open('remi_golden.txt') as csvfile:
	readCSV = csv.reader(csvfile, delimiter=' ')
	for row in readCSV:
		if(row[0]=='ip'):
			row[0]=1
			row = map(int,row)
			ip.append((row[1],row[2],row[3]))
			print("ip updated")
			print(ip)
		elif(row[0]=='a'):
			row[0]=2
			row = map(int,row)
			ipchk = 0
			opchk = 0
			for x in ip:
				if(x==(row[1],row[2],row[4])):
					kgd[row[3]]=(row[1],row[2],row[4])
					print("kgd updated")
					print(kgd)
					prv[row[3]]=(row[1],row[2],row[4])
					ipchk  = 1
			if(ipchk==0):
				if(row[4]==step):
					tdict[row[3]]=(row[1],row[2],row[4])
				else:
					print("at step",step)
					print(tdict)
					print(prv)
					for r, y in tdict.items():
						for d, x in kgd.items():
							if(ismix((y[0],y[1]),y[2])):
								kgd[r]=y
								print("mixer detected")
								print(kgd)
					while True:
						swchk = 0
						del dlst[:]
						del nlst[:]
						for r, y in tdict.items():
                                                	for d, x in kgd.items():
                                                        	if(ismix((y[0],y[1]),y[2])==0):		
									if(d != r and abs(y[0]-x[0]) + abs(y[1]-x[1]) <= abs(y[2]-x[2])):
										swchk = 1
										dlst.append(d)
										if(abs(y[2]-x[2])==1):
											nlst.append(d)
											nlst.append(r)
											print("too close", d, r)
						if(len(dlst)!=0):
							maxd = max(dlst,key=dlst.count)
							if maxd in nlst:
								file1.write(str(tdict[maxd]).replace("(","").replace(")","").replace(", ",",")+"\n")
                                                        	kgd[maxd]=tdict[maxd]
							else:	
								file1.write(str(prv[maxd]).replace("(","").replace(")","").replace(", ",",")+"\n")
								kgd[maxd]=prv[maxd]
								print("using prv for kgd")
							print("problematci droplets",dlst)
							print(kgd)
						else:
							break
							#dlst.append(d)
					step=row[4]
					for x in op:
						for r, y in tdict.items():
							if(x==y):
								del kgd[r]
								print("kgd entry deleted",r)
					prv=tdict.copy()				
					tdict.clear()
					tdict[row[3]]=(row[1],row[2],row[4])			#kgd[d]=tdict[d]
									
				#for x in op:
				#	if(x==(row[1],row[2],row[4])):
				#		del kgd[row[3]]
				#		#del prv[row[3]]
				#		print("kgd entry deleted",row[3])
				#		opchk = 1
			#if(opchk == 0):
			#	prv[row[3]]=(row[1],row[2],row[4])
			#print("prv updated")
			#print(prv)
		elif(row[0]=='op'):
			row[0]=3
			row = map(int,row)
                        op.append((row[1],row[2],row[3]-1))
			print("op updated")
			print(op)			
		#print(len(row))

file1.close()
