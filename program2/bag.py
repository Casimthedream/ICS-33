from collections import defaultdict
from goody import type_as_str

class Bag:
    def __init__(self, item = 0): 
        if item != 0:
            self.item = ['d','a','b','d','c','b','d']
            if type(item) == list: 
                self.item = item 
        else: 
            self.item = "Empty"
        
    
    def __repr__(self): 
        if self.item != "Empty":
            return "Bag(" + str(self.item) + ")"
        else: return "Bag()"
        
    def __str__(self): 
        if self.item == "Empty": 
            return "Bag()" 
        else:
            chars_count = {}  
            chars = set()
            for obj in self.item: 
                chars.add(obj) 
            for char in chars:
                count = 0 
                for obj in self.item: 
                    if char == obj:
                        count += 1 
                chars_count[char] = count 
            return "Bag(" + str([str(k)+'['+str(v)+']' for k,v in chars_count.items()])+")" 

    def __len__(self): 
        if self.item == "Empty":
            return 0 
        else: 
            return len(self.item) 

    def unique(self):
        if self.item == "Empty":
            return 0 
        else: 
            chars = set()
            for obj in self.item: 
                chars.add(obj) 
            return len(chars)
        
    def add(self, var): 
        if self.item == "Empty":
            self.item = [var]
        else: 
            self.item.append(var)

    def __contains__(self, substr):
        if self.item == "Empty": 
            return False 
        if substr in self.item: 
            return True 
        
    def count(self, var):
        count = 0 
        if self.item == "Empty": 
            return 0
        for obj in self.item: 
            if var == obj:
                count += 1 
        return count 
    
    def __add__(self, other):
        if type(other) != Bag: 
            return NotImplemented 
        newBag = Bag() 
        for obj in self.item: 
            newBag.add(obj) 
        for obj in other.item: 
            newBag.add(obj) 
        return newBag 
    
    def remove(self, var): 
        if var not in self.item: 
            raise ValueError("Value not found")
        else: 
            self.item.remove(var) 
            
    def __eq__(self, other): 
        if type(other) != (Bag): 
            return False
        
        chars_count = {}  
        chars = set()
        for obj in self.item: 
            chars.add(obj) 
        for char in chars:
            count = 0 
            for obj in self.item: 
               if char == obj:
                    count += 1 
            chars_count[char] = count 
                
        hars_count = {}  
        hars = set()
        for obj in other.item: 
            hars.add(obj) 
        for char in hars:
            count = 0 
            for obj in other.item: 
               if char == obj:
                    count += 1 
            hars_count[char] = count 
            
        if chars_count == hars_count: 
            return True 
        else: 
            return False 
     
    def __iter__(self): 
        def gen(bins):
            for i in range(len(self.item)): 
                yield bins[i]
        return gen(list(self.item))
    
    def __next__(self):
        if self.n < self.__len__(): 
            result = self.n
            self.n += 1 
            return self.item[result]  
        else: 
            raise StopIteration 
    
            
if __name__ == '__main__':
    
    #driver tests
    import driver
    driver.default_file_name = 'bscp21W20.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
