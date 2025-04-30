'''
Created on 25-Jun-2013
@author: Sukanta
'''
from Tkinter import *
import time 
import random


cell_size = 36
inactive_cell_color = "#B0F5C6"
active_cell_color = "#FFFFFF"
active_mixer_color = "#B0DBF5"
back_color = "#000000"
waste_reservior_color = "#000000"
output_reservior_color = "#230CF2"

reservoir_colors = [waste_reservior_color,output_reservior_color]
intermediate_color = []

def make_list(size):
    """create a list of size number of val"""
    mylist = []
    for i in range(size):
        mylist.append(cell())
    return mylist

def create_matrix(rows, cols):
    """create a 2D matrix as a list of rows number of lists where the lists are cols in size resulting matrix contains val"""
    matrix = []
    for i in range(rows):
        matrix.append(make_list(cols))
    return matrix

def get_random_color(mixed_droplet=False):
    r = hex(random.randint(20,150))[2:].zfill(2)
    g = hex(random.randint(50,190))[2:].zfill(2)
    b = hex(random.randint(10,230))[2:].zfill(2)
    color = '#'+str(r)+str(g)+str(b)
    if mixed_droplet == False:
        while color in reservoir_colors:
            color = get_random_color()
        reservoir_colors.append(color)
    else:
        while color in reservoir_colors or color in intermediate_color:
            color = get_random_color(mixed_droplet=True)
        intermediate_color.append(color)
    
    return color



class cell:
    def __init__(self):
        self.electrode = None   # canvas for drawing droplet
        self.type = None        #type = op_reservior / waste_reservior / reagent / inactive / active   active -> biochip cell
        self.conc = []

class active_mixers:
    def __init__(self,t,start,end,r1,c1,r2,c2):
        self.mtype = t          # mtype is the type of mixer horizontal(14) = 1 * 4, vertical(41) = 4 * 1
        self.state = 0          # state indicates the mixer configuration [0-6]
        self.s_time = start     # start time of mixer
        self.e_time = end       # end time of mixer
        self.d1r = r1           # location of first droplet  
        self.d1c = c1
        self.d2r = r2           # location of first droplet  
        self.d2c = c2
        self.cdr = -1           # location of combined droplet  
        self.cdc = -1
        self.change_color = True 
    def show(self):
        print '----------------------------------'
        print 'mixer type: %d'%self.mtype
        print 'mixer state: %d'%self.state
        print 'mixer start: %d end: %d' %(self.s_time,self.e_time)
        print 'D1: (%d,%d)'%(self.d1r,self.d1c)
        print 'D2: (%d,%d)'%(self.d2r,self.d2c)
        print 'CD: (%d,%d)'%(self.cdr,self.cdc)
        

class Biochip(Frame): 
    def __init__(self, parent,r,c):
        Frame.__init__(self, parent)
        self.parent = parent
        parent.resizable(0,0)
        self.parent.title('SymBiochip')
        self.row = r
        self.col = c 
        self.biochip = create_matrix(self.row+2,self.col+2)    # canvas for each electrode
        
        self.mixer_table = []
        self.clock = 0
        self.grid()                                                 # set grid layout
        self.__arch_layout()
        
        
    def advance_clock(self):
        self.clock = self.clock + 1
    
    def get_clock(self):
        return self.clock
    
    def set_clock(self,t):
        self.clock = t
        
#    def callback_quit(self):
#        self.parent.quit()


    def __arch_layout(self):
        for i in range(self.row+2):
            self.rowconfigure(i, pad=1)
        for j in range(self.col+2):
            self.columnconfigure(j, pad=1)
                
        # First Row
        for j in range(self.col+2):
            self.biochip[0][j].electrode = Canvas(self, bg=inactive_cell_color,height=cell_size, width=cell_size,highlightbackground=back_color)
            self.biochip[0][j].electrode.grid(row=0,column=j)
            self.biochip[0][j].type = 'inactive'
        
           
        for i in range(1,self.row+1):
            #First Column
            self.biochip[i][0].electrode = Canvas(self, bg=inactive_cell_color,height=cell_size, width=cell_size,highlightbackground=back_color)
            self.biochip[i][0].electrode.grid(row=i,column=0)
            self.biochip[i][0].type = 'inactive'
            #Electrode 
            for j in range(1,self.col+1):
                self.biochip[i][j].electrode = Canvas(self, bg=active_cell_color,height=cell_size, width=cell_size,highlightbackground=back_color)
                self.biochip[i][j].electrode.grid(row=i,column=j)
                self.biochip[i][j].type = 'active'
            #Last Column
            self.biochip[i][self.col+1].electrode = Canvas(self, bg=inactive_cell_color,height=cell_size, width=cell_size,highlightbackground=back_color)
            self.biochip[i][self.col+1].electrode.grid(row=i,column=self.col+1)
            self.biochip[i][self.col+1].type = 'inactive'
        
        #last row
        for j in range(self.col+2):
            self.biochip[self.row+1][j].electrode = Canvas(self, bg=inactive_cell_color,height=cell_size, width=cell_size,highlightbackground=back_color)
            self.biochip[self.row+1][j].electrode.grid(row=self.row+1,column=j)
            self.biochip[self.row+1][j].type = 'inactive'
            
        #Button(self.parent, text='Quit', command=self.callback_quit).grid()    
        # program load and set step time
        
        
    def set_resevior(self,x,y,reservior_type,name = None):
        
        if self.__droplet_loc_is_valid(x,y) == False :
            print 'dispense_droplet-1: Cannot dispense droplet from wrong reservoir (%d,%d)\n' %(x,y)
            return
        
        # Indicates from which reservoir colour can be drawn
        color_row = x
        color_col = y
        if x == 1:
            color_row = x - 1
        elif x == self.row:
            color_row = x + 1
        elif y == 1:
            color_col = y - 1
        elif y == self.col:
            color_col = y + 1
        else:
            pass
        
        if reservior_type == 'waste_reservior':    #waste reservior
            self.biochip[color_row][color_col].electrode.configure(bg = waste_reservior_color)
            self.biochip[color_row][color_col].electrode.create_text(cell_size/2, cell_size/2,fill=active_cell_color,text='W')
            
        elif reservior_type == 'op_reservior':    #output reservior
            self.biochip[color_row][color_col].electrode.configure(bg = output_reservior_color)
            self.biochip[color_row][color_col].electrode.create_text(cell_size/2, cell_size/2,fill=active_cell_color,text='O/P')
            
        else:
            self.biochip[color_row][color_col].electrode.configure(bg = get_random_color())
            if name == None:
                print 'set_reservior: reagent name should be present'
                return
        self.biochip[color_row][color_col].electrode.create_text(cell_size/2, cell_size/2,fill=active_cell_color,text=name)
            
        self.biochip[color_row][color_col].type = reservior_type
        pass
        
        
    def dispense_droplet(self,x,y):
       
        if self.__droplet_loc_is_valid(x,y) == False :
            print 'dispense_droplet-1: Cannot dispense droplet from wrong reservoir (%d,%d)\n' %(x,y)
            return
        
        # Indicates from which reservoir colour can be drawn
        color_row = x
        color_col = y
        if x == 1:
            color_row = x - 1
        elif x == self.row:
            color_row = x + 1
        elif y == 1:
            color_col = y - 1
        elif y == self.col:
            color_col = y + 1
        else:
            print 'dispense_droplet-2 : dispenser location  (%d,%d) is wrong\n' %(x,y)
            return
        
        if self.biochip[color_row][color_col].type != "reagent":
            print 'dispense_droplet-3 : Cannot dispense droplet from wrong reservoir (%d,%d)\n' %(x,y)
            return
        #get the colour attribute
        color = self.biochip[color_row][color_col].electrode.cget('bg') 
        #create droplet
        self.biochip[x][y].electrode.create_oval(cell_size/4, cell_size/4, cell_size*3/4, cell_size*3/4, fill = color, width = 1)  
        self.biochip[x][y].electrode.update()
    
    def __droplet_loc_is_valid(self,x,y):
        if x not in range(1,self.row+1):
            return False
        if y not in range(1,self.col+1):
            return False
        
    def __get_id_width_fill_of_droplet(self,r,c):
        
        ID = self.biochip[r][c].electrode.find_all()
        if len(ID) == 0:
            print '__get_id_width_fill_of_droplet: No droplet is in position (%d,%d)'%(r,c)
            return
        
        w = self.biochip[r][c].electrode.itemcget(ID[0],'width')
        c = self.biochip[r][c].electrode.itemcget(ID[0],'fill')
        
        return ID[0],w,c
        
        
    def move_droplet(self,xold,yold,xnew,ynew):        
        if self.__droplet_loc_is_valid(xold,yold) == False:
            print 'Initial droplet location is not valid'
            return
        if self.__droplet_loc_is_valid(xnew,ynew) == False:
            print 'Final droplet location is not valid'
            return  
        
        # Check for valid 1 cell droplet movement
        pass 
            
        #get the id,color,width of droplet (xold,yold)
        (ID, w, c) = self.__get_id_width_fill_of_droplet(xold,yold)
                            
        # delete old droplet
        self.biochip[xold][yold].electrode.delete(ID)
        self.biochip[xold][yold].electrode.update()
        # create new droplet and preserve its width, fill
        if w == str(1.0):  # 1X droplet
            self.biochip[xnew][ynew].electrode.create_oval(cell_size/4, cell_size/4, cell_size*3/4, cell_size*3/4, fill = c, width = w)
            self.biochip[xnew][ynew].electrode.update()
        else:
            self.biochip[xnew][ynew].electrode.create_oval(1, 1, cell_size-1, cell_size-1, fill = c, width = w)
            self.biochip[xnew][ynew].electrode.update()    
        
        return 
    
    def instantiate_mixer(self,r1,c1,r2,c2,mixing_time): 
        if self.__droplet_loc_is_valid(r1, c1) == False:
            print 'instantiate_mixer: droplet location is invalid'
            return
        if self.__droplet_loc_is_valid(r2, c2) == False:
            print 'instantiate_mixer: droplet location is invalid'
            return
        # Find the type of mixer (type = 14)
        #|+++|+++|+++|+++|
        #| D1|   |   | D2|
        #|+++|+++|+++|+++|
        if r1 == r2 and abs(c1 - c2) == 3:   # 1*4 mixer
            if c1 < c2:
                mixer = active_mixers(14,self.clock,self.clock + mixing_time,r1,c1,r2,c2)   #instantiate
            else:
                mixer = active_mixers(14,self.clock,self.clock + mixing_time,r2,c2,r1,c1)
                
            self.mixer_table.append(mixer)      #register mixer
            
                
        #type = 41
        #++++++
        #| D1 |
        #++++++
        #|    |
        #++++++
        #|    |
        #++++++
        #| D2 |
        #++++++       
        elif c1 == c2 and abs(r1 - r2) == 3:    # 4*1 mixer
            if r1 < r2:
                mixer = active_mixers(41,self.clock,self.clock + mixing_time,r1,c1,r2,c2)
            else:
                mixer = active_mixers(41,self.clock,self.clock + mixing_time,r2,c2,r1,c1)
                
            self.mixer_table.append(mixer)      #register mixer
            
            # render mixer
            for i in range(r1,r2+1,1):
                self.biochip[i][c1].electrode.configure(bg=active_mixer_color)
                self.biochip[i][c1].electrode.update()
                
        else:
            print 'instantiate_mixer: mixer type is invalid'
            return
        
    def __delete_mixer(self,mixer):
        #print 'In delete_mixer'
        if mixer.mtype == 14:
            for i in range(mixer.d1c,mixer.d2c+1,1):
                self.biochip[mixer.d1r][i].electrode.configure(bg=active_cell_color)
                self.biochip[mixer.d1r][i].electrode.update()
        elif mixer.mtype == 41:
            for i in range(mixer.d1r,mixer.d2r+1,1):
                self.biochip[i][mixer.d1c].electrode.configure(bg=active_cell_color)
                self.biochip[i][mixer.d1c].electrode.update()
        else:
            print 'delete_mixer: Invalid mixer type'
            
    def delete_droplet(self,x,y):
        if self.__droplet_loc_is_valid(x,y) == False :
            print 'delete_droplet-0: Cannot delete droplet in (%d,%d)\n' %(x,y)
            return
        
        # Indicates from which reservoir colour can be drawn
        color_row = x
        color_col = y
        if x == 1:
            color_row = x - 1
        elif x == self.row:
            color_row = x + 1
        elif y == 1:
            color_col = y - 1
        elif y == self.col:
            color_col = y + 1
        else:
            pass
        
        if self.biochip[color_row][color_col].type not in  ['op_reservior','waste_reservior']:
            print 'delete_droplet-1: No reservior is in position (%d,%d)'%(x,y)
            return
                
        ID = self.biochip[x][y].electrode.find_all()
        if len(ID) == 0:
            print 'delete_droplet-2: No droplet is in position (%d,%d)'%(x,y)
            return
        self.biochip[x][y].electrode.delete(ID[0])
        self.biochip[x][y].electrode.update() 
           
    def delete_mixer_droplet(self,r,c):        
        ID = self.biochip[r][c].electrode.find_all()
        if len(ID) == 0:
            print 'delete_droplet-2: No droplet is in position (%d,%d)'%(r,c)
            return
        self.biochip[r][c].electrode.delete(ID[0])
        self.biochip[r][c].electrode.update()
    
    def __mixer_41(self,mixer):
        if self.clock == mixer.s_time:  #run mixer next clock after instantiation
            return
        if mixer.state == 0:
            # render mixer
            for i in range(mixer.d1r,mixer.d2r+1,1):
                self.biochip[i][mixer.d1c].electrode.configure(bg=active_mixer_color)
                self.biochip[i][mixer.d1c].electrode.update()
               
            #+++++
            #| o |
            #+++++
            #|   |
            #+++++
            #|   |
            #+++++
            #| o |
            #+++++
            self.move_droplet(mixer.d1r, mixer.d1c, mixer.d1r+1, mixer.d1c)
            mixer.d1r = mixer.d1r + 1
                    
            self.move_droplet(mixer.d2r, mixer.d2c, mixer.d2r - 1, mixer.d2c)
            mixer.d2r = mixer.d2r - 1
        elif mixer.state == 1:
            #+++++
            #|   |
            #+++++
            #| o |
            #+++++
            #| o |
            #+++++
            #|   |
            #+++++
            self.delete_mixer_droplet(mixer.d2r, mixer.d2c)
            mixer.d2r = -1
            mixer.d2c = -1
            
            if mixer.change_color == True:  #First mixing - change color
                c = get_random_color(mixed_droplet=True)
                mixer.change_color = False
            else:       #Subsequent mixing - donot change color
                (ID,w,c) = self.__get_id_width_fill_of_droplet(mixer.d1r,mixer.d1c)  
                                                
            self.delete_mixer_droplet(mixer.d1r, mixer.d1c)
            self.biochip[mixer.d1r][mixer.d1c].electrode.create_oval(1, 1, cell_size-1, cell_size-1, fill = c, width = 2)
            self.biochip[mixer.d1r][mixer.d1c].electrode.update()
            mixer.cdr = mixer.d1r
            mixer.cdc = mixer.d1c
            mixer.d1r = -1
            mixer.d1c = -1
        elif mixer.state == 2:
            #+++++
            #|   |
            #+++++
            #| @ |
            #+++++
            #|   |
            #+++++
            #|   |
            #+++++
            self.move_droplet(mixer.cdr, mixer.cdc, mixer.cdr+1, mixer.cdc)
            mixer.cdr = mixer.cdr + 1
        elif mixer.state == 3:
            #+++++
            #|   |
            #+++++
            #|   |
            #+++++
            #| @ |
            #+++++
            #|   |
            #+++++
            self.move_droplet(mixer.cdr, mixer.cdc, mixer.cdr - 1, mixer.cdc)
            mixer.cdr = mixer.cdr - 1
        elif mixer.state == 4:
            #+++++
            #|   |
            #+++++
            #| @ |
            #+++++
            #|   |
            #+++++
            #|   |
            #+++++
        
            (ID,w,c) = self.__get_id_width_fill_of_droplet(mixer.cdr,mixer.cdc)
            self.delete_mixer_droplet(mixer.cdr, mixer.cdc)
                    
            self.biochip[mixer.cdr][mixer.cdc].electrode.create_oval(cell_size/4, cell_size/4, cell_size*3/4, cell_size*3/4, fill = c)
            self.biochip[mixer.cdr][mixer.cdc].electrode.update()
            mixer.d1r = mixer.cdr
            mixer.d1c = mixer.cdc
                    
            self.biochip[mixer.cdr+1][mixer.cdc].electrode.create_oval(cell_size/4, cell_size/4, cell_size*3/4, cell_size*3/4, fill = c)
            self.biochip[mixer.cdr+1][mixer.cdc].electrode.update()
            mixer.d2r = mixer.cdr + 1
            mixer.d2c = mixer.cdc 
                    
            mixer.cdr = -1
            mixer.cdc = -1
        elif mixer.state == 5:
            #+++++
            #|   |
            #+++++
            #| o |
            #+++++
            #| o |
            #+++++
            #|   |
            #+++++
            self.move_droplet(mixer.d1r, mixer.d1c, mixer.d1r - 1, mixer.d1c)
            mixer.d1r = mixer.d1r - 1
            self.move_droplet(mixer.d2r, mixer.d2c, mixer.d2r + 1, mixer.d2c)
            mixer.d2r = mixer.d2r + 1
        else:
            print 'run_mixer: mixer is in invalid state'
            return
                
        mixer.state = (mixer.state + 1) % 6
    
    def __mixer_14(self,mixer):
        if self.clock == mixer.s_time:  #run mixer next clock after instantiation
            return
        if mixer.state == 0:
            # render mixer
            for i in range(mixer.d1c,mixer.d2c+1,1):
                self.biochip[mixer.d1r][i].electrode.configure(bg=active_mixer_color)
                self.biochip[mixer.d1r][i].electrode.update()
               
            #|+++|+++|+++|+++|
            #| o |   |   | o |
            #|+++|+++|+++|+++|
            self.move_droplet(mixer.d1r, mixer.d1c, mixer.d1r, mixer.d1c+1)
            mixer.d1c = mixer.d1c + 1
                    
            self.move_droplet(mixer.d2r, mixer.d2c, mixer.d2r, mixer.d2c-1)
            mixer.d2c = mixer.d2c - 1
        elif mixer.state == 1:
            #|+++|+++|+++|+++|
            #|   | o | o |   |
            #|+++|+++|+++|+++|
            self.delete_mixer_droplet(mixer.d2r, mixer.d2c)
            mixer.d2r = -1
            mixer.d2c = -1
            
            if mixer.change_color == True:  #First mixing - change color
                c = get_random_color(mixed_droplet=True)
                mixer.change_color = False
            else:       #Subsequent mixing - donot change color
                (ID,w,c) = self.__get_id_width_fill_of_droplet(mixer.d1r,mixer.d1c) 
                                               
            self.delete_mixer_droplet(mixer.d1r, mixer.d1c)
            self.biochip[mixer.d1r][mixer.d1c].electrode.create_oval(1, 1, cell_size-1, cell_size-1, fill = c, width = 2)
            self.biochip[mixer.d1r][mixer.d1c].electrode.update()
            mixer.cdr = mixer.d1r
            mixer.cdc = mixer.d1c
            mixer.d1r = -1
            mixer.d1c = -1
        elif mixer.state == 2:
            #|+++|+++|+++|+++|
            #|   | @ |   |   |
            #|+++|+++|+++|+++|
            self.move_droplet(mixer.cdr, mixer.cdc, mixer.cdr, mixer.cdc+1)
            mixer.cdc = mixer.cdc + 1
        elif mixer.state == 3:
            #|+++|+++|+++|+++|
            #|   |   | @ |   |
            #|+++|+++|+++|+++|
            self.move_droplet(mixer.cdr, mixer.cdc, mixer.cdr, mixer.cdc-1)
            mixer.cdc = mixer.cdc - 1
        elif mixer.state == 4:
            #|+++|+++|+++|+++|
            #|   | @ |   |   |
            #|+++|+++|+++|+++|
        
            (ID,w,c) = self.__get_id_width_fill_of_droplet(mixer.cdr,mixer.cdc)
            self.delete_mixer_droplet(mixer.cdr, mixer.cdc)
                    
            self.biochip[mixer.cdr][mixer.cdc].electrode.create_oval(cell_size/4, cell_size/4, cell_size*3/4, cell_size*3/4, fill = c)
            self.biochip[mixer.cdr][mixer.cdc].electrode.update()
            mixer.d1r = mixer.cdr
            mixer.d1c = mixer.cdc
                    
            self.biochip[mixer.cdr][mixer.cdc+1].electrode.create_oval(cell_size/4, cell_size/4, cell_size*3/4, cell_size*3/4, fill = c)
            self.biochip[mixer.cdr][mixer.cdc+1].electrode.update()
            mixer.d2r = mixer.cdr
            mixer.d2c = mixer.cdc + 1
                    
            mixer.cdr = -1
            mixer.cdc = -1
        elif mixer.state == 5:
            #|+++|+++|+++|+++|
            #|   | o | o |   |
            #|+++|+++|+++|+++|
            self.move_droplet(mixer.d1r, mixer.d1c, mixer.d1r, mixer.d1c - 1)
            mixer.d1c = mixer.d1c - 1
            self.move_droplet(mixer.d2r, mixer.d2c, mixer.d2r, mixer.d2c + 1)
            mixer.d2c = mixer.d2c + 1
        else:
            print 'run_mixer: mixer is in invalid state'
            return
                
        mixer.state = (mixer.state + 1) % 6    
        
    def run_mixer(self):
        for mixer in self.mixer_table:
            if mixer.mtype == 14:   #1*4 horizontal mixer
                self.__mixer_14(mixer)
            elif mixer.mtype == 41:  #4*1 vertical mixer
                self.__mixer_41(mixer)
            else:
                print 'run_mixer: Invalid mixer type'
                
        
        # delete expired mixers
        active_mixers = []
        for mixer in self.mixer_table:       
            if self.clock == mixer.e_time:
                self.__delete_mixer(mixer)
            else:
                active_mixers.append(mixer)
        
        self.mixer_table = active_mixers 
    
    
#root = Tk()
#B = Biochip(root,6,10)
#root.mainloop()