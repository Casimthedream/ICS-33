# Black_Hole inherits from only Simulton, updating by finding+removing
#   any Prey whose center is contained within its radius
#  (returning a set of all eaten simultons), and
#   displays as a black circle with a radius of 10
#   (width/height 20).
# Calling get_dimension for the width/height (for
#   containment and displaying) will facilitate
#   inheritance in Pulsator and Hunter

from simulton import Simulton
from prey import Prey


class Black_Hole(Simulton):
    color = 'Black' 
    radius = 10 
    def __init__(self,x,y): 
        Simulton.__init__(self,x,y,Black_Hole.radius*2,Black_Hole.radius*2) 
        
    def update(self,model):
        s = set() 
        prey = model.find(lambda x : issubclass(type(x),Prey) )
        for obj in prey: 
            if Black_Hole.contains(self,obj._x,obj._y): 
                s.add(obj)
                model.remove(obj)
        return s 
        
    def display(self,canvas): 
        canvas.create_oval(self._x-self._width/2      , self._y-self._height/2,
                                self._x+self._width/2 , self._y+self._height/2,
                                fill=Black_Hole.color) 
        
    def contains(self,x,y): 
        return self._x - self._width/2  <= x <= self._x + self._width/2 and\
               self._y - self._height/2 <= y <= self._y + self._height/2
        
