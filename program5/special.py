#This class makes a prey object that disappears and reappears every 30 counts 



from prey import Prey
import random

class Special(Prey): 
    radius = 8
    color = 'yellow'
    angle = 90 
    speed = 14
    count = 0 
    def __init__(self,x,y): 
        Prey.__init__(self,x,y,Special.radius*2,Special.radius*2,Special.angle,Special.speed) 
    
    def update(self,model): 
        self.move() 
        Special.count += 1 
        if Special.count % 30 == 0 and Special.count != 0:
            model.objects.add(Special(random.randint(1,499),random.randint(1,499))) 
            model.remove(self) 
            Special.count = 0   
        
        
    
    def display(self,canvas):
       canvas.create_oval(self._x-Special.radius      , self._y-Special.radius,
                                self._x+Special.radius, self._y+Special.radius,
                                fill=Special.color)