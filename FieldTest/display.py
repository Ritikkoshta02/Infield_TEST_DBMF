'''
Created on 14-Jan-2016
@author: sukanta
'''


import re
import subprocess
from ast import literal_eval as make_tuple

# assay_time = 80
# rownum = 8 
# colnum = 15
# reservoir = [(3,1,'S'),(3,7,'R'),(7,5,'W')]

assay_time = 45
rownum = 7 
colnum = 7
reservoir = [(3,1,'S'),(3,7,'R'),(7,5,'W')]

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
    myfile.write('\\documentclass{article}\n\n')
    myfile.write('\\usepackage{tikz}\n\n')
    myfile.write('\\begin{document}\n\n')
    myfile.write('\\tikzset{droplet/.style={draw,circle,fill, yellow, inner sep=6pt, text=black}}\n')
    myfile.write('\\tikzset{detector/.style={gray}}\n')
    myfile.write('\\tikzset{detecting/.style={green}}\n')
    myfile.write('\\tikzset{mixer/.style={draw,circle,fill, pink, inner sep=4pt, text=black}}\n')
    myfile.write('\\tikzset{dispenser/.style={black}}\n')
    myfile.write('\\tikzset{sink/.style={cyan,fill,rectangle,minimum height = 2.6em, minimum width = 2.6em, text=black}}\n')
    

def step_tex_gen():
    global snapShotDict
    init()
    for time in range(1,assay_time+1):
        f = open('op','r')
        myfile.write('\n\\fbox{\n')
        #myfile.write('\n Time %3d\n\n'%time)
        myfile.write('\\begin{tikzpicture}\n')
        myfile.write('\draw[step=1.0,black,thin] (0,0) grid (%d,%d);\n'%(colnum,rownum))
        
        myfile.write('\\node[sink] at (%f,%f) {\\Large $%s$};\n'%(0-0.5,rownum-0.5,'S'))
        myfile.write('\\node[sink] at (%f,%f) {\\Large $%s$};\n'%(colnum+0.75,0+0.5,'E'))
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
            
            myfile.write('\\node[sink] at (%f,%f) {\\Large $%s$};\n'%(x-0.5,y+0.5,res[2]))
                    
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
            myfile.write('\\node[droplet] at (%f,%f) {$%d$};\n'%(y-.5,(rownum+1)-x-.5,drop_id))
           
                
        # Render occupied cells
        if time in snapShotDict:
            occupiedCells = snapShotDict[time]
            for (x,y) in occupiedCells:
                print (x,y)
                
                myfile.write('\\node[mixer] at (%f,%f) {f};\n'%(y-.5,(rownum+1)-x-.5))
        
        myfile.write('\n\\end{tikzpicture}\n')
        myfile.write('}\n\\pagebreak\n\\vspace{20pt}\n')
        f.close()
#createSnapshotDict('assayPCR8x15.txt')
createSnapshotDict('assayInVitro7x7.txt') 
#createSnapshotDict('assayREMIA10x10.txt')
#print snapShotDict           
step_tex_gen()
myfile.write('\n\\end{document}')
myfile.close()
subprocess.call(["pdflatex", "gui.tex"])  