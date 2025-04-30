'''
Created on 29-Jun-2013
@author: sukanta
'''

#from Tkinter import ttk
import subprocess as sp
import os
from Biochip import  *
from Biochip_V import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
import tkinter.messagebox
import _thread
import threading
import time



myfont = ("Arial", 10, "bold")

sleep_time = 0
clock = None        #Slider Handle
ip_file = ''

root = None
B = None
B_V = None
btnStart = None
CheckVarPause = None


def header(ip_f):
    global root, B, B_V  
    
    #--------------------dimension------------------------------------    
    line = ip_f.readline() 
    while not line.strip():
        line = ip_f.readline() 
               
    token = line.split()
    if token[0] != 'dimension' or len(token) != 3:
        print ('First line should be \'dimension m n\'')
        sys.exit()
    else:  
        root = Tk()
        (row,col)= (int(token[1]),int(token[2]))
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
    #---------------------Instantiate--------------------------------------    
        
    B = Biochip(root,row,col,accuracy)      # instantiate gui engine
    B_V =  Biochip_V(row,col,accuracy)      # instantiate verification engine
    
    #---------------process reservoir descriptions-----------------------    
    line = ip_f.readline()
    while not line.strip():
            line = ip_f.readline() 
    
    instr_line = re.compile('[a-z_]+\s*\([\s*\d+\s*,\s*]+\s*\w+\s*\)').findall(line)
    for instr in instr_line:
        obj = re.compile('[a-z_]+').match(instr)
        if obj == None:
            print ('Invalid syntax: ' + instr)
            sys.exit() 
        print (instr)
        opcode = obj.group()    
        operands = re.compile('(\d+|\w+)').findall(instr[obj.end() + 1 :])
        if opcode == 'reagent' and len(operands) >= 3 and len(operands) % 2 == 1:
            reagent_dispenser_list = []
            for i in range(0,len(operands) - 1,2):
                r = int(operands[i].strip())
                c = int(operands[i+1].strip())
                reagent_dispenser_list.append((r,c))
            
            reagent_name = operands[len(operands) - 1]
            B_V.verify_set_reagent_reservior(reagent_dispenser_list,reagent_name)
            B.set_reagent_resevior(reagent_dispenser_list,reagent_name)
        elif opcode == 'waste_reservoir' and len(operands) == 2:
            r = int(operands[0].strip())
            c = int(operands[1].strip())    
            B_V.verify_set_resevior(r,c,'waste_reservoir')    
            B.set_resevior(r,c,'waste_reservoir')
        elif opcode == 'output_reservoir' and len(operands) == 2:
            r = int(operands[0].strip())
            c = int(operands[1].strip()) 
            B_V.verify_set_resevior(r,c,'op_reservoir')         
            B.set_resevior(r,c,'op_reservoir')  
        else:
            print ('Invalid Command:' + instr)
            sys.exit()
    # ratio assignment to reagents
    B.assign_ratio_to_reagents()
    #---------------------------------------------------------------------
    print ('clock = %d ' %B.get_clock()   )
    
#----------------------------run gui for every instruction----------------        
def gen(instr):
    global  B
    obj = re.compile('[a-z_]+').match(instr)
    if obj == None:
        print ('Invalid syntax: ' + instr)
        sys.exit() 
    print (instr)
    opcode = obj.group()    
    operands = re.compile('(\d+|\w+)').findall(instr[obj.end() + 1 :])
    
    if opcode == 'dispense' and len(operands) == 2:
        r = int(operands[0].strip())
        c = int(operands[1].strip())
        B.dispense_droplet(r,c)
    elif opcode == 'mix_split' and len(operands) == 5:
        r1 = int(operands[0].strip())
        c1 = int(operands[1].strip())
        r2 = int(operands[2].strip())
        c2 = int(operands[3].strip())
        t = int(operands[4].strip())
        B.instantiate_mixer(r1, c1, r2, c2, t)
    elif opcode == 'move' and len(operands) == 4:
        rold = int(operands[0].strip())
        cold = int(operands[1].strip())
        rnew = int(operands[2].strip())
        cnew = int(operands[3].strip())
        B.move_droplet(rold, cold, rnew, cnew)
    elif opcode == 'waste' and len(operands) == 2:
        r = int(operands[0].strip())
        c = int(operands[1].strip())
        B.delete_droplet(r, c)
    elif opcode == 'output' and len(operands) == 2:
        r = int(operands[0].strip())
        c = int(operands[1].strip())
        B.delete_droplet(r, c)   
    elif opcode == 'end':
        pass   
    else:
        print ('Invalid Command:' + instr)
        sys.exit()   
            
#----------------------runs every clock---------------------------------------        
def common():
    global B,B_V
    B.run_mixer()
    B.advance_clock()
    time.sleep(sleep_time)
    # show mixing graph - optional
    B_V.show_mixing_graph()     
    print ('clock = %d ' %B.get_clock())
    

def new_interpreter(filename):
    global B_V, CheckVarPause, sleep_time, B
    ip_f = open(filename,'r')
    
    header(ip_f)  
     
    c_time = 0                  #start time     
    for line in ip_f:           #read each line
        if not line.strip():    #skipping blank lines
            continue            
        
        B_V.verify_line(line)   # validate instructions
        #extract time from instruction line
        t = re.compile('\d+').match(line)
        if t == None:
            print ('Invalid syntax: ' + line)
            sys.exit()
        
        op_time = int(t.group())     #operation execution time
        while c_time < op_time:
            common()
            c_time = c_time + 1        
            
        # Paused ?
        while CheckVarPause.get():
            #print CheckVarPause.get()
            time.sleep(1)
            
        
        # extract each instructions  
        instr_line = re.compile('[a-z_]+\s*\([\s*\d+\s*,\s*]+\s*\w+\s*\)').findall(line)
        # run
        for instr in instr_line:
            gen(instr)                
        common()
        c_time = c_time + 1             #execution of instructions is finished - increase clock
    ip_f.close()
    B_V.show_mixing_graph()   



def callback_fileopen():
    global ip_file
    ip_file= askopenfilename(filetypes=(("Program files", "*.dmfb"),("All files", "*.*") ))

class myThread (threading.Thread):
    def __init__(self,  fname):
        threading.Thread.__init__(self)        
        self.filename = fname
        
    def run(self):
        global  B 
        print ("Starting SimBioSys" )
        new_interpreter(self.filename)
        B.mainloop()
    
def callback_start():
    global sleep_time,ip_file,clock,btnStart
    
    if ip_file == '':
        showinfo('Oops!!', 'No input file')
        return
    
    sleep_time = clock.get()/1000.0
    btnStart.configure(state = DISABLED)
    # start program
    #new_interpreter(ip_file)
    btnStart.configure(state = NORMAL)
    try:
        thread = myThread(ip_file)
        thread.start()
    except:
        print ("Error: unable to start thread")
    
def callback_about():
    showinfo('Developed by -', 'Sukanta Bhattacharjee\nWeb: www.isical.ac.in/~sukanta_r')   
    
def callback_scale(event = None):
    global sleep_time
    sleep_time = int(event)/1000.0
    
def callback_pause():
    print ("hello")
    
# main program
def main():
    global clock,root, btnStart, CheckVarPause   
    root = Tk()  
    root.title('Biochip Simulator')
    root.resizable(0,0)
    content = Frame(root,width=200, height =200, bg = "#660A26",bd=3)
    content.grid()
    for i in range(3):
        content.rowconfigure(i,pad = 2)
        content.columnconfigure(i,pad = 2)
    
    Button(content, text='Load program',relief=RAISED,bd=4, width=30, bg = "#820E31", fg = "white",\
           activebackground="#820E31", activeforeground="#9BF1F2",font=myfont,\
           command=callback_fileopen).grid(row=0,columnspan=3,pady=10)
    Label(content, bg = "#660A26",relief=GROOVE,bd=2,fg="white",text="Time Step (ms): ",font=myfont).grid(row=1,column=0)
    clock = Scale(content,command = callback_scale, from_=100, to=3000, orient=HORIZONTAL, \
                  length =150,bd=2,relief=RAISED,bg = "#820E31",fg="white",troughcolor="white",\
                  font=myfont,activebackground="navy")
    clock.grid(row=1,column=1,columnspan=2,pady = 10)
    clock.set(500) 
    btnStart = Button(content, text='Start',relief=RAISED,bd=4,bg = "#820E31", fg = "white",\
                      activebackground="#820E31",activeforeground="#9BF1F2",font=myfont, command=callback_start)
    btnStart.grid(row=2,column=2,rowspan = 3,sticky = E)
    Button(content, text='About',relief=RAISED,bd=4,bg = "#820E31", fg = "white",activebackground="#820E31",\
           activeforeground="#9BF1F2",font=myfont, command=callback_about).grid(row=2,column=0,rowspan = 1,sticky = W)
    
    CheckVarPause = IntVar()
    Checkbutton(content, text = "Pause", variable = CheckVarPause, bg = "#820E31", fg = "white", selectcolor='brown',\
                font=myfont, onvalue = 1, offvalue = 0, activebackground="#820E31",activeforeground="#9BF1F2", \
                height=2, width = 5,relief=RAISED, bd = 4, command = callback_pause).grid(row=2,column=1,sticky = E)
    root.mainloop()
    
if __name__ == '__main__':
    subprocess.Popen(["evince","mg.pdf"],shell=True)
    main()
