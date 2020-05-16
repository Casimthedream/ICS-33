import prompt 
from goody       import safe_open,irange
from collections import defaultdict # Use defaultdict for prefix and query


def all_prefixes(fq : (str,)) -> {(str,)}:
    prefixes = set() 
    for i in range(1,len(fq)+1): 
        end = len(fq) - i
        prefixes.add((fq[:i])) 
    return prefixes   

def add_query(prefix : {(str,):{(str,)}}, query : {(str,):int}, new_query : (str,)) -> None:
    new_pref = all_prefixes(new_query) 
    
    for obj in new_pref: 
        prefix[obj].add(new_query) 
        
    if new_query in query: 
        query[new_query] += 1 
    else: 
        query[new_query] = 1 
    

def read_queries(open_file : open) -> ({(str,):{(str,)}}, {(str,):int}):
    p = defaultdict(set) 
    q = defaultdict(int) 
    list_of_lines = []
    for line in open_file: 
        chars = line.split() 
        chars[-1].strip('\n') 
        list_of_lines.append(tuple(chars)) 
    for i in range(len(list_of_lines)):
        add_query(p, q, list_of_lines[i])
        
    p_sorted = defaultdict(set)
    length = 1 
    
    p_list = []
    for k in p:
        length = len(k) 
        p_set = []
        for key in p: 
            if len(key) == length:  
                if key not in p_set: 
                    p_set.append(key) 
        if p_set not in p_list: 
            
            p_list.append(p_set) 
                       
    for i in range(len(p_list)): 
        p_list[i] = sorted((p_list[i])) 
        
    
    for i in range(len(p_list)): 
        for j in range(len(p_list[i])): 
            p_sorted[p_list[i][j]] = p[p_list[i][j]]         
    
    
    q_sorted = defaultdict(int) 
    q_list = sorted(q, key = lambda x : q[x], reverse = True)
    for obj in q_list: 
        q_sorted[obj] = q[obj] 
    
    
        
    return (p_sorted, q_sorted) 


def dict_as_str(d : {None:None}, key : callable=None, reverse : bool=False) -> str:
    real_str = '' 
    
    if reverse == True: 
        d_reverse = sorted(d, key = key, reverse = reverse)
        for k in d_reverse: 
            real_str += "  " + str(k) + " -> " + str(d[k]) + '\n'
    else:
        dd = sorted(d, key = key)      
        for k in dd: 
            real_str += "  " + str(k) + " -> " + str(d[k]) + '\n' 
        
    return real_str


def top_n(a_prefix : (str,), n : int, prefix : {(str,):{(str,)}}, query : {(str,):int}) -> [(str,)]:
    search = [] 
    if a_prefix not in prefix: 
        return search
    pref = prefix[a_prefix]
    
    list = sorted(query, key = lambda x: query[x])
    list.reverse() 
     
    
         
    for k in list: 
        if k in pref:
            search.append(k) 
        if len(search) == n: 
            break  
        
        
    
    return search
    




# Script

if __name__ == '__main__':
    # Write script here
    infile = input("Pick the file name containing the full query: ")
    p,q = read_queries(open(infile))
    print()          
    print("Prefix dictionary:\n")
    print(dict_as_str(p))
    print() 
    print("Query dictionary:\n") 
    print(dict_as_str(q)) 
    print() 
    sequence = input("Pick the prefix sequence (or enter done): ")
    while sequence.lower() != 'done':
        m = tuple(sequence.split()) 
        n = top_n(m, 3, p,q) 
        print()
        print("  Top (up to 3) matching full queries in order = ", n)
        sequence = input("Pick the prefix sequence (or enter done): ") 
        print()   
    print()
    fq = input("Pick the full query sequence (or enter done): ") 
    while fq.lower() != 'done': 
        m = tuple(fq.split()) 
        add_query(p, q, m) 
        print()          
        print("Prefix dictionary:\n")
        print(dict_as_str(p))
        print() 
        print("Query dictionary:\n") 
        print(dict_as_str(q)) 
        print() 
        fq = input("Pick the full query sequence (or enter done): ") 
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc5.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
