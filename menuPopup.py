from Tkinter import *
import re
from os.path import expanduser
import os
import time
import sys

fname = sys.argv[1]
with open(fname) as file:
    pass

class AutocompleteEntry(Entry):
    def __init__(self, fname, *args, **kwargs):
        
        Entry.__init__(self, *args, **kwargs)
        self.fname=fname
        self.lista = self.readInFile(self.fname)
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()
            self.config(width=80)
            self.focus()
            self.pack(side="top")

        self.var.trace('w', self.changed)
#        self.bind("<Right>", self.selection)
        self.bind("<Return>", self.choose)
        self.bind("<Escape>", self.terminate)
        self.bind("<Up>", self.up)
        self.bind("<Tab>", self.down)
        self.bind("<Down>", self.down)
        self.lb = Listbox(root, width=w, height=h)
        self.lb.bind("<Double-Button-1>", self.selection)
        self.lb.bind("<Right>", self.selection)
        #self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
        self.lb.pack(side="left",fill="both", expand=True)
        

    def changed(self, name, index, mode):  

            words = self.comparison()
            if words:            
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                self.lb.delete(0, END)
        
    def selection(self, event):
        self.var.set(self.lb.get(ACTIVE))
        self.finish()
        
    def terminate(self, event):
        self.finish()
        
    def finish(self):
        print self.var.get()
        toAdd= re.sub("[']", '', self.var.get())
        os.system("echo -n '%s;' | xclip -sel clip" % toAdd )
        #os.system("~/.config/qtile/sendKeys.sh '%s'&" % self.var.get()) 
        root.quit()
        

    def readInFile(self, fname):
        content = [line.rstrip('\n') for line in open(fname)]
        return content

    def appendToFile(self, fname, txt):
        with open(fname, "a") as myfile:
            myfile.write(txt)

    def choose(self, event):
        if self.lb.curselection() != ():
            self.var.set(self.lb.get(ACTIVE))
        
        if self.isUnique(self.var.get()):
            self.appendToFile(self.fname, self.var.get() + "\n")
        self.finish()

    def up(self, event):

        if self.lb.curselection() == ():
            index = '0'
        else:
            index = self.lb.curselection()[0]
        if index != '0':                
            self.lb.selection_clear(first=index)
            index = str(int(index)-1)                
            self.lb.selection_set(first=index)
            self.lb.activate(index) 

    def down(self, event):

        if self.lb.curselection() == ():
            index = '-1'
        else:
            index = self.lb.curselection()[0]
        if index != END:                        
            self.lb.selection_clear(first=index)
            index = str(int(index)+1)        
            self.lb.selection_set(first=index)
            self.lb.activate(index) 

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*', re.IGNORECASE)
        return [w for w in self.lista if re.match(pattern, w)]

    def isUnique(self, toCheck):
        return not toCheck in self.lista
#        pattern = re.compile('^' + toCheck + '$')
#        return [w for w in self.lista if re.match(pattern, w)] == []



if __name__ == '__main__':
    root = Tk()
    root.wm_attributes('-topmost', 1)
    w = 600 #The value of the width
    h = 650 #The value of the height of the window
    x = root.winfo_pointerx() 
    y = root.winfo_pointery()
    # get screen width and height
    ws = x
    hs = y

    # calculate position x, y
    x = (ws) - (w/2)
    y = (hs) - (h/2)

    #This is responsible for setting the dimensions of the screen and where it is
    #placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    entry = AutocompleteEntry(fname, root)
    #entry.grid(row=0, column=0)

    root.mainloop()

