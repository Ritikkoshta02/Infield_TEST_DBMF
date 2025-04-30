import sys
cyc=0
wrline=[]
file1 = open(sys.argv[1]+".dat","w")
with open('golden.txt','r') as f:
	for line in f:
		line = line.strip().split(' ')
		if (line[0]=='a'):
			if(line[4]==cyc):
				wrline[0]=wrline[0]+1
				wrline.append(line[1])
				wrline.append(line[2])
				wrline.append(line[3])
			else:
				if(cyc!=0):
					file1.write(str(wrline).replace("[","").replace("]","").replace(","," ").replace("'",""))
					file1.write("\n")
					del wrline[:]
				wrline.append(1)
				wrline.append(line[4])
				cyc=line[4]
				wrline.append(line[1])
                               	wrline.append(line[2])
                               	wrline.append(line[3])
file1.close()
	#for word in line.splinelit():
           #print(word)
