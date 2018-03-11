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

def baseStep(defList, unitID, unitName, unitsDict):

    # The purpose of this function is to swap-in a single argument (with a non-SIBU unit) with replacement arguments
    # where the degrees in the replacement are affected by the degree of the argument being replaced
    # Since the overall calling routine is cycling on the dictionary, creating the "baseList", this function
    # is design for essentially a single pass through the argument tuples in defList

    errLabel = "OK"
    if len(defList) == 0 or type(defList) is None:
        errLabel = "Passed defList not proper list"
        breakStop = True

    new_defList = defList
    for argTuple in defList:
        
        # Presumed defList is structured with 2tuples: (symbol, degree)
        if type(argTuple) != tuple:
            errLabel = "Arg in defList not a 2tuple"
            breakStop = True
            
        argSymbol = argTuple[0]
        argDegree = argTuple[1]
                
        if not isSIBU(argSymbol):
            
            # Start by clearing the offending argument out of argument list and assigning to new variable
            new_defList.remove(argTuple)
            
            # This is key bit.  Replacement argument list is returned by looking through dictionary list to find
            # entry where its 'symbol' matches the symbol from argTuple
            
            matchFound = False
            for entry in unitsDict.items():
                # Loop through dictionary to identify the 'root' entry with a symbol (defined for the unit)
                # that matches the symbol in the argument
                # Note as well that an entry 'matching on itself' recursively is problem with dictionary (only allowable for Base Units)
                # Such a case is at least omitted from 'proper' matchFound

                matchName = entry[1]['name']
                if entry[1]['symbol'] == argSymbol and not (unitName == matchName):
                    # When find a match, assign its defList to a replacement def list (as to structure)
                    # i.e. this defList needs to be 'adjusted' consistent with the degree of the original argument
                    
                    matchFound = True
                    rep_defList = entry[1]['defList']
                    break
                     
            if matchFound:
                # This for loop builds a set of tuples consistent with rep_defList, but where degrees multiplied by degree
                # from the argument that is being replaced (and already cleared from defList

                for repArg in rep_defList:
                    repSymbol = repArg[0]
                    repDegree = argDegree * repArg[1]   
                    repTuple = (repSymbol, repDegree)
                    new_defList.append(repTuple)
            
                    # Revised defList simply returned with newArgs added
                    # (noting non-SIBU 2tuple argument was 'cleared out' earlier in function)

            else: # If no match found
                # Best course is to simply replace argTuple back into string (order will be changed, though) and move on/out
                new_defList.append(argTuple)
                errLabel = "No entry match found for an arg\'s symbol in dictionary"       
                breakStop = True         
                break
            
            
            if new_defList is None:
                errLabel = "Replacement defList is NoneType"
                breakStop = True

    return (new_defList, errLabel)

def allSIBU(unitList):
    # This function tests all arguments in a list of 2tuples to see if unit letters are SIBU
    # 2tuple presumed to have structure: symbol, degree

    allSIBU = True
    
    for unitTuple in unitList:

        if len(unitTuple) != 2:
            breakStop = True
  
        symbol = unitTuple[0]
        degree = unitTuple[1]

        if not isSIBU(symbol):
            allSIBU = False
            break

    return allSIBU

def isSIBU(symbol):
    # Function simply test a single unit letter to see if in SIBU list, ignoring integers or floats
    
    SIBUlist = ('kat', '"', 'grad', 'sr', '#', 'm', 'kg', 's', 'A', 'K', 'mol', 'cd')
    
    isSIBU = True
    unit_is_number = isinstance(symbol, int) or isinstance(symbol, float)

    if not unit_is_number and symbol not in SIBUlist:
        isSIBU = False
        # print(unit, is_SIBU)

    return isSIBU
