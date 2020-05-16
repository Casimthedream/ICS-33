import prompt
import goody

# Use these global variables to index the list associated with each name in the dictionary.
# e.g., if men is a dictionary, men['m1'][match] is the woman who matches man 'm1', and 
# men['m1'][prefs] is the list of preference for man 'm1'.
# It would seems that this list might be better represented as a named tuple, but the
# preference list it contains is mutated, which is not allowed in a named tuple. 

match = 0   # Index 0 of list associate with name is match (str)
prefs = 1   # Index 1 of list associate with name is preferences (list of str)


def read_match_preferences(open_file : open) -> {str:[str,[str]]}:
    pref = {} 
    for line in open_file: 
        line = line.rstrip()
        peeps = line.split(';') 
        pref[peeps[0]] = [None, []] 
        for i in range(1, len(peeps)): 
            pref[peeps[0]][1].append(peeps[i])
    open_file.close() 
    return pref 
         
         
    


def dict_as_str(d : {str:[str,[str]]}, key : callable=None, reverse : bool=False) -> str:
    str_dict = ''
    if reverse == False and key == None: 
        list_keys = [] 
        for k in d: 
            list_keys.append(k) 
            list_keys.sort() 
        for i in range(len(d)): 
            str_dict += '  ' + list_keys[i] + ' -> ' + str(d[list_keys[i]]) + '\n'
        return str_dict
        
    if reverse == True and key == None: 
        list_keys = [] 
        for k in d: 
            list_keys.append(k) 
            list_keys.sort(reverse = True) 
        for i in range(len(d)): 
            str_dict += '  ' + list_keys[i] + ' -> ' + str(d[list_keys[i]]) + '\n' 
        return str_dict
        
    if reverse == True: #Both params are filled  
        list_keys =[] 
        for k,v in d.items(): 
            list_keys.append(v) 
            list_keys.sort(reverse = True)
        for i in range(len(list_keys)): 
            for k in d: 
                if d[k] == list_keys[i]: 
                    str_dict += '  ' + k + ' -> ' + str(list_keys[i]) + '\n' 
        return str_dict         
    
    list_keys =[]       
    for k,v in d.items(): 
        list_keys.append(v) 
        list_keys.sort()
    for i in range(len(list_keys)): 
        for k in d: 
            if d[k] == list_keys[i]: 
                str_dict += '  ' + k + ' -> ' + str(list_keys[i]) + '\n'        
    return str_dict


def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    prefer = '' 
    prefer_dict = {}
    
    for i in range(len(order)): 
        if p1 == order[i]: 
            prefer_dict[p1] = i 
        elif p2 == order[i]: 
            prefer_dict[p2] = i 
            
    if prefer_dict[p1] < prefer_dict[p2]: 
        prefer = p1
    else: 
        prefer = p2 
        
    return prefer

def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    return set((k,v[0]) for k,v in men.items())


def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:
    unmatched_men = set()
    matches = set()
    men_copy = men.copy()
    
    for k in men: 
        unmatched_men.add(k) 
        
    while unmatched_men != set(): 
        
        if trace == True: 
            print("Women Preferences (unchanging)")
            print(dict_as_str(women))
            print()
            print("Men Preferences (current)" )
            print(dict_as_str(men))
            print()
            print("unmatched men = ", unmatched_men)
            print() 
        
        for man in unmatched_men: 
            list_women = men[man][1]
    
            for i in range(len(list_women)):
                first_choice = list_women[i]
                
                if women[first_choice][0] == None and men[man][0] == None: 
                    
                    matches.add((man, first_choice))
                    list_women.remove(first_choice) 
                    men[man][0] = first_choice
                    women[first_choice][0] = man
                    unmatched_men.discard(man)
                    if trace == True: 
                        print(man + " proposes to " + first_choice + ", an unmatched woman, who accepts the proposal")
                        print()
                    break
                
                elif women[first_choice][0] != None and men[man][0] == None: 
                    list_men = women[first_choice][1]
                    married_man = women[first_choice][0] 
                    if who_prefer(list_men, man, married_man) == man: 
                        
                       matches.discard((married_man,first_choice))
                       unmatched_men.discard(man) 
                       unmatched_men.add(married_man)
                       matches.add((man, first_choice))
                       list_women.remove(first_choice)
     
                       women[first_choice][0] = man 
                       men[man][0] = first_choice
                       
                       men[married_man][0] = None
                       if trace == True: 
                           print(man + " proposes to " + first_choice + ", an unmatched woman, who accepts the proposal (she prefers her new match)")
                           print()
                       break  
                    if trace == True:
                        print(man + " proposes to " + first_choice + ", an unmatched woman, who accepts the proposal (she prefers her current match)")
                        print()
            break
    if trace == True:
        print("Algorithm traced: the final matches = ", matches)    
    return matches    

  
    
if __name__ == '__main__':

    # Write script here
    menfile = input("Pick the file name containing the preferences for men: ")
    m0 = read_match_preferences(open(menfile)) 
    womenfile = input("Pick the file name containing the preferences for women: ")
    w0 = read_match_preferences(open(womenfile)) 
    print()
    print("Men Preferences ")
    print(dict_as_str(m0))
    print()
    print("Women Preferences ")
    print(dict_as_str(w0))
    print()
    trace = input("Produce Trace of Algorithm[True]: ")
    while trace.lower() != 'false' and trace.lower() != 'true': 
        trace = input("Error: Input must be True or False ") 
    if trace.lower() == 'false': 
        matches = make_match(m0, w0)
        print()
        print("The final matches = ", matches) 
    elif trace.lower() == 'true': 
        make_match(m0, w0, True) 

                  
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
    
    
    