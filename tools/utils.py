"""
UTILITIES
"""
def distinct(inlist):
    """
    returns a list of distinct values
    (no duplicated values)
    """
    outlist = []
    for elem in inlist:
        if not elem in outlist:
            outlist.append(elem)
    return outlist

def list_evolution(list1,list2):
    """
    returns the index evolution of each element 
    of the list 1 compared to the index within list 2
    NB: if lists length do not match, place None value at missing index    
    """
#    return [list2.index(x) - list1.index(x) for x in list1 if x in list2]
    evo = []
    for x in list1:
        if x in list2:
            evo.append(list2.index(x) - list1.index(x))
        else:
            evo.append(None)
    return evo

def list_to_dict(keyslist,valueslist):
    """
    convert lists of keys and values to a dict
    """
    if len(keyslist) != len(valueslist):
        return {}  

    mydict = {}
    for idx in range(0,len(keyslist)):
        mydict[keyslist[idx]] = valueslist[idx]
    return mydict

#evo_progress: return the evolution of each item of a list compared to its left value
evo_progress = lambda pos: [] if pos == [] else [j for i in [[0],[pos[i-1]-pos[i] for i in range(1,len(pos))]] for j in i]

if __name__ == '__main__':
    mylist = ['A','B','A','C','A','A','D']
    print('ORIGINAL:', mylist)
    print('DISTINCT', distinct(mylist))
    
    mylist1 = ['A','B','C','D']
    mylist2 = ['A','D','B','C']
    print(list_evolution(mylist2,mylist1))
    
    print(list_to_dict(['a','b','c'], [1,2,3]))

    print(evo_progress([]))
    print(evo_progress([1]))
    print(evo_progress([1,4,2,4,8,5,5,3]))