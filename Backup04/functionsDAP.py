import json
import ast

def baseProcess(targetDict, exclUIDs):
    # Main processing of next dictionary
    # Creates baseList and simpList keys on targetDict and returns as outputDict

    outputDict = targetDict
    for entry in outputDict.items():
        
        unitName = entry[0]
        unitInfo = entry[1]
        uID = unitInfo['Uid']
        actionList = True
        
        # If uID excluded, simply move on to next entry in dictionary        
        if uID in exclUIDs:
            breakStop = True
            continue
    
        # print("Now working on . . .:", uID, ". ", unitName)
        # Bucket used where expectation is mutable; defList variable used as non-mutable
        # Initially assigning value defList to tempList ahead of WHILE loop important, as otherwise SIBU-only defLists
        # don't have anything to work from below loop
        defList = unitInfo['defList']
        tempList = defList

        # Attack defList until all arguments have SIBU units returned into baseList
        actionList = not allSIBU(defList)    
    
        while actionList:
            # baseStep defList and assign to tempList for iteration on this loop
        
            baseReturn = baseStep(defList, uID, unitName, targetDict)
            tempList = baseReturn[0]
            baseError = baseReturn[1]
        
            # Partly to prevent endless looping on mal-formed elements,
            # but also just to call it a day if generating errors      
            if baseError == "OK":
                actionList = not allSIBU(tempList)    
            else:
                actionList = False

        # When tempList fully processed place value in as new key into dictionary
        outputDict[unitName]['baseList'] = tempList
        
        # Then create new key that 'combines like terms' within baseList
        tempList = simplify(tempList)
        outputDict[unitName]['simpList'] = tempList

    return outputDict

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
    
    SIBUlist = ('m', 'kg', 's', 'A', 'K', 'mol', 'cd', '1', '#')
    # Note, inclusion of '1' is an artifact of simplified spreadsheet parser, where this is simplest way
    # to handle the definitions where 1 is only value in numerator; generally frequency-related units, e.g. 1/s for Hz
    # This creates a ('1', 1) argument tuple.  This is somewhat distinct by the (1, 1) tuple that relates from a unitary coefficient
    # "#", which is symbol being tested for 'count of number of units' isn't designed as SI, but just to say buying 2 cars, instead of 3
    # The same (as above) will hold for currency symbols when we get to that point
    
    isSIBU = True
    unit_is_number = isinstance(symbol, int) or isinstance(symbol, float)

    if not unit_is_number and symbol not in SIBUlist:
        isSIBU = False
        # print(unit, is_SIBU)

    return isSIBU

def selectSubDict(unitsList, rawDict):

    outputDict = {}
    for rawEntry in rawDict:

        unitName = rawEntry['name']
        if unitName in unitsList:
        
            outputDict[unitName] = rawEntry
            defString = rawEntry['defString']
        
            # JSON structure of defString formatted to 'look' like Python list, but needs to be converted into one
            # and added into dictionary under new 'defList' key
            defList = ast.literal_eval(defString)
            outputDict[unitName]['defList'] = defList

    return outputDict

def buildSOUnames(SOUset, rawDict):
    
    nameList = []
    for unitEntry in rawDict:

        if unitEntry['SOU'] in SOUset:
            nameList.append(unitEntry['name'])

    # Extract SI and metric dictionary entries and build new dictionary, using 'name' of unit entry as key in new dictionary
    
    return nameList

def loadRaw(fileName):
    
    dictPath = "C:\\0_Python\dap-api-test\\"
    
    with open(dictPath + fileName, 'r') as file:      # Open connection to file, read only
        rawDict = json.load(file)
        # rawDict has the structure as list of dictionaries, i.e. each entry is un-keyed and only a member of a list
    
    return rawDict

def printDict(targetDict, exclUIDs):
    # Simple output function for showing dictionary

    for entry in targetDict.items():
        
        unitName = entry[0]
        unitInfo = entry[1]
    
        uID = unitInfo['Uid']
        if uID not in exclUIDs:

            print("Output: ", uID, ". ", unitName, unitInfo['defList'])
            print("baseList: ", unitInfo['baseList'])
            print("simpList: ", unitInfo['simpList'])
            print("------------")