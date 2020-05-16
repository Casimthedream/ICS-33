import goody


def read_ndfa(file : open) -> {str:{str:{str}}}:
    ndfa_dict = {} 
    for line in file: 
        ndfa = line.split(';') 
        ndfa[-1] = ndfa[-1].strip('\n') 
        ndfa_dict[ndfa[0]] = {} 
        real_dict = ndfa_dict[ndfa[0]] 

        real_ndfa = ndfa[1::] 
        for i in range(len(real_ndfa)): 
            
            if i % 2 == 0: 
                if real_ndfa[i] in real_dict.keys(): 
                    real_dict[real_ndfa[i]].add(real_ndfa[i+1]) 
                else:
                    real_dict[real_ndfa[i]] = {real_ndfa[i+1]} 
            if i % 2 == 1: 
                pass
    file.close()
    return ndfa_dict


def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    ndfa_str = ''
    for i in range(len(sorted(ndfa.keys()))): 
        ndfa_list = []
        
        keys = sorted(ndfa.keys())[i]
        if len(keys) != 0: 
            if len(keys) > 1: 
                state_list = []
                sort_keys = sorted(ndfa[keys].keys()) 
                for i in range(len(sort_keys)):
                    ndfa_list.append((sort_keys[i], sorted(list(ndfa[keys][sort_keys[i]])) ) )  
            else:    
                for k,v in ndfa[keys].items(): 
                    
                    ndfa_list.append((k,sorted(v)))
             
            ndfa_str += "  " + str(keys) + " transitions: " + str(ndfa_list) + '\n'
        else: 
            ndfa_str += "  " + str(keys) + " transitions: " + str(ndfa[keys]) + '\n'
    return ndfa_str

def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    process_list = [] 
    process_list.append(state) 
    last_states = set()
    options = set()
    all_keys = set()
    for k,v in ndfa.items(): 
        for key in v: 
            all_keys.add(key) 

    for i in range(len(inputs)):
        
        if i == 0: 
            if str(inputs[i]) not in all_keys: 
                return process_list
            state_dict = ndfa[state]
            for obj in state_dict[str(inputs[i])]: 
                options.add(obj)
                last_states.add(obj)
            process_list.append((inputs[i], set(sorted(options))))
            #process_list.append((inputs[i], sorted(options)))
            
            
        else:
         
            last_states = options.copy()  
            all_keys = set() 
            for k in last_states: 
                for keys in ndfa[k]: 
                    all_keys.add(keys)
            if str(inputs[i]) not in all_keys:
                process_list.append((inputs[i], set()))
                return process_list  
            
            options = set() 
            for states in last_states:
                state_dict = ndfa[states] 
                #return state_dict[str(inputs[i])]
                if str(inputs[i]) not in state_dict: 
                    pass 
                else: 
                    for obj in state_dict[str(inputs[i])]: 
                        #return state_dict[str(inputs[i])]
                        options.add(obj)
            process_list.append((inputs[i], set(sorted(options))))
            #process_list.append((inputs[i], sorted(options)))
            
            
    return process_list
    

def interpret(result : [None]) -> str:
    final = "Start state = " + result[0] + "\n" 
    steps = result[1::] 
    for i in range(len(steps)):
        
        final += "  Input = " + str(steps[i][0]) + "; new possible states = " + str(sorted(steps[i][1])) + '\n' 
    
    final += "Stop state(s) = " + str(sorted(steps[-1][1])) + '\n'
    return final 
 
          
   





if __name__ == '__main__':
    # Write script here
    fa = input("Pick the file name containing this Non-Deterministic Finite Automaton: ")
    k = read_ndfa(open(fa))
    print() 
    print("The Contents of the file picked for this Non-Deterministic Finite Automaton ")  
    print(ndfa_as_str(k)) 
    print() 
    file_inputs = input(" Pick the file name containing a sequence of start-states and subsequent inputs: ")
    print()
    infile = open(file_inputs, "r") 
    for line in infile: 
        line = line.strip('\n')
        inputs = line.split(';')
        input_list = inputs[1::]
        results = process(k, inputs[0], input_list) 
        print("Commence tracing this NDFA from its start-state") 
        print(interpret(results)) 
    infile.close() 
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc4.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
