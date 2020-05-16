# Pass a reference to this module when calling each update in update_all

#Use the reference to this module to pass it to update methods
import controller
import model     
import math,random

from ball      import Ball
from floater   import Floater
from blackhole import Black_Hole
from pulsator  import Pulsator
from hunter    import Hunter
from special import Special

# Global variables: declare them global in functions that assign to them: e.g., ... = or +=
objects = set() 
running = False 
cycle_count = 0 


#return a 2-tuple of the width and height of the canvas (defined in the controller)
def world():
    return (controller.the_canvas.winfo_width(),controller.the_canvas.winfo_height())


#reset all module variables to represent an empty/stopped simulation
def reset ():
    global running, cycle_count, objects, last
    objects = set() 
    running = False 
    cycle_count = 0 
    last = None



#start running the simulation
def start ():
    global running 
    running = True 
    


#stop running the simulation (freezing it)
def stop ():
    global running 
    running = False 


#tep just one update in the simulation
def step ():
    global cycle_count, running 
    if running == False: 
        running = True
        cycle_count += 1
        for o in objects: 
            o.update(model)
        running = False   
    else: 
        cycle_count += 1
        for o in objects: 
            o.update(model) 
        running = False


#remember the kind of object to add to the simulation when an (x,y) coordinate in the canvas
#  is clicked next (or remember to remove an object by such a click)   
def select_object(kind):
    global last
    last = kind
    print(last)
    
    
#add the kind of remembered object to the simulation (or remove all objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):
    
    
    global objects, last
    
    if last != 'Remove':
        objects.add(eval(last+'('+str(x)+','+str(y)+')')) 
        print(x,y)
    elif last == 'Remove': 
        copy = objects.copy()
        print(x,y)
        for o in copy: 
            if o._x-o._width/2  <= x <= o._x + o._width/2  and o._y - o._height/2 <= y <= o._y + o._height/2: 
                remove(o)
    elif last in ("Restart", 'Stop', 'Start', 'Step'): pass 

                
         
    
        


#add simulton s to the simulation
def add(s):
    global last 
    pass 
"""
    if s == 'Ball': 
        objects.add(Ball(x,y))
""" 

# remove simulton s from the simulation    
def remove(s):
    global objects 
    objects.remove(s)
    

#find/return a set of simultons that each satisfy predicate p    
def find(p):
    global objects 
    s = set()
    for o in objects: 
        if p(o): 
            s.add(o)
    return s 
     


#call update for every simulton (passing each model) in the simulation
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def update_all():
    global cycle_count, running 
    if running: 
        cycle_count += 1 
        try: 
            for o in objects: 
                o.update(model)
        
        except: 
            stop()
            if len(objects) > 0: 
                start()
        

#To animate: first delete every simulton from the canvas; then call display on
#  each simulton being simulated to add it back to the canvas, possibly in a
#  new location; also, update the progress label defined in the controller
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def display_all():
    for o in controller.the_canvas.find_all(): 
        controller.the_canvas.delete(o)
        
    for b in objects:
        b.display(controller.the_canvas)
    
    controller.the_progress.config(text=str(len(objects))+" Objects/"+str(cycle_count)+" cycles")
        
    
