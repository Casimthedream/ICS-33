from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # We start by binding the class attribute to True meaning checking can occur
    #   (but only when the function's self._checking_on is also bound to True)
    checking_on  = True
  
    # For checking the decorated function, bind its self._checking_on as True
    def __init__(self, f):
        self._f = f
        self._checking_on = True
        self._return_values = []
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        tie = annot
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        def check_type(par,ann,val):
    
            if isinstance(val, ann) == False: 
                raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(val)+ 
                      '\', was type ' + str(type(val)) + "... should be type " + str(ann) )
            
                
    
        def check_list(par,ann,val):  
            if len(ann) == 1: 
                
                if type(val) != list: 
                    raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(val)+ 
                      '\', was type ' + str(type(val)) + "... should be type " + str(ann) )          
                
                if type(ann[0]) == list: 
                    for i in val: 
                        check_list(par,ann[0],i)
                elif type(ann[0]) == tuple: 
                    for i in val: 
                        check_tuple(par, ann[0], i)
                elif type(ann[0]) != list:
                    for i in val: 
                        self.check(par,ann[0],i)
                        
                elif len(val) > 1: 
                    for i in range(len(val)):
                        if isinstance(val[i], ann[0]) == False:
                            raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(val[i])+ 
                      '\', was type ' + str(type(val[i])) + "... should be type " + str(ann[0]))   
                        
            elif len(ann) > 1: 
                if len(ann) != len(val): 
                    raise AssertionError("Parameter List does not have same size as value list")
                
                for i in range(len(ann)): 
                    if isinstance(val[i], ann[i]) == False: 
                        raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(val[i])+ 
                      '\', was type ' + str(type(val[i])) + "... should be type " + str(ann[i])) 
                    
        def check_tuple(par,ann,val): 
            if type(val) != tuple:
                raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(val)+ 
                      '\', was type ' + str(type(val)) + "... should be type " + str(ann) )  
            
            if len(ann) == 1 : 
                if type(val) != tuple: 
                    raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(val)+ 
                      '\', was type ' + str(type(val)) + "... should be type " + str(ann) )
                
                if type(ann[0]) == tuple: 
                    for i in val: 
                        check_tuple(par, ann[0],i) 
                        
                elif type(ann[0]) == list: 
                    for i in val: 
                        check_list(par, ann[0],i)
                        
                elif len(val) > 1: 
                    for i in range(len(val)): 
                        if isinstance(val[i],ann[0]) == False:
                            raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(val[i])+ 
                      '\', was type ' + str(type(val[i])) + "... should be type " + str(ann[0]) )
                        
            elif len(ann) > 1: 
                if len(ann) != len(val): 
                    raise AssertionError("Parameter Tuple does not have same size as Value Tuple")
                
                for i in range(len(ann)): 
                    if isinstance(val[i], ann[i]) == False: 
                        raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(val[i])+ 
                      '\', was type ' + str(type(val[i])) + "... should be type " + str(ann[i]) ) 
            
        def check_dict(par,ann,val): 
            if isinstance(val, dict) == False: 
                raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(val)+ 
                      '\', was type ' + str(type(val)) + "... should be type " + str(ann) )
            if len(ann) > 1: 
                raise AssertionError( par + "annotation inconsistency: dict should have 1 item but had " +
                                      str(len(ann)) + "\n annotation = " + str(ann)  )
                 
            for key, value in ann.items(): 
                for k,v in val.items(): 
                    if isinstance(k, key) == False: 
                        raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(k)+ 
                      '\', was type ' + str(type(k)) + "... should be type " + str(key) )
                    if isinstance(v,value) == False:  
                        raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(v)+ 
                      '\', was type ' + str(type(v)) + "... should be type " + str(value) )
                        
        def check_set(par, ann, val):
            if isinstance(val, set) == False: 
                raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(val)+ 
                      '\', was type ' + str(type(val)) + "... should be type " + str(ann) ) 
            
            if len(ann) > 1: 
                raise AssertionError( par + "annotation inconsistency: set should have 1 item but had " +
                                      str(len(ann)) + "\n annotation = " + str(ann)  ) 
            
            else: 
                for i in val: 
                    if type(i) not in ann:
                        for v in ann:  
                            raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(i)+ 
                                                  '\', was type ' + str(type(i)) + "... should be type " + str(v) ) 
                    
        def check_fset(par, ann, val):
            if isinstance(val, frozenset) == False: 
                raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(val)+ 
                      '\', was type ' + str(type(val)) + "... should be type " + str(ann) )
                 
            if len(ann) > 1: 
                raise AssertionError( par + "annotation inconsistency: set should have 1 item but had " +
                                      str(len(ann)) + "\n annotation = " + str(ann)  )  
            else: 
                for i in val: 
                    if type(i) not in ann:
                        for v in ann: 
                            raise AssertionError( par + " failed annotation check(wrong type): value = \'" + str(i)+ 
                                                  '\', was type ' + str(type(i)) + "... should be type " + str(v) )  
            
        def check_lambda(par, ann, val):
            if len(ann.__code__.co_varnames) == 0 or len(ann.__code__.co_varnames) > 1: 
                raise AssertionError( par + "annotation inconsistency: set should have 1 item but had " +
                                      str(len(ann.__code__.co_varnames)) ) 
            
            try:   
                if ann(val) == False: 
                    raise AssertionError ( par + " failed annotation check(wrong type): value = \'" + str(val)+ 
                      '\', was type ' + str(type(val)) + "... should be type " + str(ann) ) 
            except: 
                raise AssertionError 
            
        def check_other(par, ann, val):
            try: 
                if ann.__check_annotation__: 
                    pass 
            except AttributeError: 
                raise AssertionError 
            
                    
        
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)
        # We start by comparing check's function annotation to its arguments
        
        if tie == None: 
            pass 
        elif type(annot) == type: 
            check_type(param,annot,value)
        elif type(tie) == list:
            check_list(param, annot, value)      
        elif type(tie) == tuple: 
            check_tuple(param, annot, value)
        elif type(tie) == dict: 
            check_dict(param,annot,value) 
        elif type(tie) == set: 
            check_set(param,annot,value)    
        elif type(tie) == frozenset: 
            check_fset(param,annot,value)
        elif type(tie) == type(lambda x : x): 
            check_lambda(param,annot,value)
        else: 
            check_other(param,annot,value)
        
        
        
            
        
            
         
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Returns the parameter->argument bindings as an ordereddict, derived
        #   from dict, binding the function header's parameters in order
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        if self.checking_on == False: 
            return self._f(*args) 
        
        try:
            # Check the annotation for each of the annotated parameters
            # Compute/remember the value of the decorated function
            # If 'return' is in the annotation, check it 
            # Return the decorated answer
            #return self._f(*)
            if self.checking_on: 
                dict_params = param_arg_bindings() 
                
              
                for vars,vals in dict_params.items():
                    self.check(vars,self._f.__annotations__[vars],vals,'') 
                    
                answer = self._f(*args) 
                self._return_values.append(answer)
                if 'return' in  self._f.__annotations__: 
                    dict_params['_return'] = answer  
                    self.check('_return',self._f.__annotations__['return'],answer) 
                return answer 
                
                    
                    #self.check()
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
            #print(80*'-')
            #for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
            #    print(l.rstrip())
            #print(80*'-')
            raise AssertionError




  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
    def f(x : int): pass
    f = Check_Annotation(f)
    #f('a')
    #f((1))
    #f([1])
    #f(['a',2])
   
    #driver tests
    import driver
    driver.default_file_name = 'bscp4W20.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
