'''
Created on 31 Oct, 2018
@author: sukanta
'''

import re
import subprocess

T = 70
numRows = 8
numCols = 15
mix_id = [50,51,52,53,54,55,56,57,58,59,60]
reservoir = [(5,1,'R1'),(5,8,'R2'), (1,3,'O1'), (1,6,'O2'), (9,6,'O3')]

myfile = open("Biochip.tex","w+")

def init():
    myfile.write('\\documentclass[a4paper,landscape]{article}\n\n')
    myfile.write('\\usepackage{tikz}\n\n')
    myfile.write('\\begin{document}\n\n')
    myfile.write('\\tikzset{droplet/.style={draw,circle,fill, yellow, inner sep=5pt, text=black}}\n')
    myfile.write('\\tikzset{detector/.style={gray}}\n')
    myfile.write('\\tikzset{detecting/.style={green}}\n')
    myfile.write('\\tikzset{mixer/.style={draw,circle,fill, pink, inner sep=5pt, text=black}}\n')
    myfile.write('\\tikzset{dispenser/.style={black}}\n')
    myfile.write('\\tikzset{sink/.style={cyan,fill,rectangle,minimum height = 2.6em, minimum width = 2.6em, text=black}}\n')
    

def step_tex_gen():
    init()
    for time in range(0,T+1):
        f = open('op','r')
        myfile.write('\n\\fbox{\n')
        #myfile.write('\n\\hspace*{-100pt}\n')
        myfile.write('\n Time %3d\n\n'%time)
        myfile.write('\\begin{tikzpicture}\n')
        myfile.write('\draw[step=1.0,black,thin] (0,0) grid (%d,%d);\n'%(numCols,numRows))
        for res in reservoir:
            x = res[1]
            if x == 1:
                x = x - 1
            if x == numCols:
                x = x + 1
                            
            y = numRows - res[0]
            if y == 0:
                y = y - 1
            if y == numRows - 1:
                y = y + 1
            
            myfile.write('\\node[sink] at (%f,%f) {\\Large $%s$};\n'%(x-0.5,y+0.5,res[2]))
            
        string = 'a'+ '[0-9_]+_'+str(time)+' = True'
        l = re.findall(string,f.read())
        print l
        mixTable = dict() 
        for e in l:
            drop_id = int(e.split('_')[3])
            #print drop_id
            # x,y location must be interchanged for proper display
            x = float(e.split('_')[2])
            #print x
            y = numRows - float(e.split('_')[1])
            #print y
            if drop_id not in mix_id:
                myfile.write('\\node[droplet] at (%f,%f) {$%d$};\n'%(x-0.5,y+0.5,drop_id))
            else:
                if drop_id not in mixTable:
                    mixTable[drop_id] = [(x,y)]
                else:
                    mixTable[drop_id].append((x,y))
                
        # Render Mixer
        for mixer_id in mixTable:
            #print time,mixTable[mixer_id]
            mix_loc_1 = mixTable[mixer_id][0]
            mix_loc_2 = mixTable[mixer_id][1]
            x1 = mix_loc_1[0]
            y1 = mix_loc_1[1] 
            x2 = mix_loc_2[0]
            y2 = mix_loc_2[1] 
            if (x1 == x2):
                if y1 < y2:
                    myfile.write('\\fill[blue!40!white] (%f,%f) rectangle (%f,%f);\n'%(x1-1,y1,x2,y2+1))
                else:
                    myfile.write('\\fill[blue!40!white] (%f,%f) rectangle (%f,%f);\n'%(x2-1,y2,x1,y1+1))
            else:
                if x1 < x2:
                    myfile.write('\\fill[blue!40!white] (%f,%f) rectangle (%f,%f);\n'%(x1-1,y1,x2,y2+1))
                else:
                    myfile.write('\\fill[blue!40!white] (%f,%f) rectangle (%f,%f);\n'%(x2-1,y2,x1,y1+1))
                      
            myfile.write('\\node[mixer] at (%f,%f) {$%d$};\n'%(x1-0.5,y1+0.5,mixer_id))
            myfile.write('\\node[mixer] at (%f,%f) {$%d$};\n'%(x2-0.5,y2+0.5,mixer_id))
        myfile.write('\n\\end{tikzpicture}\n')
        myfile.write('}\n\\pagebreak\n\\vspace{20pt}\n')
        #myfile.write('\n\\pagebreak\n\\vspace{20pt}\n')
        f.close()
            
step_tex_gen()
myfile.write('\n\\end{document}')
myfile.close()
subprocess.call(["pdflatex", "Biochip.tex"])     
