import csv
import subprocess
kgd = {}
prv = {}
#tdictlst
tdict = {}
ipdict = {}
opdict = {}
mixdict = []
ip =[]
op =[]
mix =[]
dlst = []
nlst = []
step=0
def ismix((x,y),t):
	for (r1,c1), (r2,c2), ts, td in mix:
		if(((x,y) == (r1,c1) or (x,y) == (r2,c2)) and (ts<=t<ts+td)):
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

with open('remi_golden.txt') as csvfile:
	readCSV = csv.reader(csvfile, delimiter=' ')
	for row in readCSV:
		if(row[0]=='ip'):
			row[0]=1
			row = map(int,row)
			ip.append((row[1],row[2],row[3]))
			print("ip updated")
			print(ip)
		elif(row[0]=='op'):
                        row[0]=3
                        row = map(int,row)
                        op.append((row[1],row[2],row[3]-1))
                        print("op updated")
                        print(op)
		elif(row[0]=='a'):
			row[0]=2
			row = map(int,row)
			for x in ip:
				if(x==(row[1],row[2],row[4])):
					ipdict[row[3]]=(row[1],row[2],row[4])
			for x in op:
				if(x==(row[1],row[2],row[4])):
					opdict[row[3]]=(row[1],row[2],row[4])
			if(ismix((row[1],row[2]),row[4])):
				mixdict.append((row[1],row[2],row[3],row[4]))


print(opdict)
print(ipdict)
print(mixdict)
lnglst=[]
#subprocess.run('cat cplist.txt | sed 's/,/ /g' | sort -nk 3 > cplistcopy.txt', shell=True)
t=0
with open('cplistcopy.txt') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=' ')
        for row in readCSV:
                row = map(int,row)
		if (t == row[2]):
			lnglst.append(row)
		else:
			tdict[t] = lnglst
			del lnglst[:]
			lnglst.append(row)
			t=row[2]			
		#tdict[(row[2],row[3])]=(row[0],row[1])

t=0
i=1
file1 = open("newcplist.txt","w")
with open('cplistcopy.txt') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=' ')
        for row in readCSV:
		row = map(int,row)
		print(row)
		if((row[3], (row[0],row[1],row[2])) in ipdict.viewitems()):
			print("escaping input")
			kgd[row[3]] = (row[0],row[1],row[2])
			
		#elif((row[0],row[1],row[3],row[2]) in mixdict):
		#	print("escaping mix")
		#	kgd[row[3]] = (row[0],row[1],row[2])
		#elif((row[3], (row[0],row[1],row[2])) in opdict.viewitems()):
                #        print("detected output")
                 #       del kgd[row[3]] 
		else:
			if row[3] in kgd:
				for k,v in kgd.items():
					if(k != row[3] and abs(v[0]-row[0]) + abs(v[1]-row[1]) <= (abs(v[2]-row[2])+2)):
                                	#(x,y)=tdict[row[2],k]
						print("added row:",row)
						file1.write(str(row).replace("[","").replace("]","").replace(", ",",")+"\n")
						prv[row[3]] = (row[0],row[1],row[2])
						dlst.append(row[3])
					else:
						print("deleted row:", row)
						print(kgd)
				if(t!=row[2]):
					for d in dlst:
						kgd[d]=prv[d]
					del dlst[:]
					t=row[2]

				if((row[3], (row[0],row[1],row[2])) in opdict.viewitems()):
                        		print("detected output")
                        		del kgd[row[3]]
			else:
				print("added new row:",row)
                                file1.write(str(row).replace("[","").replace("]","").replace(", ",",")+"\n")
                                kgd[row[3]] = (row[0],row[1],row[2])
				#t=row[2]

file1.close()	
