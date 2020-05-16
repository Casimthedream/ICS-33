# Hunter inherits from the Pulsator (1st) and Mobile_Simulton (2nd) classes:
#   updating/displaying like its Pulsator base, but also moving (either in
#   a straight line or in pursuit of Prey), like its Mobile_Simultion base.


from prey import Prey
from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
import math 


class Hunter(Pulsator, Mobile_Simulton):
    dist = 200 
    count = 0 
    def __init__(self,x,y): 
        
        Mobile_Simulton.__init__(self,x,y,20,20,0,5) 
        
    def update(self,model): 
        self.move()
        s = set()
        Hunter.count += 1 
        prey = model.find(lambda x : issubclass(type(x),Prey)) 
        for o in prey: 
            if o.distance((self._x,self._y)) < 200:
                self._angle =  math.atan2(o._y-self._y,o._x-self._x)
                if Pulsator.contains(self,o._x,o._y): 
                    s.add(o) 
                    model.remove(o) 
                    Hunter.count = 0
                    self._width += 1 
                    self._height += 1
        if Hunter.count%30 == 0 and Hunter.count != 0: 
            self._width -= 1
            self._height -= 1 
            #print(self._width)
            if self._width <= 0: 
                #print(self._width)
                model.remove(self)
        return s 
                
                 
                
                
