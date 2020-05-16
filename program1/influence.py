import prompt
from goody       import safe_open
from math        import ceil 
from collections import defaultdict


def read_graph(open_file : open) -> {str:{str}}:
    dictGraph = {} 
    line = open_file.readlines()
    listOfFriends=[]
    for i in range(len(line)): 
        if ';' in line[i]:
            friends=line[i].split(';')
            if friends[0] not in listOfFriends: 
                listOfFriends.append(friends[0])
            elif friends[1] not in listOfFriends: 
                listOfFriends.append(friends[1].strip('\n')) 
        else:
            listOfFriends.append(line[i]) 
    listOfFriends.sort()
    listOfShips=[] 
    for i in range(len(line)): 
        if ';' in line[i]: 
            listOfShips.append(line[i].split(';')) 
            listOfShips[i][1] = listOfShips[i][1].strip('\n')
    listofFS=[]
    for i in range(len(listOfFriends)):
        minilist=[] 
        for j in range(len(listOfShips)):
            for k in range(len(listOfShips[j])):
                if listOfFriends[i] in listOfShips[j]:
                    if listOfFriends[i] != listOfShips[j][k]:
                        minilist.append(listOfShips[j][k]) 
        minilist.sort()
        listofFS.append(minilist)           
    open_file.close()
    for i in range(len(listOfFriends)): 
        dictGraph[listOfFriends[i]] = set(listofFS[i])
    open_file.close()
    return dictGraph



def graph_as_str(graph : {str:{str}}) -> str:
    graphstr=''
    newDict = {}
    real = sorted(graph)
    for i in range(len(real)):
        newDict[real[i]]= graph[real[i]] 
    for k,v in newDict.items():
        string=''
        string += str(list(sorted(v)))
        graphstr += "  "+ k + ' -> '+ string+ '\n'
    return graphstr


def find_influencers(graph : {str:{str}}, trace = False) -> {str}:
    infl_dict = {} 
    infl_set = []
    for k,v in graph.items(): 
        friends = len(v)
        if friends == 0: 
            infl_dict[k] = [-1, friends, k]
            infl_set.append((-1, friends, k))
        else:  
            infl_dict[k]= [friends-(ceil(friends/2)), len(v), k] 
            infl_set.append((friends-(ceil(friends/2)), len(v), k)) 
                   
    for l in range(len(graph)):
        h = min(infl_set) 
        if h[0] < 0: 
            infl_set.remove(h) 
        else: 
            if trace == True: 
                print("influencer dictionary = ", infl_dict)
                print("Removal dictionary = ", infl_set)
            
                 
            if trace == True: 
                print("Removing from influencer dictionary = ", h)
            infl_set.remove(h) 
            del infl_dict[h[2]]
            min_friends = list(graph[h[2]])
            for i in range(len(min_friends)): 
                if min_friends[i] in infl_dict: 
                    alpha = min_friends[i]
                    infl_dict[alpha][0] -= 1
                    infl_dict[alpha][1] -= 1
                    for j in range(len(infl_set)): 
                            
                        if alpha == infl_set[j][2]: 
                            infl_set[j] = (int(infl_set[j][0])-1, int(infl_set[j][1])-1, alpha)
                                 
                        
    #finally: 
        if trace == True: 
            print("small influencer set= ", infl_dict)
    for key in infl_dict: 
        infl_set.append(key)
    return set(infl_set)       

def all_influenced(graph : {str:{str}}, influencers : {str}) -> {str}:
    fset = set()
    fdict = {}
    
    for s in influencers:   #Checks for nonvalid chars
        if s not in graph: 
            return 'Not Valid Subset'
        
    for k,v in graph.items():         #Checks who has a fr in set 
        fdict[k] = False
        if len(v) == 0 and fdict[k] in influencers: 
            fdict[k] = True
        if len(v) == 1: 
            if list(v)[0] in influencers: 
                fdict[k] = True
        if k in influencers: 
            fdict[k] = True
            
    if len(list(influencers))==0: #Checks if empty 
        for k in graph: 
            fset.add(k)
        return fset 
    
    fdict_copy = fdict
    fdict_copy2 = {} 
    while fdict_copy != fdict_copy2:  
        fdict_copy2 = fdict.copy()
        for k,v in graph.items():
            count = 0  
            for i in range(len(v)): 
                if list(v)[i] in influencers:       #list(v) = friends
                    count += 1 
                    if count >= ceil(len(v)/2): 
                        fdict[k] = True 
                        influencers.add(k)
                        fdict_copy = fdict 
    for k in fdict:
        if fdict[k] == True: 
            fset.add(k) 
    return fset 
        
       
            
    
if __name__ == '__main__':
    # Write script here    
    k = input("Pick the file name with the desired friendship graph: ")
    infl_dict = read_graph(open(k))
    g = graph_as_str(infl_dict)
    print("Graph: person --> [friends]")
    print(g)
    
    tp = input("Produce Trace of Algorithm[True]: ")
    f ={}
    if tp.lower() == "true":  
        f = find_influencers(infl_dict, True) 
    elif tp.lower() == "false" or "":
        f = find_influencers(infl_dict)
        
    print("The influencers are ", f) 
    j = input("Pick any subset (or enter done): "  )
    while j != 'done': 
        if j == '': 
            setj ={}
            print("Friends influenced by subset (100.0% of graph) = ", all_influenced(infl_dict,setj))

        else:
            
            jline = list(j)
            setj =set()
            for i in range(len(jline)):
                if jline[i].isalpha() == True: 
                    setj.add(jline[i])
            if all_influenced(infl_dict, setj) == 'Not Valid Subset': 
                print('Entry Error: '+ str(j) +';' )
                print('Please enter a legal String') 
            else:   
                print("Friends influenced by subset (" + str(float(len(setj)/len(infl_dict))*100)+ "%  of graph) = ", all_influenced(infl_dict, setj)) 
        j = input("Pick any subset (or enter done): "  )
    
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc1.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
    