from tkinter import *
from tkinter import filedialog
from tkcalendar import DateEntry #pip install tkcalendar
import tkinter as tk
import ctypes 
from stix2validator import validate_file, validate_string, print_results,ValidationOptions,validate_instance #install
from stix2 import Indicator,ThreatActor,AttackPattern,Bundle, Relationship, parse #install
import pyautogui #install
import json
import random
import math
import string
import keyboard#install
import copy
from datetime import datetime
##create program to open file import jsons- turn to stix objects - combine objects
def add_obj_array(array, file):
    inputString = ""
    with open(file) as f:
        inputString = f.read()
        
        #options = ValidationOptions(strict=True, version="2.2")    
        if( inputString[ 0: 1] == '['):
            jsonList = json.loads(inputString)              
            for jo in jsonList :  
                results = validate_instance(jo)
                if results.is_valid :       
                    obj = parse(jo)
                    if(obj['type'] == 'bundle'):
                        objects = obj['objects']    
                        for o in objects :
                            add_stix_button(o)
                            array.append(o)
                    else:
                        array.append(obj)
                        add_stix_button(obj)
                    print_results(results)
                    print("this is a stix valid json" )
                else:
                    print_results(results)
                    print("this is not a stix valid json")        
        else:
            results = validate_string(inputString)
            if results.is_valid :
                obj = parse(inputString)
                if(obj['type'] == 'bundle'):
                    objects = obj['objects']    
                    for o in objects :
                        array.append(o)
                        add_stix_button(o)
                else:
                    array.append(obj)
                    add_stix_button(obj)
                print_results(results)
                print("this is a stix valid json" )
            else:
                print_results(results)
                print("this is not a stix valid json")

# Function to open a file in the system
def open_file():
   global curInd
   global obj_array
   filepath = filedialog.askopenfilename(title="Open a Text File", filetypes=(("text    files","*.json"), ("all files","*.*")))
   files.append(open(filepath,'r'))
   print(curInd)
   print(files[curInd].name)
   files[curInd].close()   
   nams = "" 
   add_obj_array(obj_array, files[curInd].name)    
   for ele in files:
      nams += ele.name + "\n"
   fileLab.config(text="Files: "+nams)
     
   curInd+=1
   lineUpdate()

def reset(): 
    global files, curInd,obj_array,obj_buttons, sourceObj, targetObj
    files = []
    obj_array = []
    for o in obj_buttons:
        o.destroy()
    obj_buttons = []
    curInd = 0
    fileLab.config(text="Files:")  
    sourceObj = []
    targetObj = []
def createBundle():           
    bundle = Bundle(obj_array)
    ctypes.windll.user32.MessageBoxW(0, "bundle successfully created", "success", 1)
    
    stix_json_string = bundle.serialize(pretty=True)
    print(stix_json_string)
    with open("combine.json", "w") as write_file:
        write_file.write(stix_json_string)

def add_stix_button(stixObj):
    global obj_buttons
    if stixObj.type != 'relationship' :
        stixLab = Label(win, text=stixObj.name +" \n" +stixObj.type,  height= 2, background="lightgray")
        xloc =  0 + random.randrange(1, 30)*26
        yloc = 150 + random.randrange(1, 30)*26
        stixObj =  StixObject(stixLab, id=stixObj.id, x=xloc, y=yloc, dragable = True)
    else:
        stixLab = Label(win, text=stixObj.relationship_type, height= 2, background="lightgray")
        xloc =  20 + random.randrange(1, 20)*20
        yloc = 150 + random.randrange(1, 20)*20
        stixObj =  StixObject(stixLab, id=stixObj.id, x=xloc, y=yloc, dragable = False, source = stixObj.source_ref, target = stixObj.target_ref)
    obj_buttons.append(stixObj)

def lineUpdate():
    
    for o in obj_buttons:
        if(o.source != None and o.target != None) :            
            if( o.line == None):
                o.makeLine()
            else:
                o.updateLine()
       
#stix obj stuff
def makeReference(sourceId, targetId):
    global obj_array
    print(sourceId, targetId)

    type = pyautogui.prompt("Relationship type")
    if(type != None):
        if(type == ''):
            type = ''.join(random.choices( string.ascii_lowercase, k=random.randrange(3, 10)))
        relationship = Relationship(relationship_type=type,                            
            source_ref = sourceId,
            target_ref = targetId,)
        obj_array.append(relationship)
        add_stix_button(relationship)
        lineUpdate()
def find_bottonID( id):
    result = None
    for o in obj_buttons:
        if(o.id == id):
            result = o
    return result
def reference_exists(sourceID, targetId):
    global obj_array
    for o in obj_array:
        if(o.type == 'relationship' and ((o.source_ref == sourceID and o.target_ref == targetId ) 
                                         or (o.source_ref == targetId and o.target_ref == sourceID ) ) ):
            print( "relationship already exist")
            return True
    return False
def pointDirection(point1x, point1y, point2x, point2y):	
    top = point2y - point1y
    bottem = point2x - point1x		
    return( math.atan2(top,bottem) )
def pointDistance(point1x, point1y, point2x, point2y):	
	
	fir = point2y - point1y
	sec = point2x - point1x
		
	return( math.sqrt( math.pow(fir, 2) + math.pow(sec, 2) ) )
	
def lengthDirX( width,  angle ):		
	
	return( ( width * math.cos(angle)) )

def lengthDirY( width,  angle ):		

	return( ( width * math.sin(angle)) )    
def deleteObjects():
    global obj_array, obj_buttons, sourceObj, targetObj
    for ob in sourceObj :          
        ind = obj_buttons.index(ob)
        b = obj_buttons.pop(ind)
        b.destroy()
      
    lineUpdate()
    
    sourceObj = []
    targetObj = []
   
def createStixObject():      
    options = [   
        "attack-pattern",
        "threat-actor",
        "indicator",
        "malware",
        "identity",
        "location"        
    ]  

    global menu, windowButtons, objJson,amount
    def selectMenu(choice):
        global menu
        menu = variable.get()
        choice = variable.get()
    def clicked():
        global menu, windowButtons, objJson,amount
        amount = number.get()
        if(amount == ''):
            amount = 1  
        else:
            amount = int( amount) 
            if(amount > 40 ):
                amount = 40
            if(amount < 0 ):
                amount = 1
        nam = name.get()
        description = desc.get()          
        rnam = nam
        if(nam == ''):
            rnam = "@random"
   
        rmenu = menu
        if(menu == ''):
            rmenu = options[random.randrange(0, len(options))]
        objJson = {
            "name": rnam,
            "type": rmenu,
            "spec_version": "2.1"
        }   
        if(description != ''):
            objJson["description"] = description
        for b in windowButtons:         
            b.destroy()
        windowButtons = []
        r = 0
        t = Label(window ,text = rmenu+":")
        t.grid(row = 0,column = 0)
        n = Label(window ,text = rnam)
        n.grid(row = 0,column = 1)
        if(rmenu ==  "attack-pattern"):

            
            b = Label(window ,text = "aliases")
            b.grid(row = 1,column = 0)
                        
            alias = Entry(window)            
            alias.grid(row = 1,column = 1)
            windowButtons.append(alias)
   
    #        c = Label(window ,text = "kill chain phases ")
     #       c.grid(row = 2,column = 0)    
            
  #          kc = Entry(window)
   #         kc.grid(row = 2,column = 1)
    #        windowButtons.append(kc)
            r = 4
        elif (rmenu ==  "threat-actor"):
            Label(window ,text = "threat actor types ").grid(row = 1,column = 0)
            thact = Entry(window)
            thact.grid(row = 1,column = 1)
            windowButtons.append(thact)
            
            Label(window ,text = "aliases").grid(row = 2,column = 0)
            alias = Entry(window)
            alias.grid(row = 2,column = 1)
            windowButtons.append(alias)
            
            Label(window ,text = "first_seen").grid(row = 3,column = 0)
            first = DateEntry(window, date_pattern='yyyy/MM/dd')
            first.delete(0, "end")
            ##first
            first.grid(row = 3,column = 1)
            windowButtons.append(first)
            
            Label(window ,text = "last_seen").grid(row = 4,column = 0)
            last = DateEntry(window, date_pattern='yyyy/MM/dd')
            last.delete(0, "end")
            last.grid(row = 4,column = 1)
            windowButtons.append(last)
            
            Label(window ,text = "roles").grid(row = 5,column = 0)
            roles = Entry(window)
            roles.grid(row = 5,column = 1)
            windowButtons.append(roles)
            
            Label(window ,text = "goals").grid(row = 6,column = 0)
            goals = Entry(window)
            goals.grid(row = 6,column = 1)
            windowButtons.append(goals)
            
            Label(window ,text = "sophistication").grid(row = 7,column = 0)
            sophist = Entry(window)
            sophist.grid(row = 7,column = 1)
            windowButtons.append(sophist)
            
            Label(window ,text = "resource level").grid(row = 8,column = 0)
            resource = Entry(window)
            resource.grid(row = 8,column = 1)
            windowButtons.append(resource)
            
            Label(window ,text = "primary motivation").grid(row = 9,column = 0)
            motive = Entry(window)
            motive.grid(row = 9,column = 1)
            windowButtons.append(motive)
            
            r =10
        elif (rmenu ==  "indicator"):
            Label(window ,text = "indicator types").grid(row = 1,column = 0)
            indTypes = Entry(window)
            indTypes.grid(row = 1,column = 1)
            windowButtons.append(indTypes)
            
            Label(window ,text = "pattern ").grid(row = 2,column = 0)
            pattern = Entry(window)
            pattern.grid(row = 2,column = 1)
            windowButtons.append(pattern)
            
            Label(window ,text = "pattern type ").grid(row = 3,column = 0)
            pattType = Entry(window)
            pattType.grid(row = 3,column = 1)          
            windowButtons.append(pattType)
            
            Label(window ,text = "valid from ").grid(row = 4,column = 0)
            valfro = DateEntry(window, date_pattern='yyyy/MM/dd')
            valfro.delete(0, "end")
            valfro.grid(row = 4,column = 1)
            windowButtons.append(valfro)
            
            Label(window ,text = "valid until").grid(row = 5,column = 0)
            valunt = DateEntry(window, date_pattern='yyyy/MM/dd')
            valunt.delete(0, "end")
            valunt.grid(row = 5,column = 1)
            windowButtons.append(valunt)
            
            Label(window ,text = "kill chain phases ").grid(row = 6,column = 0)
            kcp = Entry(window)
            kcp.grid(row = 6,column = 1)
            windowButtons.append(kcp)
            
            r = 8
        elif (rmenu ==  "malware"):
            Label(window ,text = "malware types ").grid(row = 1,column = 0)
            malTypes = Entry(window)
            malTypes.grid(row = 1,column = 1)
            windowButtons.append(malTypes)
            check = IntVar()
            Label(window ,text = "is family ").grid(row = 2,column = 0)
            isfam = Checkbutton(window, variable=check)
            isfam.grid(row = 2,column = 1)
            windowButtons.append(check)
            
            Label(window ,text = "aliases ").grid(row = 3,column = 0)
            pattType = Entry(window)
            pattType.grid(row = 3,column = 1)    
            windowButtons.append(pattType)
            
       #     Label(window ,text = "kill chain phases ").grid(row = 4,column = 0)
        #    kcp = Entry(window)
         #   kcp.grid(row = 4,column = 1)
          #  windowButtons.append(kcp)
            
            Label(window ,text = "first seen ").grid(row = 4,column = 0)
            valfro = DateEntry(window, date_pattern='yyyy/MM/dd')
            valfro.delete(0, "end")  
            valfro.grid(row = 4,column = 1)
            windowButtons.append(valfro)
            
            Label(window ,text = "last seen ").grid(row =5,column = 0)
            valunt = DateEntry(window, date_pattern='yyyy/MM/dd')
            valunt.delete(0, "end")
            valunt.grid(row = 5,column = 1)
            windowButtons.append(valunt)
            
            Label(window ,text = "capabilities ").grid(row =6 ,column = 0)
            kcp = Entry(window)
            kcp.grid(row = 6,column = 1)
            windowButtons.append(kcp)
            
            r = 8
        elif (rmenu ==  "identity"):
            Label(window ,text = "roles ").grid(row = 1,column = 0)
            malTypes = Entry(window)
            malTypes.grid(row = 1,column = 1)
            windowButtons.append(malTypes)
            
            Label(window ,text = "sectors").grid(row = 2,column = 0)
            isfam = Entry(window)
            isfam.grid(row = 2,column = 1)
            windowButtons.append(isfam)
            
            Label(window ,text = "contact_information").grid(row = 3,column = 0)
            pattType = Entry(window)
            pattType.grid(row = 3,column = 1)    
            windowButtons.append(pattType)
            
            r = 5
        elif (rmenu ==  "location"):
            
            Label(window ,text = "region ").grid(row = 1,column = 0)
            reg = Entry(window)
            reg.grid(row = 1,column = 1)    
            windowButtons.append(reg)
            
            Label(window ,text = "country ").grid(row = 2,column = 0)
            kcp = Entry(window)
            kcp.grid(row = 2,column = 1)
            windowButtons.append(kcp)
            
            Label(window ,text = "city ").grid(row = 3,column = 0)
            valfro = Entry(window)
            valfro.grid(row = 3,column = 1)
            windowButtons.append(valfro)
            
            Label(window ,text = "street address  ").grid(row =4,column = 0)
            valunt = Entry(window)
            valunt.grid(row = 4,column = 1)
            windowButtons.append(valunt)

            Label(window ,text = "latitude ").grid(row = 5,column = 0)
            lati = Entry(window)
            lati.grid(row = 5,column = 1)
            windowButtons.append(lati)
            
            Label(window ,text = "longitude ").grid(row = 6,column = 0)
            long = Entry(window)
            long.grid(row = 6,column = 1)
            windowButtons.append(long)
            
            r = 8
        sub = filedialog.Button(window ,text="Submit", command = clicked2)
        sub.grid(row=r,column=0)
        windowButtons.append(sub)
        cal = filedialog.Button(window ,text="Cancel", command = window.destroy)
        cal.grid(row=r,column=1)
    def clicked2():
        global menu, windowButtons,objJson,amount
      
        if(objJson["type"] == "attack-pattern"):            
            #,text = "external references")
            
            aliases = windowButtons[0].get()
            if(aliases != ''):
                objJson["aliases"] = aliases.split(',')
            
        #    phases = windowButtons[1].get()
         #   if(phases != ''):
          #      objJson["kill_chain_phases"] = phases.split(',')
            # Label(window ,text = "aliases")
            
            #c = Label(window ,text = "kill chain phases ")
        elif(objJson["type"] == "threat-actor"):
            atype = windowButtons[0].get()
            if(atype != ''):
                objJson["threat_actor_types"] = atype.split(',')
        
            ali = windowButtons[1].get()
            if(ali != ''):
                objJson["aliases"] = ali.split(',')
    
            firs = windowButtons[2].get()
            if(firs != ''):
                objJson["first_seen"] = datetime.strptime(firs+"T00:00:0.000Z", "%Y/%m/%dT%H:%M:%S.%fZ")     
      
            lasts = windowButtons[3].get()
            if(lasts != ''):
                objJson["last_seen"] = datetime.strptime(lasts+"T00:00:0.000Z", "%Y/%m/%dT%H:%M:%S.%fZ")          
 
            role = windowButtons[4].get()
            if(role != ''):
                objJson["roles"] = role.split(',')

            goals = windowButtons[5].get()
            if(goals != ''):
                objJson["goals"] = goals.split(',')          
  
            soph = windowButtons[6].get()
            if(soph != ''):
                objJson["sophistication"] = soph         
 
            res = windowButtons[6].get()
            if(res != ''):
                objJson["resource_level"] = res       

            mot = windowButtons[6].get()
            if(mot != ''):
                objJson["primary_motivation"] = mot   

        elif(objJson["type"] == "indicator"):
            indt = windowButtons[0].get()
            if(indt != ''):
                objJson["indicator_types"] = indt.split(',')    
            
            patt = windowButtons[1].get()
            if(patt != ''):
                objJson["pattern"] = patt    
            else:
                objJson["pattern"] = "pattern"
            pattype = windowButtons[2].get()
            if(pattype != ''):
                objJson["pattern_type"] = pattype    
            else:
                objJson["pattern_type"] = "pattern_Type"
            valfro = windowButtons[3].get()
            if(valfro != ''):
                objJson["valid_from"] = datetime.strptime(valfro+"T00:00:0.000Z", "%Y/%m/%dT%H:%M:%S.%fZ")     
    
            valtil = windowButtons[4].get()
            if(valtil != ''):
                objJson["valid_until"] = datetime.strptime(valtil+"T00:00:0.000Z", "%Y/%m/%dT%H:%M:%S.%fZ") 

            kchp = windowButtons[5].get()
            if(kchp != ''):
                objJson["kill_chain_phases"] = kchp.split(',')          
        elif(objJson["type"] == "malware"):

            malt = windowButtons[0].get()
            if(malt != ''):
                objJson["malware_types"] = malt.split(',')   
            
            objJson["is_family"] = windowButtons[1].get() == 1         
         
            ali = windowButtons[2].get()
            if(ali != ''):
                objJson["aliases"] = ali.split(',') 
           
       #     kchp = windowButtons[3].get()
        #    if(kchp != ''):
         #       objJson["kill_chain_phases"] = kchp.split(',')      
                       
            first = windowButtons[3].get()
            if(first != ""):
                objJson["first_seen"] = datetime.strptime(first+"T00:00:0.000Z", "%Y/%m/%dT%H:%M:%S.%fZ")
            
            last = windowButtons[4].get()
            if(last != ""):
                objJson["last_seen"] = datetime.strptime(last+"T00:00:0.000Z", "%Y/%m/%dT%H:%M:%S.%fZ")
     
            capa = windowButtons[5].get()
            if(capa != ''):
                objJson["capabilities"] = capa.split(',')  

        elif(objJson["type"] == "identity"):
            rol = windowButtons[0].get()
            if(rol != ''):
                objJson["roles"] = rol.split(',')   

            sec = windowButtons[1].get()
            if(sec != ''):
                objJson["sectors"] = sec.split(',')  
           
            cont = windowButtons[2].get()
            if(cont != ''):
                objJson["contact_information"] = cont
                
        elif(objJson["type"] == "location"):            
           
            reg = windowButtons[0].get()
            if(reg != ''):
                objJson["region"] = reg  
            else:
                objJson["region"] = ''.join(random.choices( string.ascii_lowercase, k=random.randrange(3, 10)))  
            coun = windowButtons[1].get()
            if(coun != ''):
                objJson["country"] = coun  
                
            cit = windowButtons[2].get()
            if(cit != ''):
                objJson["city"] = cit 

            street = windowButtons[3].get()
            if(street != ''):
                objJson["street_address"] = street   

            lat = windowButtons[4].get()
            if(lat != ''):
                objJson["latitude"] = float(lat)       

            long = windowButtons[5].get()
            if(long != ''):
                objJson["longitude"] = float(long)              
        for i in range(0, amount):                 
          #  strJson =  json.dumps(objJson)
            tmp_json = copy.deepcopy(objJson)
            if(tmp_json["name"] == "@random"):
                tmp_json["name"] = ''.join(random.choices(string.ascii_uppercase 
                    + string.digits + string.ascii_lowercase, k=random.randrange(3, 10)))
            obj = parse(tmp_json)      
            print(tmp_json)          
            add_stix_button(obj)
            obj_array.append(obj)     
        window.destroy()     
            
    menu = ""
    window = tk.Toplevel()
    window.title("Create Stix object")
    window.geometry('300x300')
    window.configure(background = "white")
    variable = StringVar()
    windowButtons = []
    nam = Label(window ,text = "Name")
    nam.grid(row = 0,column = 0)
    windowButtons.append(nam)
    
    typ = Label(window ,text = "Type")
    typ.grid(row = 1,column = 0)
    windowButtons.append(typ)
    d = Label(window ,text = "Description")
    d.grid(row = 2,column = 0)
    windowButtons.append(d)
    num = Label(window ,text = "Number")
    num.grid(row = 3,column = 0)    
    windowButtons.append(num)
    name = Entry(window)
    name.grid(row = 0,column = 1)
    windowButtons.append(name)
    type = OptionMenu( window , variable, *options, command=selectMenu )
    type.grid(row = 1,column = 1)
    windowButtons.append(type)
    desc = Entry(window)
    desc.grid(row = 2,column = 1)
    windowButtons.append(desc)
    number = Entry(window)
    number.grid(row = 3,column = 1)#restrict to ints later
    windowButtons.append(number)
    sub = filedialog.Button(window ,text="Submit", command = clicked)
    sub.grid(row=5,column=0)
    windowButtons.append(sub)
    cal = filedialog.Button(window ,text="Cancel", command = window.destroy)
    cal.grid(row=5,column=1)
    windowButtons.append(cal)
    window.mainloop()

class StixObject():
    widget = None
    target = None
    source = None
    line = None
    id = ""
    def __init__(self, widget, id, x=0, y=0, dragable = True,source = None, target = None):
        self.start_x = 0
        self.start_y = 0
        self.x = x + widget.winfo_reqwidth()/2       
        self.y = y + widget.winfo_reqheight()/2
        self.widget = widget
        self.id = id
        widget.place(x=x, y=y)
        
        if( source != None): 
            self.source = source
        if( target != None):
            self.target = target                

        widget.bind("<ButtonRelease-1>", self.no_click)
        if(dragable):
            widget.bind("<ButtonPress-1>"  , self.drag_Start)
            widget.bind("<B1-Motion>"      , self.drag)
        widget.bind("<Button-1>"       , self.left_click)
        widget.bind("<Button-2>"       , self.right_click)
        widget.bind("<Button-3>"       , self.right_click)
        
    def drag_Start(self, event):
        self.start_x = event.x
        self.start_y = event.y   

    def drag(self, event):       
        delta_x = event.x - self.start_x
        delta_y = event.y - self.start_y
        x = event.widget.winfo_x() - event.widget.winfo_reqwidth()/2  + delta_x
        y = event.widget.winfo_y() - event.widget.winfo_reqheight()/2 + delta_y
        self.x = x + event.widget.winfo_reqwidth()/2     
        self.y = y + event.widget.winfo_reqheight()/2
        event.widget.place(x = x, y = y)
        lineUpdate()
        
    def left_click(self,event):       
        global sourceObj, targetObj       
        event.widget.configure(bg="green")  
        sourceObj = []
        targetObj = []
    def right_click(self, event):
        global sourceObj, targetObj  
        if(self.source == None):      
            if sourceObj == [] or keyboard.is_pressed("Shift"):
                sourceObj.append( self)
                event.widget.configure(bg="red")
            else :
                if(sourceObj.count( self.id) == 0):
                    for ob in sourceObj:
                        if(not reference_exists(ob, self.id) ):
                            targetObj =  self.id
                            makeReference(ob.id, targetObj) 
                            but = find_bottonID(ob.id)
                            but.widget.configure(bg="lightgray")  
                        else:
                            but = find_bottonID(ob.id)
                            but.widget.configure(bg="lightgray")  
                    sourceObj = []
                    targetObj = []
                else:
                    for ob in sourceObj:
                        find_bottonID(ob.id).widget.configure(bg="lightgray") 
                    event.widget.configure(bg="lightgray")  
                    sourceObj = []
                    targetObj = []
            
            
    def no_click(self, event):
        event.widget.configure(bg="lightgray")  
    def destroy(self):
        
        if( self.line != None):
            canvas.delete(self.line)
        self.widget.destroy()    
        for o in obj_array:
            if(o.id == self.id):
                obj_array.remove(o)
                print(o.id)
    def makeLine(self):       
        sbot = find_bottonID(self.source)
        tbot = find_bottonID(self.target)        
        if( sbot != None and tbot != None): 
            dir = pointDirection(sbot.x, sbot.y, tbot.x, tbot.y)
            dis = pointDistance(sbot.x, sbot.y, tbot.x, tbot.y) 
            xto = sbot.x + lengthDirX(dis*.92, dir)
            yto = sbot.y + lengthDirY(dis*.92, dir) 
            arrowX1 = xto + lengthDirX(-45, dir-.52)
            arrowY1 = yto + lengthDirY(-45, dir-.52)
            arrowX2 = xto + lengthDirX(-45, dir+.52)
            arrowY2 = yto + lengthDirY(-45, dir+.52)    
            self.line = canvas.create_line( sbot.x, sbot.y, xto, yto, xto, yto, arrowX1, arrowY1, xto, yto, arrowX2, arrowY2)  
                      
            xx = sbot.x + (xto -sbot.x)/2 - self.widget.winfo_reqwidth()/2  
            yy = sbot.y + (yto -sbot.y)/2 - self.widget.winfo_reqheight()/2
            self.widget.place(x=xx, y=yy)
    def updateLine(self):       
        sbot = find_bottonID(self.source)
        tbot = find_bottonID(self.target)        
        if( sbot != None and tbot != None): 
            dir = pointDirection(sbot.x, sbot.y, tbot.x, tbot.y)
            dis = pointDistance(sbot.x, sbot.y, tbot.x, tbot.y) 
            xto = sbot.x + lengthDirX(dis*.92, dir)
            yto = sbot.y + lengthDirY(dis*.92, dir) 
            arrowX1 = xto + lengthDirX(-45, dir-.52)
            arrowY1 = yto + lengthDirY(-45, dir-.52)
            arrowX2 = xto + lengthDirX(-45, dir+.52)
            arrowY2 = yto + lengthDirY(-45, dir+.52)         
            canvas.coords( self.line, sbot.x, sbot.y, xto, yto, xto, yto, arrowX1, arrowY1, xto, yto, arrowX2, arrowY2)    
            xx = sbot.x + (xto -sbot.x)/2 - self.widget.winfo_reqwidth()/2  
            yy = sbot.y + (yto -sbot.y)/2 - self.widget.winfo_reqheight()/2
            self.widget.place(x=xx, y=yy)    
        else:
            self.destroy()     
      
            

# Create an instance of window
win=Tk()
canvas = Canvas(width=2000, height=1600)
sourceObj = []
targetObj = []
# Set the geometry of the window
win.geometry("900x700")

Label(win, text="Stix bundle maker", font='Arial 16 bold').pack(pady=3)

files = []
obj_array   = []
obj_buttons = []

curInd = 0
   
# Create a button to trigger the dialog
button = Button(win, text="Open", command=open_file)
button.pack(pady=5)
fileLab = Label(win, text="Files:", font='Arial 8 bold')
fileLab.place(relx = 0.0, rely = 1.0, anchor ='sw')

resetBut = Button(win, text="Reset", command=reset)
resetBut.pack(pady=5)
makeBut = Button(win, text="MakeObj", command=createStixObject)
makeBut.pack()
makeBut = Button(win, text="MakeBuddle", command=createBundle)
makeBut.pack()

delBut = Button(win, text="DeleteObjects", command=deleteObjects)
delBut.place(relx = 0.85, rely = 0.05, anchor ='nw')

canvas.place(x = 0, y =0)


win.mainloop()
