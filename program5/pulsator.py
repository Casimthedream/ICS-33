# A Pulsator is a Black_Hole; it updates as a Black_Hole
#   does, but also by growing/shrinking depending on
#   whether or not it eats Prey (and removing itself from
#   the simulation if its dimension becomes 0), and displays
#   as a Black_Hole but with varying dimensions


from blackhole import Black_Hole
from prey import Prey

class Pulsator(Black_Hole): 
    counter = 0 
    def __init__(self,x,y): 
        Black_Hole.__init__(self,x,y) 
        
    def update(self,model):
        Pulsator.counter += 1 
        s = set() 
        prey = model.find(lambda x : issubclass(type(x),Prey) )
        for obj in prey: 
            if Black_Hole.contains(self,obj._x,obj._y): 
                s.add(obj)
                model.remove(obj)
                Pulsator.counter = 0 
                self._width += 1 
                self._height += 1
        if Pulsator.counter%30 == 0 and Pulsator.counter != 0: 
            self._width -= 1
            self._height -= 1 
            #print(self._width)
            if self._width <= 0: 
                #print(self._width)
                model.remove(self)
        return s 
         
