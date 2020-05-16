def read_graph(fileName)->dict:
    infile = open(fileName, 'r')
    dictGraph = {} 
    line = infile.readlines()
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
    infile.close()
    for i in range(len(listOfFriends)): 
        dictGraph[listOfFriends[i]] = listofFS[i]
    return dictGraph
    
def graph_as_str(dictGraph)->str:
  graphstr=''
  for k,v in dictGraph.items(): 
      graphstr += k + '-->' + str(v)  + '\n'
  return graphstr
      
    
def find_influencers(dictGraph, tp = False)->set: 
    infl_dict = {} 
    infl_set = set()
    for k,v in dictGraph.items(): 
        if len(v)==0: 
            infl_dict[k] = [-1, len(v), k]
        else:  
            infl_dict[k]= [len(v)//2, len(v), k] 
    while bool(infl_dict) != False:
        if tp == True: 
            print("influencer dictionary = ", infl_dict)
        h = min(infl_dict.items(), key=lambda x: x[1][1]) 
        if h[1][0] < 0: 
            infl_set.add(h[0])
            del infl_dict[h[0]]
        else: 
            if tp == True: 
                print("Removing from influencer dictionary = ", h)
            del infl_dict[h[0]]
            for i in range(len(dictGraph[h[0]])): 
                if dictGraph[h[0]][i] in infl_dict: 
                    alpha = dictGraph[h[0]][i]
                    infl_dict[alpha][0] = infl_dict[alpha][0] - 1
                    infl_dict[alpha][1] = infl_dict[alpha][1] - 1
        if tp == True: 
            print("small influencer set= ", infl_set)
    return infl_set            
        
def all_influenced(dictGraph, setNodes={})->set:
    fdict={}
    fset=set()
    if setNodes == {} or setNodes == None: 
        for k in dictGraph: 
            fset.add(k)
        fset = sorted(fset) 
        return fset 
    for i in setNodes: 
        if i not in dictGraph: 
            return 'Not Valid Subset'
    for k in dictGraph:
        if k in setNodes: 
            fdict[k] = True
        else:
            fdict[k]= False
    for k,v in dictGraph.items(): 
        if len(v) == 0: 
            if k in setNodes:
                fdict[k] = True 
        if len(v) == 1: 
            if v[0] in setNodes:
                fdict[k]=True
    for k,v in dictGraph.items():
        count = 0
        for i in range(len(v)):
            if v[i] in setNodes: 
                count += 1 
                if count >= len(v)//2: 
                    fdict[k] = True
    for k in fdict: 
        if fdict[k] == True: 
            fset.add(k) 
    fset = sorted(fset)
    return fset

    

if __name__ == '__main__':
    k = input("Pick the file name with the desired friendship graph: ")
    infl_dict = read_graph(k)
    g = graph_as_str(infl_dict)
    print("Graph: person --> [friends]")
    print(g)
    tp = input("Produce Trace: Yes or No ")
    f ={}
    if tp.lower() == "yes":  
        f = find_influencers(infl_dict, True) 
    elif tp.lower() == "no":
        f = find_influencers(infl_dict)
    print("The influencers are: ", f) 
    j = input("Pick a subset(seperate char by space) or enter 'done': ")
    while j != 'done': 
        if j == '': 
            print(all_influenced(infl_dict))
        else: 
            jline = j.split(" ")
            setj=set()
            for i in range(len(jline)): 
                setj.add(jline[i]) 
            print(all_influenced(infl_dict, setj)) 
        j = input("Pick a subset(seperate char by space) or enter 'done': ")