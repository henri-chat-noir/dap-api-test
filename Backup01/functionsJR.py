def testFunction():
    print('This import worked')

    nothing = ' '
    return nothing


def isSIBU(unit):
    # Function simply test a single unit letter to see if in SIBU list, ignoring integers or floats
    
    SIBUlist = ('m', 'kg', 's', 'A', 'K', 'mol', 'cd')
    
    isSIBU = True
    unit_is_number = isinstance(unit, int) or isinstance(unit, float)

    if not unit_is_number and unit not in SIBUlist:
        isSIBU = False
        # print(unit, is_SIBU)

    return isSIBU


def allSIBU(unitList):
    # This function tests all arguments in a list to see if unit letters are SIBU

    SIBUlist = ('m', 'kg', 's', 'A', 'K', 'mol', 'cd')
    
    allSIBU = True

    for unit, degree in unitList:

        unit_is_number = isinstance(unit, int) or isinstance(unit, float)

        if not unit_is_number and unit not in SIBUlist:
            allSIBU = False
            # print(unit, allSIBU)

    return allSIBU

def base_step(defList, units_dict):

    # The purpose of this function is to swap-in a single argument (with a non-SIBU unit) with replacement arguments
    # where the degrees in the replacement are affected by the degree of the argument being replaced
    
    base_step = defList

    for argTuple in defList:

        symbol = argTuple[0]
        degree = argTuple[1]
        
        if not isSIBU(symbol):
                       
            # print(argTuple, " needs to be base-stepped, since it has this symbol:", symbol )
            # print("Current argument list: ", argTuple)
            
            # Start by clearing the offending argument out of argument list
            defList.remove(argTuple)
            # print("This is arg list after argument removed: ", defList)

            # This is key bit.  Replacement argument list is returned by looking through dictionary list to find
            # entry where 'symbol' matches the symbol from argTuple
            
            i = 0
            rep_defList = [('No match', 0)]
            maxIndex = len(units_dict)
            while i < maxIndex and units_dict[i]['symbol'] != symbol:
                
                # print("index = ", i, units_dict[i]['symbol'])
                i = i + 1
            
            if i == maxIndex:
                rep_defList = [('No match', 0)]
            
            else:
                rep_defList = units_dict[i]['defList']
            
            # print("The is replacement arg list from dictionary, i.e. prior to degree adjustment: ", rep_defList)
            
            # This for loop builds a set of tuples consistent with rep_defList, but where degrees multiplied by degree
            # from the argument that is being replaced (and already cleared from defList
            newArgs = []
            for repArg in rep_defList:
                
                repSymbol = repArg[0]
                repDegree = degree * repArg[1]   
                repTuple = (repSymbol, repDegree)
                newArgs.append(repTuple)

            # On this side of else, i.e. when non SIBU, defList simply returned with newArgs added
            # (noting argument cleared earlier in function)
            defList = defList + newArgs
            # print("This is revised arguments list:", defList)
           
        base_step = defList

    return base_step

def simplify(arg_list):

    unit_list = []
    
    for unit, degree in arg_list:

        if unit not in unit_list:
            unit_list.append(unit)  
    
    simplify = []
    for unique_unit in unit_list:
        
        comb_degree = 0
        for unit, degree in arg_list:

            if unit == unique_unit:
                comb_degree = comb_degree + degree
            
        simplify.append( (unique_unit, comb_degree) )

    return simplify