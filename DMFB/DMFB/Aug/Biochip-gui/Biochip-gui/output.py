from Tkinter import *
from tkFileDialog import askopenfilename 
from tkMessageBox import showinfo

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

class cell:
    def __init__(self):
        self.electrode = None   # canvas for drawing droplet
        self.ID = None           # denote its position in ratio -- valid for type = reagent only  
        self.toolTip = None

class Biochip(Frame): 
    def __init__(self, parent,r,c):
        Frame.__init__(self, parent)
        self.parent = parent
        self.row = r
        self.col = c
        self.biochip = create_matrix(self.row+2,self.col+2)     # canvas for each electrode        
        self.grid()                                             # set grid layout
        self.__arch_layout()
        self.__ID = -1                                          # indicates the number of reagents
        
        self.parent.resizable(0,0)
        self.parent.title('SimBioSys')
        
# Create biochip layout 
    def __arch_layout(self):
        for i in range(self.row+2):
            self.rowconfigure(i, pad=1)
        for j in range(self.col+2):
            self.columnconfigure(j, pad=1)
            
        
        for i in range(self.row+2):
            for j in range(self.col+2):
                self.biochip[i][j].electrode = Canvas(self, bg="white",height=50, \
                                                      width=50,highlightbackground="red")
                #self.biochip[i][j].toolTip = Message(self.biochip[i][j].electrode,text="",relief=RAISED,bd=1,aspect=1500 )
                #self.biochip[i][j].toolTip.grid()
                self.biochip[i][j].electrode.grid(row=i,column=j)
    
    def show( self,r,c ):
        """ Displays the ToolTip """
        ratio = str(r)+","+str(c)
        #self.biochip[r][c].toolTip = Message(self.biochip[r][c].electrode,text="",relief=RAISED,bd=1,aspect=1500 )
        #self.biochip[r][c].toolTip.grid()
        #self.biochip[r][c].toolTip.config(text=ratio)
        self.biochip[r][c].electrode.create_oval(50/4, 50/4, 50*3/4, 50*3/4, fill = "red", width = 1) 
                
root = Tk()  
root.title('Biochip Simulator')
root.resizable(0,0)  
B = Biochip(root,4,4)
B.show(3,3)
root.mainloop()
