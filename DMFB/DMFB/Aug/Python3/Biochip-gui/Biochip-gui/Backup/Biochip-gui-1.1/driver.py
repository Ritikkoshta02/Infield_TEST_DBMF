'''
Created on 27-Jun-2013

@author: sukanta
'''
from Tkinter import *
from tkFileDialog   import askopenfilename 
from tkMessageBox import *
import re
import subprocess

sleep_time = 0
clock = None        #Slider Handle
ip_file = ''


def header(ip_f,op_f):
    line = ip_f.readline()            
    token = line.split()
    if token[0] != 'dimension' or len(token) != 3:
        print 'First line should be \'dimension m n\''
        return
    else:
        op_f.write('from Biochip import *\n\n\n')
        op_f.write('root = Tk()\n')
        op_f.write('B = Biochip(root,%d,%d)\n'%(int(token[1]),int(token[2])))
        
        
    line = ip_f.readline()
    while not line.strip():
            line = ip_f.readline() 
    
    instr_line = re.compile('[a-z_]+\s*\([\s*\d+\s*,\s*]+\s*\w+\s*\)').findall(line)
    #print instr_line
    for instr in instr_line:
        gen(instr,op_f)
    
    op_f.write('print \'clock = %d \' %B.get_clock()\n')
    op_f.write('#----------------------------------------------------------------\n')
        
def gen(instr,f):
    obj = re.compile('[a-z_]+').match(instr)
    if obj == None:
        print 'Invalid syntax: ' + instr
        exit() 
    
    opcode = obj.group()    
    operands = re.compile('(\d+|\w+)').findall(instr[obj.end() + 1 :])
    
    if opcode == 'dispense' and len(operands) == 2:
        r = int(operands[0].strip())
        c = int(operands[1].strip())
        f.write('B.dispense_droplet(%d,%d)\n' % (r, c))
    elif opcode == 'move' and len(operands) == 4:
        rold = int(operands[0].strip())
        cold = int(operands[1].strip())
        rnew = int(operands[2].strip())
        cnew = int(operands[3].strip())
        f.write('B.move_droplet(%d,%d,%d,%d)\n' % (rold, cold, rnew, cnew))
    elif opcode == 'mix_split' and len(operands) == 5:
        r1 = int(operands[0].strip())
        c1 = int(operands[1].strip())
        r2 = int(operands[2].strip())
        c2 = int(operands[3].strip())
        t = int(operands[4].strip())
        f.write('B.instantiate_mixer(%d,%d,%d,%d,%d)\n' % (r1, c1, r2, c2, t))
    elif opcode == 'waste' and len(operands) == 2:
        r = int(operands[0].strip())
        c = int(operands[1].strip())
        f.write('B.delete_droplet(%d,%d)\n' % (r, c))
    elif opcode == 'output' and len(operands) == 2:
        r = int(operands[0].strip())
        c = int(operands[1].strip())
        f.write('B.delete_droplet(%d,%d)\n' % (r, c))
    elif opcode == 'reagent' and len(operands) == 3:
        r = int(operands[0].strip())
        c = int(operands[1].strip())
        reagent_name = operands[2]
        f.write('B.set_resevior(%d,%d,\'reagent\',"%s")\n'%(r,c,reagent_name))
    elif opcode == 'waste_reservior' and len(operands) == 2:
        r = int(operands[0].strip())
        c = int(operands[1].strip())
        
        f.write('B.set_resevior(%d,%d,\'waste_reservior\')\n'%(r,c))
    elif opcode == 'output_reservior' and len(operands) == 2:
        r = int(operands[0].strip())
        c = int(operands[1].strip())        
        f.write('B.set_resevior(%d,%d,\'op_reservior\')\n'%(r,c))
        
    elif opcode == 'end':
        pass
    else:
        print 'Invalid Command:' + instr
        exit()   
            
        
def common(op_f):
    op_f.write('B.run_mixer()\n')
    op_f.write('B.advance_clock()\n')
    op_f.write('time.sleep(%f)\n' %sleep_time)
    op_f.write('print \'clock = %d \' %B.get_clock()\n')
    

def new_interpreter(filename):
    ip_f = open(filename,'r')
    op_f = open('output.py','w')
    
    header(ip_f,op_f)  
     
    c_time = 0      #start time     
    for line in ip_f:
        if not line.strip():
            continue            #skipping blank lines
        time = re.compile('\d+').match(line)
        if time == None:
            print 'Invalid syntax: ' + line
            exit()
        
        op_time = int(time.group())     #operation execution time
        if c_time > op_time:
            print 'Timing violation'
            return
        while c_time < op_time:
            common(op_f)
            c_time = c_time + 1
        
        c_time = c_time + 1  
          
        instr_line = re.compile('[a-z_]+\s*\([\s*\d+\s*,\s*]+\s*\w+\s*\)').findall(line)
        
        for instr in instr_line:
            gen(instr,op_f)
                
        common(op_f)
    
    #op_f.write('B.mainloop()\n')
    ip_f.close()
    op_f.close() 
    



def callback_fileopen():
    #print 'In callback()'
    global ip_file
    ip_file= askopenfilename(filetypes=(("Program files", "*.dmfb"),("All files", "*.*") ))

    
def callback_start():
    global sleep_time,ip_file
    
    if ip_file == '':
        showinfo('No', 'Sorry, no input file')
        return
    
    global clock
    sleep_time = clock.get()/1000.0
    
    new_interpreter(ip_file)
    ip_file = ''    
    subprocess.call(["python", "output.py"])  

   
root = Tk()  
root.title('Biochip Simulator')
root.resizable(0,0)
content = Frame(root,width=200, height =200)
content.grid()
for i in range(3):
    content.rowconfigure(i,pad = 2)
    content.columnconfigure(i,pad = 2)

Button(content, text='Load program', width=30, command=callback_fileopen).grid(row=0,columnspan=2,pady=10)
Label(content, text="Time Step (ms): ").grid(row=1,column=0)
spinval = StringVar()
clock = Scale(content, from_=100, to=2000, orient=HORIZONTAL, length =150)
clock.grid(row=1,column=1)
clock.set(1000) 
Button(content, text='Start', command=callback_start).grid(row=2,column=1,rowspan = 3,sticky = E)
root.mainloop()



