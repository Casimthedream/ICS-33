import goody


def read_fa(file : open) -> {str:{str:str}}:
    fa_dict = {}
    for line in file: 
        chars = line.split(';') 
        chars[-1] = chars[-1].strip("\n") 
        fa_dict[chars[0]] = {}
        inside_dict = fa_dict[chars[0]]
        def_list = chars[1::]
        for i in range(len(def_list)): 
            if i%2 == 0:
                inside_dict[def_list[i]] = def_list[i+1]
            if i%2 == 1: 
                pass 
         
    
    
    file.close() 
    return fa_dict


def fa_as_str(fa : {str:{str:str}}) -> str:
    fa_str = "" 
    fa_new = {}
    keys = sorted(fa.keys()) 
    for i in range(len(keys)): 
        fa_new[keys[i]] = fa[keys[i]] 
        
    for k,v in fa_new.items(): 
        fa_set = []
        for key,value in v.items(): 
            fa_set.append((key, value))
        fa_set.sort()
        fa_str += "  " + str(k) + " transitions: " + str(fa_set) + "\n" 
    return fa_str 

    
def process(fa : {str:{str:str}}, state : str, inputs : [str]) -> [None]:
    list_states = []
    list_states.append(state) 
    state_dict = fa[state]
    for i in range(len(inputs)): 
        if i > 0:
            state_dict = fa[list_states[-1][1]]
        if inputs[i] in state_dict.keys(): 
            list_states.append((inputs[i], state_dict[inputs[i]])) 
        else: 
            list_states.append((inputs[i], None))
            return list_states
    return list_states

def interpret(fa_result : [None]) -> str:
    result = fa_result[1::] 
    output = 'Start state = ' + fa_result[0] + "\n" 
    for i in range(len(result)): 
        in_out = result[i] 
        output += "  Input = " + str(in_out[0]) +"; "
        if in_out[1] == None: 
            output += "illegal input: simulation terminated\n" 
            output += "Stop state = None\n"
            return output 
        else: 
            output += "new state = " + str(in_out[1]) + '\n'
    output += "Stop state = " + str(result[-1][1]) + '\n'
    return output  
    




if __name__ == '__main__':
    # Write script here
    fa = input("Pick the file name containing this Finite Automaton: ")
    k = read_fa(open(fa))
    print() 
    print("The Contents of the file picked for this Finite Automaton ")  
    print(fa_as_str(k)) 
    print() 
    file_inputs = input(" Pick the file name containing a sequence of start-states and subsequent inputs: ")
    print()
    infile = open(file_inputs, "r") 
    for line in infile: 
        line = line.strip('\n')
        inputs = line.split(';')
        input_list = inputs[1::]
        results = process(k, inputs[0], input_list) 
        print("Commence tracing this FA from its start-state") 
        print(interpret(results)) 
    infile.close() 
        
              
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc3.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
