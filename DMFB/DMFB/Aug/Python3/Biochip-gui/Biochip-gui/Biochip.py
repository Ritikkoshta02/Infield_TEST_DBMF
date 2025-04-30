'''
Created on 25-Jun-2013
@author: Sukanta
'''
from tkinter import *
import random


cell_size = 35
inactive_cell_color = "#B0F5C6"
active_cell_color = "#FFFFFF"
active_mixer_color = "#B0DBF5"
back_color = "#000000"
waste_reservior_color = "#000000"
output_reservior_color = "#230CF2"
tooltipfont = ("Arial", 12, "bold")

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

class ToolTip( Toplevel ):
    """ Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the ToolTip constructor
    """ 
    def __init__( self, wdgt, msgFunc=None):
        """ Initialize the ToolTip        
        Arguments:
          wdgt: The widget this ToolTip is assigned to
          msgFunc: A function that retrieves a string to use as the ToolTip text
        """
        self.wdgt = wdgt
        # The parent of the ToolTip is the parent of the ToolTips widget
        self.parent = self.wdgt.master  
        # Initalize the Toplevel                    
        Toplevel.__init__( self, self.parent, bg='black', padx=1, pady=1 )  
        # Hide initially    
        self.withdraw()  
        # The ToolTip Toplevel should have no frame or title bar                                                        
        self.overrideredirect( True )
        self.msgFunc = msgFunc       
        # create message box that shows the ratio of reagents  
        self.Msg = Message(self,text="",relief=RAISED,bd=1,bg='#000000',fg="#FFFFFF",font = tooltipfont,aspect=1500 )
        self.Msg.grid() 
        # Add bindings to the widget.  This will NOT override bindings that the widget already has                                            
        self.wdgt.bind( '<Enter>', self.show, '+' )                                    
        self.wdgt.bind( '<Leave>', self.hide, '+' )
        self.wdgt.bind( '<Motion>', self.move, '+' )       
        
    def show( self,event=None ):
        """ Displays the ToolTip """
        ratio = self.msgFunc()
        if ratio == None:
            self.withdraw() 
        else:
            self.Msg.config(text=ratio)
            self.deiconify()
            
    def move( self, event ):
        """ Processes motion within the widget.        
        Argument -> event: The event that called this function """
        
        # Offset the ToolTip 10x10 pixes southwest of the pointer
        self.geometry( '+%i+%i' % (event.x_root+10, event.y_root+10 ))
        ratio = self.msgFunc()
        if ratio == None:
            self.withdraw() 
        else:
            self.Msg.config(text=ratio)
            self.deiconify()
            
    def hide( self, event=None ):
        """ Hides the ToolTip.  Usually this is caused by leaving the widget        
         event: The event that called this function"""
        self.withdraw()

class cell:
    def __init__(self):
        self.electrode = None   # canvas for drawing droplet
        self.type = None        #type = op_reservior / waste_reservior / reagent / inactive / active   active -> biochip cell
        self.conc = []
        self.RID = -1           # denote its position in ratio -- valid for type = reagent only  
               
        
    def show_ratio(self):       # String shown when pointer is in cell
        if self.conc == []:
            return None
        else:
            ratio = str(self.conc[0])
            for i in range(1,len(self.conc)):
                ratio = ratio + ':' + str(self.conc[i])
            return ratio

class active_mixers:
    def __init__(self,t,start,end,r1,c1,r2,c2):
        self.mtype = t              # mtype is the type of mixer horizontal(14) = 1 * 4, vertical(41) = 4 * 1
        self.state = 0              # state indicates the mixer configuration [0-6]
        self.s_time = start         # start time of mixer
        self.e_time = end           # end time of mixer
        self.d1r = r1               # location of first droplet  
        self.d1c = c1
        self.d2r = r2               # location of first droplet  
        self.d2c = c2
        self.cdr = -1               # location of combined droplet  
        self.cdc = -1
        self.change_color = True    # change_color is used in mixing operation for changing mixed droplet color
        
    def show(self):
        print ('----------------------------------')
        print ('mixer type: %d'%self.mtype)
        print ('mixer state: %d'%self.state)
        print ('mixer start: %d end: %d' %(self.s_time,self.e_time))
        print ('D1: (%d,%d)'%(self.d1r,self.d1c))
        print ('D2: (%d,%d)'%(self.d2r,self.d2c))
        print ('CD: (%d,%d)'%(self.cdr,self.cdc))
        print ('----------------------------------')
        

class Biochip(Frame): 
    def __init__(self, parent,r,c,n):
        Frame.__init__(self, parent)
        self.parent = parent
        self.row = r
        self.col = c
        self.accuracy = n 
        self.biochip = create_matrix(self.row+2,self.col+2)     # canvas for each electrode        
        self.mixer_table = []                                   # active mixers
        self.clock = 0
        self.grid()                                             # set grid layout
        self.__arch_layout()
        self.__ID = -1                                          # indicates the number of reagents
        
        self.parent.resizable(0,0)
        self.parent.title('SimBioSys')
        
        
        
    # get position for new sample in ratio - reagent only
    def __get_ID(self):
        self.__ID = self.__ID + 1
        return self.__ID
        
    def advance_clock(self):
        self.clock = self.clock + 1
    
    def get_clock(self):
        return self.clock
    
    def set_clock(self,t):
        self.clock = t

    # Create biochip layout 
    def __arch_layout(self):
        for i in range(self.row+2):
            self.rowconfigure(i, pad=1)
        for j in range(self.col+2):
            self.columnconfigure(j, pad=1)
                
        # First Row
        for j in range(self.col+2):
            self.biochip[0][j].electrode = Canvas(self, bg=inactive_cell_color,height=cell_size, \
                                                  width=cell_size,highlightbackground=back_color)
            ToolTip( self.biochip[0][j].electrode, msgFunc=self.biochip[0][j].show_ratio)
            self.biochip[0][j].electrode.grid(row=0,column=j)
            self.biochip[0][j].type = 'inactive'        
           
        for i in range(1,self.row+1):
            #First Column
            self.biochip[i][0].electrode = Canvas(self, bg=inactive_cell_color,height=cell_size, \
                                                  width=cell_size,highlightbackground=back_color)
            ToolTip( self.biochip[i][0].electrode, msgFunc=self.biochip[i][0].show_ratio)
            self.biochip[i][0].electrode.grid(row=i,column=0)
            self.biochip[i][0].type = 'inactive'
            #Electrode 
            for j in range(1,self.col+1):
                self.biochip[i][j].electrode = Canvas(self, bg=active_cell_color,height=cell_size, \
                                                      width=cell_size,highlightbackground=back_color)
                ToolTip( self.biochip[i][j].electrode, msgFunc=self.biochip[i][j].show_ratio)
                self.biochip[i][j].electrode.grid(row=i,column=j)
                self.biochip[i][j].type = 'active'
            #Last Column
            self.biochip[i][self.col+1].electrode = Canvas(self, bg=inactive_cell_color,height=cell_size, \
                                                           width=cell_size,highlightbackground=back_color)
            ToolTip( self.biochip[i][self.col+1].electrode, msgFunc=self.biochip[i][self.col+1].show_ratio)
            self.biochip[i][self.col+1].electrode.grid(row=i,column=self.col+1)
            self.biochip[i][self.col+1].type = 'inactive'
        
        #last row
        for j in range(self.col+2):
            self.biochip[self.row+1][j].electrode = Canvas(self, bg=inactive_cell_color,height=cell_size, \
                                                           width=cell_size,highlightbackground=back_color)
            ToolTip( self.biochip[self.row+1][j].electrode, msgFunc=self.biochip[self.row+1][j].show_ratio)
            self.biochip[self.row+1][j].electrode.grid(row=self.row+1,column=j)
            self.biochip[self.row+1][j].type = 'inactive'
            

        
            
    
    # setting a reservior in biochip     
    def set_reagent_resevior(self,reagent_dispenser_list,name):
        # Reagent reservior creation - requires ID for indicating position in ratio
        # Only one ID for each reagent
        new_id = self.__get_ID()
        color = get_random_color()
        for (x,y) in reagent_dispenser_list:
            # (color_row,color_col) indicates from which reservoir droplet colour to be drawn
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
            
            self.biochip[color_row][color_col].RID = new_id
            self.biochip[color_row][color_col].electrode.configure(bg = color)
            
            print ('ID(%d,%d) = %d' %(color_row,color_col,new_id))
            # set label and reservior type    
            self.biochip[color_row][color_col].electrode.create_text(cell_size/2, cell_size/2,fill=active_cell_color,text=name)            
            self.biochip[color_row][color_col].type = 'reagent'
    
            
    # setting waste and output reservior in biochip     
    def set_resevior(self,x,y,reservior_type):
        # (color_row,color_col) indicates from which reservoir droplet colour to be drawn
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
        
        if reservior_type == 'waste_reservoir':    #waste reservior
            self.biochip[color_row][color_col].electrode.configure(bg = waste_reservior_color)
            self.biochip[color_row][color_col].electrode.create_text(cell_size/2, cell_size/2,fill=active_cell_color,text='W')            
        elif reservior_type == 'op_reservoir':    #output reservior
            self.biochip[color_row][color_col].electrode.configure(bg = output_reservior_color)
            self.biochip[color_row][color_col].electrode.create_text(cell_size/2, cell_size/2,fill=active_cell_color,text='O/P')            
        else:
            pass
        
        # set reservior type            
        self.biochip[color_row][color_col].type = reservior_type
       
    
    # This function must be called after reservior allocations have been done
    # Creates initial ratio for reagents - total no of reagents is (self.__ID +1)
    def assign_ratio_to_reagents(self):
        for j in range(self.col+2):
            #top row
            if self.biochip[0][j].type == 'reagent':
                self.biochip[0][j].conc = [0]*(self.__ID + 1)
                self.biochip[0][j].conc[self.biochip[0][j].RID] = 2**self.accuracy
                print (self.biochip[0][j].conc)
            #bottom row
            if self.biochip[self.row+1][j].type == 'reagent':
                self.biochip[self.row+1][j].conc = [0]*(self.__ID + 1)
                self.biochip[self.row+1][j].conc[self.biochip[self.row+1][j].RID] = 2**self.accuracy
                print (self.biochip[self.row+1][j].conc)
        
        for i in range(1,self.row+1):
            #left column
            if self.biochip[i][0].type == 'reagent':
                self.biochip[i][0].conc = [0]*(self.__ID + 1)
                self.biochip[i][0].conc[self.biochip[i][0].RID] = 2**self.accuracy   
            #right column
            if self.biochip[i][self.col+1].type == 'reagent':
                self.biochip[i][self.col+1].conc = [0]*(self.__ID + 1)
                self.biochip[i][self.col+1].conc[self.biochip[i][self.col+1].RID] = 2**self.accuracy              

        
    def dispense_droplet(self,x,y):
        # (color_row,color_col) indicates from which reservoir colour can be drawn
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
    
        #get the colour attribute of (color_row,color_col)
        color = self.biochip[color_row][color_col].electrode.cget('bg') 
        #create new droplet
        self.biochip[x][y].electrode.create_oval(cell_size/4, cell_size/4, cell_size*3/4, cell_size*3/4, fill = color, width = 1)  
        self.biochip[x][y].electrode.update()
        #assign reagent to newly created droplet
        self.biochip[x][y].conc = self.biochip[color_row][color_col].conc[:] 
        
        
    def __get_id_width_fill_of_droplet(self,r,c):        
        ID = self.biochip[r][c].electrode.find_all()
        w = self.biochip[r][c].electrode.itemcget(ID[0],'width')
        c = self.biochip[r][c].electrode.itemcget(ID[0],'fill')
        
        return ID[0],w,c
        
        
    def move_droplet(self,xold,yold,xnew,ynew):                    
        #get the id,color,width of droplet (xold,yold)
        (ID, w, c) = self.__get_id_width_fill_of_droplet(xold,yold)
                            
        # delete old droplet
        D1_conc = self.biochip[xold][yold].conc[:] 
        self.biochip[xold][yold].electrode.delete(ID)
        self.biochip[xold][yold].electrode.update()
        self.biochip[xold][yold].conc = []
        
        # create new droplet and preserve its width, fill
        if w == str(1.0):   # 1X droplet - normal droplet
            self.biochip[xnew][ynew].electrode.create_oval(cell_size/4, cell_size/4, cell_size*3/4, cell_size*3/4, fill = c, width = w)
            self.biochip[xnew][ynew].electrode.update()
        else:               # 2X droplet - created during mixing operation
            self.biochip[xnew][ynew].electrode.create_oval(1, 1, cell_size-1, cell_size-1, fill = c, width = w)
            self.biochip[xnew][ynew].electrode.update()  
        
        #assign D-1 concentration to D-2      
        self.biochip[xnew][ynew].conc = D1_conc[:]
        return 
    
    def instantiate_mixer(self,r1,c1,r2,c2,mixing_time): 
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
            
        else:
            pass
        
    def __delete_mixer(self,mixer):
        # removes rendering of mixer region
        if mixer.mtype == 14:
            for i in range(mixer.d1c,mixer.d2c+1,1):
                self.biochip[mixer.d1r][i].electrode.configure(bg=active_cell_color)
                self.biochip[mixer.d1r][i].electrode.update()
        elif mixer.mtype == 41:
            for i in range(mixer.d1r,mixer.d2r+1,1):
                self.biochip[i][mixer.d1c].electrode.configure(bg=active_cell_color)
                self.biochip[i][mixer.d1c].electrode.update()
        else:
            pass
            
    def delete_droplet(self,x,y):                
        ID = self.biochip[x][y].electrode.find_all()
        self.biochip[x][y].electrode.delete(ID[0])
        self.biochip[x][y].electrode.update() 
        self.biochip[x][y].conc = []
           
    
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
            D2_conc = self.biochip[mixer.d2r][mixer.d2c].conc[:]
            self.delete_droplet(mixer.d2r, mixer.d2c)
            mixer.d2r = -1
            mixer.d2c = -1
            
            if mixer.change_color == True:  #First mixing - change color
                c = get_random_color(mixed_droplet=True)
                mixer.change_color = False
            else:       #Subsequent mixing - do not change color
                (ID,w,c) = self.__get_id_width_fill_of_droplet(mixer.d1r,mixer.d1c)  
            
            D1_conc = self.biochip[mixer.d1r][mixer.d1c].conc[:]                                              
            self.delete_droplet(mixer.d1r, mixer.d1c)
            self.biochip[mixer.d1r][mixer.d1c].electrode.create_oval(1, 1, cell_size-1, cell_size-1, fill = c, width = 2)
            self.biochip[mixer.d1r][mixer.d1c].electrode.update()
            mixed_conc = [D1_conc[i] + D2_conc[i] for i in range(len(D1_conc))]      #sum of D_1 and D_2 conc
            self.biochip[mixer.d1r][mixer.d1c].conc = mixed_conc[:]
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
            mixed_conc = self.biochip[mixer.cdr][mixer.cdc].conc[:]
            self.delete_droplet(mixer.cdr, mixer.cdc)
                    
            self.biochip[mixer.cdr][mixer.cdc].electrode.create_oval(cell_size/4, cell_size/4, cell_size*3/4, cell_size*3/4, fill = c)
            self.biochip[mixer.cdr][mixer.cdc].electrode.update()
            # Half of the concentration of mixed droplet
            self.biochip[mixer.cdr][mixer.cdc].conc = [mixed_conc[i]/2 for i in range(len(mixed_conc))]
            mixer.d1r = mixer.cdr
            mixer.d1c = mixer.cdc
                    
            self.biochip[mixer.cdr+1][mixer.cdc].electrode.create_oval(cell_size/4, cell_size/4, cell_size*3/4, cell_size*3/4, fill = c)
            self.biochip[mixer.cdr+1][mixer.cdc].electrode.update()
            # Half of the concentration of mixed droplet
            self.biochip[mixer.cdr+1][mixer.cdc].conc = [mixed_conc[i]/2 for i in range(len(mixed_conc))]
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
            pass
                
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
            D2_conc = self.biochip[mixer.d2r][mixer.d2c].conc[:]
            self.delete_droplet(mixer.d2r, mixer.d2c)
            mixer.d2r = -1
            mixer.d2c = -1
            
            if mixer.change_color == True:  #First mixing - change color
                c = get_random_color(mixed_droplet=True)
                mixer.change_color = False
            else:       #Subsequent mixing - donot change color
                (ID,w,c) = self.__get_id_width_fill_of_droplet(mixer.d1r,mixer.d1c) 
                                               
            D1_conc = self.biochip[mixer.d1r][mixer.d1c].conc[:] 
            self.delete_droplet(mixer.d1r, mixer.d1c)
            self.biochip[mixer.d1r][mixer.d1c].electrode.create_oval(1, 1, cell_size-1, cell_size-1, fill = c, width = 2)
            self.biochip[mixer.d1r][mixer.d1c].electrode.update()
            mixed_conc = [D1_conc[i] + D2_conc[i] for i in range(len(D1_conc))]     #sum of D_1 and D_2 conc
            self.biochip[mixer.d1r][mixer.d1c].conc = mixed_conc[:]
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
            mixed_conc = self.biochip[mixer.cdr][mixer.cdc].conc[:]
            self.delete_droplet(mixer.cdr, mixer.cdc)
                    
            self.biochip[mixer.cdr][mixer.cdc].electrode.create_oval(cell_size/4, cell_size/4, cell_size*3/4, cell_size*3/4, fill = c)
            self.biochip[mixer.cdr][mixer.cdc].electrode.update()
            self.biochip[mixer.cdr][mixer.cdc].conc = [mixed_conc[i]/2 for i in range(len(mixed_conc))]
            mixer.d1r = mixer.cdr
            mixer.d1c = mixer.cdc
                    
            self.biochip[mixer.cdr][mixer.cdc+1].electrode.create_oval(cell_size/4, cell_size/4, cell_size*3/4, cell_size*3/4, fill = c)
            self.biochip[mixer.cdr][mixer.cdc+1].electrode.update()
            self.biochip[mixer.cdr][mixer.cdc+1].conc = [mixed_conc[i]/2 for i in range(len(mixed_conc))]
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
            pass
                
        mixer.state = (mixer.state + 1) % 6    
        
    def run_mixer(self):
        for mixer in self.mixer_table:
            if mixer.mtype == 14:   #1*4 horizontal mixer
                self.__mixer_14(mixer)
            elif mixer.mtype == 41:  #4*1 vertical mixer
                self.__mixer_41(mixer)
            else:
                pass                
        
        # delete expired mixers
        active_mixers = []
        for mixer in self.mixer_table:       
            if self.clock == mixer.e_time:
                self.__delete_mixer(mixer)
            else:
                active_mixers.append(mixer)
        
        self.mixer_table = active_mixers 
    
    

