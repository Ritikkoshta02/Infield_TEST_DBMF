'''
Created on 20-Jun-2016
@author: sukanta
'''
import re
import subprocess
from ast import literal_eval as make_tuple

assay_time = 80
rownum = 15 
colnum = 15
reservoir = [(3,1,'S1'),(3,15,'S2'),(13,1,'R1'),(13,15,'R2'), (1,7,'W'),(1,9,'W')]

'''assay_time = 161
rownum = 16 
colnum = 16
reservoir = [(16,9,'W'),(5,16,'R1'),(12,16,'R2'),(1,5,'S3'),(1,12,'B'),(5,1,'S1'),(12,1,'S2')]
'''

myfile = open("gui.tex","w+")

snapShotDict = dict()

def createSnapshotDict(assayFile):
    global snapShotDict
    fp = open(assayFile,'r')
    for line in fp.readlines():
        if line == "end\n":
            break
        occupiedCells = line.split()
        time = int(occupiedCells[0])
        snapShotDict[time] = []
        for i in range(1,len(occupiedCells)):
            cell =  make_tuple(occupiedCells[i])
            snapShotDict[time].append(cell)
    

def init():
    myfile.write('\\documentclass[a1paper,landscape]{article}\n\n')
    myfile.write('\\usepackage{tikz}\n\n')
    myfile.write('\\usepackage{lscape}\n\n')
    myfile.write('\\begin{document}\n\n\\footnotesize\n')
    myfile.write('\\tikzset{droplet/.style={draw,circle,fill, yellow, inner sep=2pt, text=black}}\n')
    myfile.write('\\tikzset{detector/.style={gray}}\n')
    myfile.write('\\tikzset{detecting/.style={green}}\n')
    myfile.write('\\tikzset{mixer/.style={draw,circle,fill, pink, inner sep=2pt, text=black}}\n')
    myfile.write('\\tikzset{dispenser/.style={black}}\n')
    myfile.write('\\tikzset{sink/.style={cyan,fill,rectangle, text=black}}\n')
    

def step_tex_gen():
    global snapShotDict
    init()
    for time in range(1,assay_time+1):
        f = open('op','r')
        #myfile.write('\n\\hspace*{-50pt}\n')
        myfile.write('\n\\fbox{\n')
        #myfile.write('\n Time %3d\n\n'%time)
        myfile.write('\\begin{tikzpicture}\n')
        myfile.write('\draw[step=.5,black,thin] (0,0) grid (%f,%f);\n'%(colnum/2.0,rownum/2.0))
        
        #myfile.write('\\node[sink] at (%f,%f) {\\Large $%s$};\n'%(0-0.5,rownum-0.5,'S'))
        #myfile.write('\\node[sink] at (%f,%f) {\\Large $%s$};\n'%(colnum+0.5,0+0.5,'E'))
        for res in reservoir:
            x = res[1]
            if x == 1:
                x = x - 1
            if x == colnum:
                x = x + 1
                            
            y = rownum - res[0]
            if y == 0:
                y = y - 1
            if y == rownum - 1:
                y = y + 1
            
            myfile.write('\\node[sink] at (%f,%f) {$%s$};\n'%(((x/2.0)-0.25),((y/2.0)+0.25),res[2]))
                    
        string = 'x[0-9_]+_'+str(time)+' = True'
        l = re.findall(string,f.read())
        print l
        print '----------------'
        for e in l:
            drop_id = int(e.split('_')[1])
            #print drop_id
            x = float(e.split('_')[2])
            #print x
            y = float(e.split('_')[3])
            #print y
            myfile.write('\\node[droplet] at (%f,%f) {$%d$};\n'%((y/2.0)-0.25,(rownum+1-x)/2.0-0.25,drop_id))
           
                
        # Render occupied cells
        if time in snapShotDict:
            occupiedCells = snapShotDict[time]
            for (x,y) in occupiedCells:
                print (x,y)
                
                myfile.write('\\node[mixer] at (%f,%f) {f};\n'%((y/2.0)-0.25,(rownum+1-x)/2.0-0.25))
        
        myfile.write('\n\\end{tikzpicture}\n')
        myfile.write('}\n\n')
        f.close()

#createSnapshotDict('invitro_16x16.txt')
createSnapshotDict('assayMultiplexed15x15.txt')
#createSnapshotDict('assayInVitro7x7.txt') 
#createSnapshotDict('assayREMIA10x10.txt')
#print snapShotDict           
step_tex_gen()
myfile.write('\n\\end{document}')
myfile.close()
subprocess.call(["pdflatex", "gui.tex"])  