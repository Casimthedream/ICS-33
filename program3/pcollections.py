import re, traceback, keyword

def pnamedtuple(type_name, field_names, mutable = False, defaults = {}):
    def show_listing(s):
        for line_number, line_text in enumerate( s.split('\n'),1 ):  
            print(f' {line_number: >3} {line_text.rstrip()}')

    # put your code here
    regex = re.compile("^[a-z,A-Z]([a-z,A-Z,\d,_]*)$")
    def unique(iterable):           #taken from lecture notes
        iterated = set()
        for i in iterable:
            if i not in iterated:
                iterated.add(i)
                yield i 
                
    if type(type_name) != str: 
        raise SyntaxError
    if regex.match(type_name) == None: 
        raise SyntaxError 
    if type_name in keyword.kwlist: 
        raise SyntaxError
    
    if type(field_names) == list: 
        new_list = [i for i in unique(field_names)] 
        for i in new_list: 
            if regex.match(i) == None: 
                raise SyntaxError
            if i in keyword.kwlist: 
                raise SyntaxError
             
    elif type(field_names) == str: 
         new_list = [i for i in unique(re.split(",| ", field_names) )]
         if "" in new_list: 
             new_list.remove("")
         field_names = new_list
         for i in new_list: 
            if regex.match(i) == None: 
                raise SyntaxError
            if i in keyword.kwlist: 
                raise SyntaxError
    else: 
        raise SyntaxError
        
    # bind class_definition (used below) to the string constructed for the class
    def gen_init(iter): 
        s = "   def __init__(self," 
        
        for i in range(len(iter)):
            
            if i == len(iter)-1:
                if iter[i] in defaults: 
                   s += " " + iter[i] +"="+str(defaults[iter[i]])
                else:    
                    s += " " + iter[i] 
            else:
                if iter[i] in defaults: 
                   s += " " + iter[i] +"="+str(defaults[iter[i]])+','
                else:
                    s += " " + iter[i] +','
                
        s += "):\n"
        
        for i in iter:
            s += "        self." + i + " = " + i +'\n'
        return s

    def gen_repr(iter): 
        s = "    def __repr__(self):\n"
        s += "        return f'" + str(type_name) + "(" 
        
        for i in range(len(iter)): 
            if i == len(iter)-1:
                s += str(iter[i])+ '={self.' + str(iter[i]) +"})'"
            else:   
                s += str(iter[i])+ '={self.' + str(iter[i])+"},"
        return s + '\n'
    
    def gen_get(iter):
        s = ""
        for i in range(len(iter)): 
            s += "    def get_"+str(iter[i])+"(self):\n"
            s += "        return self." + str(iter[i]) + '\n'
        return s 
    
    def gen_getitem(): 
        s = "    def __getitem__(self, var):\n"
        s += "        if type(var) == int:\n"
        s += "            if var > len(self._fields) or var < 0:\n"
        s += "                raise IndexError\n"
        s += "            y = self._fields[var]\n"
        s += "            string = \'self.get_\' + str(y) + \'()\' \n"
        s += "            return eval(string)\n"
        s += "        elif type(var) == str:\n"
        s += "            if var not in self._fields:\n"
        s += "                raise IndexError\n"
        s += "            return self._fields.index(var)+1\n"
        s += "        else: raise IndexError\n"
        
        return s 
    
    def gen_eq(): 
        s = "    def __eq__(self, other):\n" 
        s += "        if type(self) == type(other):\n"
        s += "            for i in range(len(self._fields)):\n"
        s += "                if eval('self.get_'+str(self._fields[i])+'()') == eval(\'other.get_\'+str(self._fields[i])+\'()\'):\n" 
        s += "                    pass\n"
        s += "                else: return False\n"
        s += "            return True\n" 
        s += "        else: return False\n"
        return s 
    
    def gen_dict(): 
        s  = "    def _asdict(self):\n" 
        s += "        v_dict = {}\n" 
        s += "        for i in range(len(self._fields)):\n" 
        s += "            v_dict[self._fields[i]] = eval(\'self.get_\'+str(self._fields[i])+\'()\')\n" 
        s += "        return v_dict\n"
        return s 
    
    def gen_make(iter):
        s = "    def _make(iter):\n"
        s += "        m =" + str(type_name) + "(" 
        for i in range(len(iter)):
            if i == len(iter)-1: 
                s += str(iter[i]) + "=iter["+str(i)+'])\n'
            else:
                s += str(iter[i]) + "=iter["+str(i)+'],'
        s += "        return m\n" 
        return s 
    
    def gen_replace():
        s = "    def _replace(self, **kargs):\n"
        s += "        for i in kargs:\n"
        s += "            if i not in self._fields:\n"
        s += "                raise TypeError\n "
        s += "       if self._mutable == True:\n" 
        s += "            for i in range(len(self._fields)):\n"
        s += "                if self._fields[i] in kargs:\n" 
        s += "                    self.__dict__[self._fields[i]] = kargs[self._fields[i]]\n"
        s += "        else:\n" 
        s += "            for i in self._fields:\n" 
        s += "                if i not in kargs:\n"
        s += "                    kargs[i] = self.__dict__[i]\n"
        s += "            m =" + str(type_name) + "(**kargs)\n"
        s += "            return m\n" 
        return s
        


# For debugging, uncomment next line, which shows source code for the class
# show_listing(class_definition)
    c = '''\
class '''+str(type_name)+''': 
    _fields = ''' +  str(field_names) + '''
    _mutable = '''+str(mutable) + '''\n ''' 
    print(field_names)
    
    i = gen_init(field_names)
    
    r = gen_repr(field_names)
    
    g = gen_get(field_names)
    
    gi = gen_getitem() 
    
    eq = gen_eq()
    
    d = gen_dict() 
    
    m = gen_make(field_names)
    
    rp = gen_replace()
    
    class_definition = c+i+r+g+gi+eq+d+m+rp
    
    
    # Execute the class_definition (a str), in a special name space; then bind
    #   its source_code attribute to class_definition; after try/except return the
    #   class object created; if there is a syntax error, list the class and
    #   also show the error
    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )      
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):          
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test simple pnamedtuple below in script: Point=pnamedtuple('Point','x,y')
    #Triple1    = pnamedtuple('Triple1', 'a b c', defaults={'a':1})
    #driver tests
    import driver  
    driver.default_file_name = 'bscp3W20.txt'
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
