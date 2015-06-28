#!/usr/bin/python
#
 
from Tkinter import Frame, Tk, BOTH, Text, Menu, END, Canvas, W, Label, RIDGE, Entry
from ttk import Button, Style
import tkFileDialog
import tkMessageBox as box
import os
import csv

class Example(Frame):     

    def __init__(self, parent):
        Frame.__init__(self, parent)   

        self.parent = parent        
        self.initUI()

    def initUI(self):

        self.parent.title("File dialog")

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)        
        self.style = Style()
        self.style.theme_use("default")        

        global frame1
        frame1 = Frame()
        frame1.grid(row=0, column=0, sticky='w')

        l1 = Label(frame1, text='CSV file name', relief=RIDGE, width=20)
        l1.grid(row=4, column=0)
        
        l2 = Label(frame1, text='SCR file name', relief=RIDGE, width=20)
        l2.grid(row=5, column=0)
        
        inform = Button(frame1, text="Choose CSV file", command=self.onCSVfile)
        inform.grid(row=1, column=0)

        self.file_opt = options = {}
        options['defaultextension'] = '.csv'
        options['filetypes'] = [('CSV files', '.csv'), ('all files', '.*')]

    def nofilename(self, message):
        box.showerror("Error", message)
        
    def onWarn(self):
        box.showwarning("Warning", "Deprecated function call")
        
    def onQuest(self):
        box.askquestion("Question", "Are you sure to quit?")
        
    def onOpen(self):
        box.showinfo("Information", "Download completed")

    def isBlank (self, myString):
        if myString and myString.strip():
            #myString is not None AND myString is not empty or blank
            return False
        #myString is None OR myString is empty or blank
        return True

    def onCSVfile(self):
        global CSVfilename
        CSVfilename = tkFileDialog.askopenfilename(**self.file_opt)
        n1 = Label(frame1, text=CSVfilename, width=70, anchor=W)
        n1.grid(row=4,column=2)

        if self.isBlank(CSVfilename):
            self.nofilename("No file selected")
        else:
            global SCRfilename
            SCRfilename = os.path.splitext(CSVfilename)[0] + '.scr'
            n2 = Label(frame1, text=SCRfilename, width=70, anchor=W)
            n2.grid(row=5,column=2)
        
            self.setup_parms(SCRfilename)

    def myroundup(self, x, base=5):
        return int(base * round((float(x)+(base/2.0))/base))
      
    def setup_parms(self, SCRfilename):
            
        xoffset = 0
        yoffset = 0

        y_mult = 100

        yrounding = 2

        frame2 = Frame()
        frame2.grid(row=1, column=0, sticky='w')

        l1 = Label(frame2, text='Y multiplier', width=20, anchor=W)
        l1.grid(row=0, column=0)
        e1 = Entry(frame2, width=10)
        e1.grid(row=1, column=0)
        e1.insert(0, y_mult)

        l2 = Label(frame2, text='Y axis rounding', width=20, anchor=W)
        l2.grid(row=0, column=1)
        e2 = Entry(frame2, width=10)
        e2.grid(row=1, column=1)
        e2.insert(0, yrounding)
        
        l3 = Label(frame2, text='X Offset', width=20, anchor=W)
        l3.grid(row=0, column=2)
        e3 = Entry(frame2, width=10)
        e3.grid(row=1, column=2)
        e3.insert(0, xoffset)
        
        l4 = Label(frame2, text='Y Offset', width=20, anchor=W)
        l4.grid(row=0, column=3)
        e4 = Entry(frame2, width=10)
        e4.grid(row=1, column=3)
        e4.insert(0, yoffset)
        
        submit = Button(frame2, text="Enter", width=15, command=lambda: self.valueGET(e1.get(), e2.get(), e3.get(), e4.get()))
        submit.grid()
        
        return

    def valueGET(self, Ym, Yr, Xo, Yo):
        y_mult = int(float(Ym))
        yrounding = int(float(Yr))
        xoffset = int(float(Xo))
        yoffset = int(float(Yo))		      
        self.convert_file(y_mult, yrounding, xoffset, yoffset)
        return

    def convert_file(self, y_mult, yrounding, xoffset, yoffset):
 
        min_x = 2000.0
        max_x = -1000.0

        min_y = 2000.0
        max_y = -1000.0
        last_y = -100

#        x = 0

#        v1 = Label(textvariable=x, width=10, anchor=W)
#        v1.grid(row=7,column=1)

        script = open(SCRfilename, 'w')
        script.write('pline\n')

        with open(CSVfilename, 'r') as csvfile:
            profile = csv.reader(csvfile, delimiter='\t', quotechar='|')
            for row in profile:
                print(', '.join(row))
                x = float(row[0])
                y = float(row[1])
# Only create scr line if there has been a significant change in Y
                if abs(last_y - y) > 0.05:
                    last_y = y
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
                    y = y * y_mult
                    outstr = str(x+xoffset) + "," + str(y+yoffset) + "\n"
                    script.write(outstr)

# close the pline command
        script.write('\n')
        
# create the axis        
        xsteps = self.myroundup(max_x, 200) / 200

        yaxis_max = self.myroundup(max_y, yrounding)
        yaxis_min = self.myroundup(min_y, yrounding) - yrounding
       
        for xaxis in xrange(1, xsteps+1):      
             outstr = "line " + str(min_x+(200*(xaxis-1))+xoffset) + "," + str((yaxis_min * y_mult)+yoffset) + " " + str(min_x+(200*(xaxis-1))+xoffset) + "," + str((yaxis_max * y_mult)+yoffset) + "\n\n"
             script.write(outstr)

        for yaxis in xrange(yaxis_min, yaxis_max):
             outstr = "line " + str(min_x+xoffset) + "," + str((yaxis * y_mult)+yoffset) + " " + str(max_x+xoffset) + "," + str((yaxis * y_mult)+yoffset) + "\n\n"
             script.write(outstr)
        
        script.close()
        print("Min is ", min_y, "Max is ", max_y)
        print("yaxis min is ", yaxis_min, "yaxis max is ", yaxis_max)


        frame3 = Frame()
        frame3.grid(row=2, column=0, sticky='w')
# Blank line
        l1 = Label(frame3, text='', width=20, anchor=W)
        l1.grid(row=0, column=0)

        l2 = Label(frame3, text='minimum height', width=20, anchor=W)
        l2.grid(row=1, column=0)

        l3 = Label(frame3, text='maximum height', width=20, anchor=W)
        l3.grid(row=1, column=1)

        l4 = Label(frame3, text='profile length', width=20, anchor=W)
        l4.grid(row=1, column=2)

        l5 = Label(frame3, text='plotted min Y', width=20, anchor=W)
        l5.grid(row=1, column=3)

        l6 = Label(frame3, text=str(min_y), width=20, anchor=W)
        l6.grid(row=2, column=0)

        l7 = Label(frame3, text=str(max_y), width=20, anchor=W)
        l7.grid(row=2, column=1)

        l8 = Label(frame3, text=str(max_x), width=20, anchor=W)
        l8.grid(row=2, column=2)

        l9 = Label(frame3, text=str(yaxis_min * y_mult), width=20, anchor=W)
        l9.grid(row=2, column=3)



        return
        


def main():

    root = Tk()
    ex = Example(root)
    root.geometry("600x450+200+200")
    root.mainloop()  


if __name__ == '__main__':
    main()
    
