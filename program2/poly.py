class Poly:
    
    def __init__(self, *args):
        self.terms = {}
        self.list_powers = [] 
        for tup in args: 
            if (type(tup[0]) == int or type(tup[0]) == float) and type(tup[1]) == int and tup[1] >= 0:
                pass
            else:
                raise AssertionError("Invalid Terms")
            if tup[0] == 0: 
                continue 
            self.list_powers.append(tup[1]) 
            if len(self.list_powers) == 1: 
                pass 
            else: 
                last = self.list_powers[-1] 
                for obj in self.list_powers[0:len(self.list_powers)-1]: 
                    if last < obj: 
                        pass 
                    else: 
                        raise AssertionError("Must Enter Powers in decreasing order")
                    
            self.terms[tup[1]] = tup[0]  
            
    def __repr__(self): 
        repr_list = []
        for obj in self.list_powers: 
            repr_list.append((self.terms[obj], obj)) 
        return "Poly" + str(tuple(repr_list))  
    
    def __str__(self): 
        poly_str = ""
        if self.terms == {}: 
            return "0" 
        for obj in self.list_powers:
            
            if obj == self.list_powers[0]: 
                 
                if obj > 1 and self.terms[obj] != 0: 
                    
                    if self.terms[obj] == 1: 
                        poly_str += "x^"+str(obj) 
                    elif self.terms[obj] == -1: 
                        poly_str += "-x^"+str(obj)
                    else: 
                        poly_str += str(self.terms[obj])+"x^"+str(obj)
                     
                elif obj == 0: 
                    poly_str +=  str(self.terms[obj])
                    
                elif obj == 1: 
                    poly_str += str(self.terms[obj]) + "x"
            else: 
                
                if self.terms[obj] < 0: 
                    
                    #poly_str += " - "
             
                    if obj > 1:
                        if self.terms[obj] == -1 or self.terms[obj] == -1.0: 
                            poly_str += " - " + "x^" + str(obj)

                        else:  
                            poly_str += " - " + str(self.terms[obj]).lstrip('-') + "x^" + str(obj)
                            
                    elif obj == 0: 
                        poly_str += " - " + str(self.terms[obj]).lstrip('-')
                         
                    elif obj == 1:
                        if self.terms[obj] == -1 or self.terms[obj] == -1.0: 
                            poly_str += " - " + "x" 
   
                        else:  
                            poly_str += " - " + str(self.terms[obj]).lstrip('-') + "x" 
                        
                if self.terms[obj] > 0: 
                   # poly_str += " + "
                    if obj > 1:
                        if self.terms[obj] == -1 or self.terms[obj] == -1.0: 
                            poly_str += " - " + "x^" + str(obj)
                        elif self.terms[obj] == 1 or self.terms[obj] == 1.0: 
                            poly_str += " + " + "x^" + str(obj)
                        else: 
                            poly_str += " + " + str(self.terms[obj]) + "x^" + str(obj)
                            
                    elif obj == 0: 
                        poly_str += " + " + str(self.terms[obj])
                        
                    elif obj == 1:
                        if self.terms[obj] == 1 or self.terms[obj] == 1.0: 
                            poly_str += " + " + "x"
                        else:  
                            poly_str += " + " + str(self.terms[obj]) + "x"
                        
                if self.terms[obj] == 0: 
                    pass 
                
        return poly_str

    def __bool__(self):
        if self.__str__() == "0": 
            return False 
        else: 
            return True
        
    def __len__(self): 
        if self.__str__() == "0": 
            return 0
        return self.list_powers[0] 
    
    def __call__(self, num):
        sum = 0 
        for pwr in self.list_powers: 
            sum += (num**pwr)*self.terms[pwr]  
        return sum 
    
    def __iter__(self): 
        def gen(bins): 
            for pwr in self.list_powers: 
                yield (bins[pwr], pwr)
        return gen(self.terms)
    
    def __next__(self): 
        if self.n < len(self.list_powers): 
            result = self.list_powers[self.n] 
            self.n += 1
            return (self.terms[result], result)
        else: 
            raise StopIteration 
        
    def __getitem__(self, pwr):
        if pwr < 0 or type(pwr) != int: 
            raise TypeError("Not a Good power") 
        if pwr not in self.terms: 
            return 0 
        return self.terms[pwr] 
    
    def __setitem__(self, pwr, coef):
        if pwr < 0 or type(pwr) != int: 
            raise TypeError("Not a Good power")
        if type(coef) != int: 
            raise TypeError("Cannot be a coefficient") 
        if pwr not in self.terms:
            if coef == 0: 
                pass
            else: 
                self.list_powers.insert(0, pwr) 
                self.terms[pwr] = coef
             
        elif pwr in self.terms: 
            self.terms[pwr] = coef 
            if coef == 0: 
                self.terms.pop(pwr)
                self.list_powers.remove(pwr)    
    
    
    def __delitem__(self, pwr): 
        if pwr < 0 or type(pwr) != int: 
            raise TypeError("Not a Good power") 
        if pwr in self.terms: 
            self.terms.pop(pwr) 
            self.list_powers.remove(pwr)
            
    def _add_term(self, coef, pwr): 
        if pwr < 0 or type(pwr) != int: 
            raise TypeError("Not a Good power")
        if type(coef) != int: 
            raise TypeError("Cannot be a coefficient") 
        if coef == 0:
            if pwr not in self.terms:
                pass
            else: 
                self.list_powers.remove(pwr) 
                self.terms.pop(pwr)
        elif pwr in self.terms: 
            self.terms[pwr] = self.terms[pwr] + coef 
        elif self.terms == {}: 
            self.terms[pwr] = coef 
            self.list_powers.append(pwr) 
        elif pwr not in self.terms: 
            if pwr == 0: 
                self.list_powers.append(pwr)
            else:    
                for i in range(len(self.list_powers)): 
                    if pwr > self.list_powers[i]: 
                        self.list_powers.insert(i, pwr)
                        break
             
            self.terms[pwr] = coef 
        
    def __pos__(self):
        newPoly = Poly()  
        newPoly.list_powers = self.list_powers 
        newPoly.terms = self.terms
        return newPoly 
    
    def __neg__(self): 
        newPoly = Poly() 
        newPoly.list_powers = self.list_powers
        newPoly.terms = self.terms 
        for key in newPoly.terms: 
            newPoly[key] = newPoly[key] * -1 
        return newPoly 
    
    def __abs__(self):
        newPoly = Poly() 
        newPoly.list_powers = self.list_powers
        newPoly.terms = self.terms 
        for key in newPoly.terms: 
            if newPoly[key] < 0: 
                newPoly[key] = newPoly[key] * -1 
        return newPoly 
    
    def differentiate(self):
        newPoly = Poly() 
        list = []
        newPoly.list_powers = self.list_powers
        newPoly.terms = self.terms 
        for pwr in newPoly.list_powers:  
            if pwr == 0: 
                pass
            else:
                list.append((pwr-1,pwr*newPoly.terms[pwr]))

        newPoly.terms = {}
        newPoly.list_powers = []
        for tu in list:     
            newPoly.terms[tu[0]] = tu[1] 
            newPoly.list_powers.append(tu[0])  
               
        return newPoly 
    
    def integrate(self, constant):
        newPoly = Poly() 
        list = []
        newPoly.list_powers = self.list_powers
        newPoly.terms = self.terms 
        for pwr in newPoly.list_powers:      
            list.append((pwr+1, newPoly.terms[pwr]/(pwr+1))) 
        list.append((0,constant)) 
        
        newPoly.terms = {}
        newPoly.list_powers = []
        for tu in list:     
            newPoly.terms[tu[0]] = tu[1] 
            newPoly.list_powers.append(tu[0])
        return newPoly 
    
    def def_integrate(self, lower, upper):
        equation = self.integrate(0) 
        return equation(upper) - equation(lower) 
    
    def __add__(self, other):          
        newPoly = Poly() 
        newPoly.terms = self.terms.copy() 
        newPoly.list_powers = self.list_powers.copy() 
         
        if type(other) == int or type(other) == float:
            if 0 in newPoly.list_powers: 
                newPoly.terms[0] = newPoly[0] + other 
            else: 
                newPoly.terms[0] = other 
                newPoly.list_powers.append(0) 
        elif type(other) == Poly: 
            for num in other.list_powers: 
                if num in newPoly.list_powers: 
                    newPoly.terms[num] += other.terms[num] 
                else: 
                    newPoly.list_powers.append(num) 
                    newPoly.terms[num] = other.terms[num]
            newPoly.list_powers.sort(key=None, reverse=True) 
        else: 
            raise TypeError
        return newPoly

    def __radd__(self, other):
        newPoly = Poly() 
        newPoly.terms = self.terms.copy() 
        newPoly.list_powers = self.list_powers.copy() 
         
        if type(other) == int or type(other) == float:
            if 0 in newPoly.list_powers: 
                newPoly.terms[0] = newPoly[0] + other 
            else: 
                newPoly.terms[0] = other 
                newPoly.list_powers.append(0) 
        elif type(other) == Poly: 
            for num in other.list_powers: 
                if num in newPoly.list_powers: 
                    newPoly.terms[num] += other.terms[num] 
                else: 
                    newPoly.list_powers.append(num) 
                    newPoly.terms[num] = other.terms[num]
            newPoly.list_powers.sort(key=None, reverse=True) 
        else: 
            raise TypeError
        return newPoly

    def __sub__(self, other): 
        newPoly = Poly() 
        newPoly.terms = self.terms.copy() 
        newPoly.list_powers = self.list_powers.copy() 
         
        if type(other) == int or type(other) == float:
            if 0 in newPoly.list_powers: 
                newPoly.terms[0] = newPoly[0] - other 
            else: 
                newPoly.terms[0] = other*-1 
                newPoly.list_powers.append(0) 
        elif type(other) == Poly: 
            for num in other.list_powers: 
                if num in newPoly.list_powers: 
                    newPoly.terms[num] -= other.terms[num] 
                else: 
                    newPoly.list_powers.append(num) 
                    newPoly.terms[num] = other.terms[num]*-1
            newPoly.list_powers.sort(key=None, reverse=True) 
        else: 
            raise TypeError
        return newPoly
    
    def __rsub__(self, other):
        newPoly = Poly() 
        newPoly.terms = self.terms.copy() 
        newPoly.list_powers = self.list_powers.copy() 
         
        if type(other) == int or type(other) == float:
            for obj in newPoly.terms: 
                newPoly.terms[obj] *= -1 
            if 0 in newPoly.list_powers: 
                newPoly.terms[0] = newPoly[0] + other 
            else: 
                newPoly.terms[0] = other*-1 
                newPoly.list_powers.append(0) 
        elif type(other) == Poly: 
            for num in other.list_powers: 
                if num in newPoly.list_powers: 
                    newPoly.terms[num] -= other.terms[num] 
                else: 
                    newPoly.list_powers.append(num) 
                    newPoly.terms[num] = other.terms[num]*-1
            newPoly.list_powers.sort(key=None, reverse=True) 
        else: 
            raise TypeError
        return newPoly

    def __mul__(self, other):
        newPoly = Poly() 
        newPoly.terms = self.terms.copy() 
        newPoly.list_powers = self.list_powers.copy()
        finalPoly = Poly()
        if type(other) == int or type(other) == float:
            for obj in newPoly.terms: 
                newPoly.terms[obj] *= other 
            finalPoly = newPoly     
            
        elif type(other) == Poly: 
            terms_dict = {}
            count = 0 
            for pwr1, coef1 in other.terms.items():   
                for pwr2, coef2 in newPoly.terms.items():
                    terms_dict[pwr1+pwr2] = coef1 * coef2 
                    finalPoly._add_term(coef1 * coef2, pwr1+pwr2)
                    if pwr1+pwr2 not in finalPoly.list_powers: 
                        finalPoly.list_powers.append(pwr1+pwr2) 
                        
            finalPoly.list_powers.sort(key=None, reverse=True)
        else: raise TypeError
        
            
        return finalPoly 
    
    def __rmul__(self, other):
        newPoly = Poly() 
        newPoly.terms = self.terms.copy() 
        newPoly.list_powers = self.list_powers.copy()
        finalPoly = Poly()
        if type(other) == int or type(other) == float:
            for obj in newPoly.terms: 
                newPoly.terms[obj] *= other 
            finalPoly = newPoly     
            
        elif type(other) == Poly: 
            terms_dict = {}
            count = 0 
            for pwr1, coef1 in other.terms.items():   
                for pwr2, coef2 in newPoly.terms.items():
                    terms_dict[pwr1+pwr2] = coef1 * coef2 
                    finalPoly._add_term(coef1 * coef2, pwr1+pwr2)
                    if pwr1+pwr2 not in finalPoly.list_powers: 
                        finalPoly.list_powers.append(pwr1+pwr2) 
                        
            finalPoly.list_powers.sort(key=None, reverse=True)
        else: raise TypeError
        
            
        return finalPoly 
    
    def __pow__(self, other):
        newPoly = Poly() 
        newPoly.list_powers = self.list_powers.copy() 
        newPoly.terms = self.terms.copy()  
        if type(other) != int or other < 0: 
            raise TypeError 
        elif other == 0:  
            return 1   
        else:
            x = Poly() 
            x.list_powers = self.list_powers.copy() 
            x.terms = self.terms.copy()  
            for i in range(1, other): 
                newPoly *= x
                
        return newPoly  
    
    def __eq__(self, other):
        if type(other) != Poly and type(other) != int and type(other) != float: 
            raise TypeError 
        elif type(other) == int: 
            if self.list_powers[0] == 0 and type(other) == int: 
                if self.terms[0] == other: 
                    return True 
        elif type(other) == Poly: 
            if other.terms == self.terms: 
                return True 
        return False
    
    def __lt__(self, other):
        
        
        if type(other) not in (int,Poly) or type(self) not in (int,Poly): 
            raise TypeError  
        
        if type(other) == int and self.list_powers[0] == 0: 
            if self.terms[0] < other: 
                return True 
            else: 
                return False 
            
        elif type(self) == int and other.list_powers[0] == 0: 
            if other.terms[0] < self: 
                return True 
            else: 
                return False
            
        elif self.list_powers[0] < other.list_powers[0]: 
            return True 
        
        elif self.list_powers[0] == other.list_powers[0]: 
            term = self.list_powers[0]
            if self.terms[term] < other.terms[term]: 
                return True
            
        return False
    
    def __gt__(self, other):
        if type(other) not in (int,Poly) or type(self) not in (int,Poly): 
            raise TypeError  
        
        if type(other) == int and self.list_powers[0] == 0: 
            if self.terms[0] > other: 
                return True 
            else: 
                return False 
            
        elif type(self) == int and other.list_powers[0] == 0: 
            if other.terms[0] > self: 
                return True 
            else: 
                return False
            
        elif self.list_powers[0] > other.list_powers[0]: 
            return True 
        
        elif self.list_powers[0] == other.list_powers[0]: 
            term = self.list_powers[0]
            if self.terms[term] > other.terms[term]: 
                return True
            
        return False 
    
    def __le__(self, other): 
        if type(self) not in (int,Poly) or type(other) not in (int,Poly): 
            raise TypeError 
        elif self < other or self == other: 
            return True 
        return False 
    
    def __ge__(self, other): 
        if type(self) not in (int,Poly) or type(other) not in (int,Poly): 
            raise TypeError 
        elif self > other or self == other: 
            return True 
        return False 
    
    
  
        
    
    
            
         
        
if __name__ == '__main__':
    #Simple tests before running driver

    
    #Put your own test code here to test Poly before doing bsc tests
    #Debugging problems with tests is simpler

    print('Start of simple tests')
    p = Poly((3,2),(-2,1),(4,0))
    print('  For Polynomial: 3x^2 - 2x + 4')
    
    print('  str(p):',p)
    print('  repr(p):',repr(p))
    
    print('  len(p):',len(p))
    print('  p(2):',p(2))
    print('  list collecting the iterator results:', [t for t in p])
    print('  p+p:',p+p)
    print('  p+2:',p+2)
    print('  p*p:',p*p)
    print('  p*2:',p*2)
    print('End of simple tests\n\n')
    
    import driver
    driver.default_file_name = 'bscp22W20.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()     
