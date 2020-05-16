# A Floater is Prey; it updates by moving mostly in
#   a straight line, but with random changes to its
#   angle and speed, and displays as ufo.gif (whose
#   dimensions (width and height) are computed by
#   calling .width()/.height() on the PhotoImage


from PIL.ImageTk import PhotoImage
from prey import Prey
import random,math


class Floater(Prey): 
    radius = 5 
    angle = random.random()*2*math.pi
    color = 'red' 
    
    def __init__(self,x,y): 
        Prey.__init__(self,x,y,10,10,Floater.angle,5)
        self._image = PhotoImage(file='ufo.gif')
        
    
    def update(self,model):
        var = random.uniform(1,10) 
        if var > 3: 
            self.move() 
        else: 
            self._angle += random.choice([-1,1])*.5
            self._speed += random.choice([-1,1])*.5
            if self._speed < 3 or self._speed > 7: 
                self._speed = 5 
            self.move() 
            
    def display(self,canvas):
        canvas.create_image(*self.get_location(),image=self._image)
        
        """
        canvas.create_oval(self._x-Floater.radius      , self._y-Floater.radius,
                                self._x+Floater.radius, self._y+Floater.radius,
                                fill=Floater.color)
                                """