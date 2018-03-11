def isSIBU(symbol):
    # Function simply test a single unit letter to see if in SIBU list, ignoring integers or floats
    
    SIBUlist = ('kat', '"', 'grad', 'sr', '#', 'm', 'kg', 's', 'A', 'K', 'mol', 'cd')
    
    isSIBU = True
    unit_is_number = isinstance(symbol, int) or isinstance(symbol, float)

    if not unit_is_number and symbol not in SIBUlist:
        isSIBU = False
        # print(unit, is_SIBU)

    return isSIBU


def allSIBU(unitList):
    # This function tests all arguments in a list of 2tuples to see if unit letters are SIBU
    # 2tuple presumed to have structure: symbol, degree

    allSIBU = True
    
    for unitTuple in unitList:

        if len(unitTuple) != 2:
            breakOut = True
  
        symbol = unitTuple[0]
        degree = unitTuple[1]

        if not isSIBU(symbol):
            allSIBU = False
            break

    return allSIBU

def baseStep(unitName, defList, unitsDict):

    # The purpose of this function is to swap-in a single argument (with a non-SIBU unit) with replacement arguments
    # where the degrees in the replacement are affected by the degree of the argument being replaced
    
    if len(defList) == 0:
        breakOut = True

    new_defList = defList
    for argTuple in defList:
        
        # Presumed defList is structured with 2tuples: (symbol, degree)
        if type(argTuple) != tuple:
            breakStop = True

        argSymbol = argTuple[0]
        argDegree = argTuple[1]
                
        if not isSIBU(argSymbol):
            # print(argTuple, " needs to be base-stepped, since it has this symbol:", symbol )
            # print("Current argument list: ", argTuple)
            
            # Start by clearing the offending argument out of argument list and assigning to new variable
            new_defList.remove(argTuple)
            
            # print("This is arg list after argument removed: ", defList)

            # This is key bit.  Replacement argument list is returned by looking through dictionary list to find
            # entry where its 'symbol' matches the symbol from argTuple
            
            matchFound = False
            for entry in unitsDict.items():
                if entry[1]['symbol'] == argSymbol:
                    matchFound = True
                    rep_defList = entry[1]['defList']
                    break
    
            # print("The is replacement arg list from dictionary, i.e. prior to degree adjustment: ", rep_defList)
   
            if type(defList) == None:
                breakOut = True
                     
            if matchFound:
                
                # This for loop builds a set of tuples consistent with rep_defList, but where degrees multiplied by degree
                # from the argument that is being replaced (and already cleared from defList
                for repArg in rep_defList:
                
                    repSymbol = repArg[0]
                    repDegree = argDegree * repArg[1]   
                    repTuple = (repSymbol, repDegree)
                    new_defList.append(repTuple)
            
            else:
                # print(argSymbol, " is a non-SIBU symbol where no match exists within unit entries in passed dictionary")
                # repTuple = ('Match problem', 0)
                #newArgs.append(repTuple)
                break
            
            # Revised defList simply returned with newArgs added
            # (noting non-SIBU 2tuple argument cleared earlier in function)
            if new_defList is None:
                breakOut = True

            # print("This is revised arguments list:", defList)
    
    # print("This is return from baseStep: ", new_defList)

    breakToggle = False
    if new_defList[0] == (1, 1) and len(new_defList) == 1:
        breakToggle = True
        # print(breakToggle)

    baseStep = new_defList

    return baseStep

def simplify(argList):

    unitList = []
    
    for unit, degree in argList:
        if len(unitList) == 0:
            unitList = [unit]
        
        else:
            if unit not in unitList:
                unitList.append(unit)  
    
    simplify = []
    for uniqueUnit in unitList:
        
        combDegree = 0
        for unit, degree in argList:

            if unit == uniqueUnit:
                combDegree = combDegree + degree
            
        simplify.append( (uniqueUnit, combDegree) )

    return simplify