import csv
import subprocess
import base

kgd = {}
prv = {}
tdict = {}
ip =[]
op =[]
mix =[]
dlst = []
nlst = []
step=0
opmil = []
mixmil = []
def ismix((x,y),t):
	for (r1,c1), (r2,c2), ts, td in mix:
		if(((x,y) == (r1,c1) or (x,y) == (r2,c2)) and (ts==t)):
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

def runsat(opmil,mixmil,step):
	base.main(opmil,mixmil,step)
	with open('out-file.txt', 'w') as f:
		subprocess.call(["python","clause.py"], stdout=f)
	f.close()
	f = open('out-file.txt')
        line = f.readline()
        f.close()
	return(line.rstrip())

#file1 = open("newcplist.txt","a")
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
			#if (step==row[4]):
			#	tdict[row[3]]=(row[1],row[2],row[4])
			#else:
			#	if(len(dlst)!=0):
			#		maxd = max(dlst,key=dlst.count)
			#		if maxd in nlst:
			#			file1.write(str(tdict[maxd]).replace("(","").replace(")","").replace(", ",",")+"\n")
			#			kgd[maxd]=tdict[maxd]
			#		else:
			#			file1.write(str(prv[maxd]).replace("(","").replace(")","").replace(", ",",")+"\n")
                        #                        kgd[maxd]=prv[maxd]
			#	prv=tdict.copy()
                        #        tdict.clear()
                        #        tdict[row[3]]=(row[1],row[2],row[4])
			#	step = row[4]

			if (row[1],row[2],row[4]) in ip:
				kgd[row[3]]=(row[1],row[2],row[4])
			elif (row[1],row[2],row[4]) in op:
				#Now run sat to check if sat is ok till now
				opmil.append((row[1],row[2],row[3],row[4]))
				print(opmil)
				while True:
					status = runsat(opmil,mixmil,row[4])
					print("status after new op",status)
					if (status == 'sat'):
						print("trail with output")
						subprocess.call(['bash','guide.sh'])
					else:
						break

				 	
			elif (ismix((row[1],row[2]),row[4])==1):
				mixmil.append((row[1],row[2],row[3],row[4]))
				print(mixmil)
				while True:
                                        status = runsat(opmil,mixmil,row[4])
					print("status after new mix",status)
                                        if (status == 'sat'):
						print("trail with mix")
                                                subprocess.call(['bash','guide.sh'])
                                        else:
                                                break
				#run sat to check is sat is ok till now		
									

#file1.close()
