from tkinter import *
from tkinter import ttk
import tkinter as tk
import json
import random
import math
import string
 

def createStixObject():  
    
    options = [   
        "attack-pattern",
     #   "threat-actor",
      #  "indicator",
      #  "malware",
      #  "identity",
        
    ]  
    global menu
    def selectMenu(choice):
        global menu
        menu = variable.get()
        choice = variable.get()
    def clicked():
        global menu
        amount = number.get()
        if(amount == ''):
            amount = 1  
        else:
            amount = int( amount) 
            if(amount > 20 ):
                amount = 20
            if(amount < 0 ):
                amount = 1
        nam = name.get()
      #  description = desc.get()
        for i in range(0, amount):     
            rnam = nam
            if(nam == ''):
                rnam = ''.join(random.choices(string.ascii_uppercase 
                        + string.digits + string.ascii_lowercase, k=random.randrange(3, 10)))
            rmenu = menu
            if(menu == ''):
                rmenu = options[random.randrange(0, len(options))]
            objJson = {
                "name": rnam,
                "type": rmenu,
            }            
    #        if(description != ''):
     #           objJson["Description"] = description
            strJson =  json.dumps(objJson)
            print(strJson)
                          
        window.destroy()
      
            
    menu = ""
    window = tk.Toplevel()
    window.title("Create Stix object part one")
    window.geometry('300x300')
    window.configure(background = "white")
    variable = StringVar()
    a = Label(window ,text = "Name").grid(row = 0,column = 0)
    b = Label(window ,text = "Type").grid(row = 1,column = 0)
 #   c = Label(window ,text = "Description").grid(row = 2,column = 0)
    d = Label(window ,text = "Number").grid(row = 2,column = 0)    
    name = Entry(window)
    name.grid(row = 0,column = 1)
    type = OptionMenu( window , variable, *options, command=selectMenu )
    type.grid(row = 1,column = 1)
    #desc = Entry(window)
    #desc.grid(row = 2,column = 1)
    number = Entry(window)
    number.grid(row = 2,column = 1)#restrict to ints later
   
    sub = ttk.Button(window ,text="Submit", command = clicked).grid(row=5,column=0)
    cal = ttk.Button(window ,text="Cancel", command = window.destroy).grid(row=5,column=1)
    window.mainloop()
#createStixObject() 