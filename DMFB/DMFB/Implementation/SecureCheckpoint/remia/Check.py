fp = open('op','r')
ff = open('input.txt','w')
lines = fp.readlines()
for line in lines:
    token = line.strip().split("=")
    location = token[0].split("_")
    x, y, d, t = location[1], location[2], location[3], location[4]
    ff.write(str(x) + ", " + str(y) + ", " + str(t) + "\n")
fp.close()