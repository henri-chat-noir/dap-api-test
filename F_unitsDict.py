"""
Main raw units dictionary processing module on initial imported JSON 'raw dictionary'
Sub-dictionary selection
    buildIDs: used to produce list of Uids that are consistent with selected SOU
    extractSubDict:
        sub-selects out of full (raw) 'master dictionary' only those units consistent with SOU selected
        In fact, what we will do going forward is pre-process a dictionary for each SOU, so this is not repeated each time
        However, for now, this helps development by isolating only those units that have been properly established in the raw JSON

[unitProcess] processes targetDict, which modified (and passed back as outputDictionary) with following new keys:
(Note:  those that are asterisked are likely intermediate, but helpful in intermediate understanding and debugging.)

        *'baseList' - This is the first 'expansion' of the original defList back to 2tuples that are base units
        *'combList' - This reprocesses baseList to combine like terms
        'coeff' -   A float calculated by processing all numeric tuples in simpList via requried exponentiation and multiplication
        'symList' - This is the 'remainder' of combList that wasn't formed up into coeff, i.e. the 2tuples of (base) symbols and degrees
        'baseUnit'- A simple Boolean to indicate the particular unit is a base unit (in the given SOU)
        'pathList' -In 'walking back' to the base units, this is the list of intermediate units used to get there
                    Presumed this may be important when providing additional definitional information for problems

which relies on following sub-functions:
    tagBase - makes determination as to whether current 2tuple represents a 'base unit'
    processCoeff - function that evaluates and comes up with 'coeff' float from numeric 2tuples in passed list of (base, degree) 2tuples
    baseStep - the fundamental procedure that takes 'one step closer' to base units by walking through current defList

all in turn supported by simple small logic functions:
    argsDone - have all the arguments been fully processed back to base unit, which is determined simply by evaluating each symbol, per . . .
    symDone - generally if isNumber(symbol) or isBase(symbol) or symbol in stopSym, then symDone = True
    isNumber - is the base of 2tuple numeric? (includes evaluation of '1')
    isBase - is the symbol on list of base symbols, currently just for SI via:
             SIBUlist = ('m', 'kg', 's', 'A', 'K', 'mol', 'cd')

"""
import F_general as fGen
import ast
# import os

def unitProcess(targetDict, exclUIDs):
    # Process targetDict
    # Creates baseList and simpList keys on targetDict and returns as outputDict

    outputDict = targetDict
    for unitName, unitInfo in outputDict.items():
        
        uID = unitInfo['Uid']
        pathList = []
        actionList = True
        
        # If uID excluded, simply move on to next entry in dictionary        
        if uID in exclUIDs:
            breakStop = True
            continue
    
        # tempList is bucket used where expectation is mutable; defList variable used as non-mutable
        # Initially assigning value defList to tempList ahead of WHILE loop important, as otherwise
        # those units that are SIBU-only to begin with don't have anything to work from below loop
        defList = unitInfo['defList']
        tempList = defList[:]

        # Attack defList until all arguments have SIBU units returned into baseList
        actionList = not argsDone(defList)    
    
        while actionList:
            # baseStep defList and assign to tempList for iteration on this loop
        
            baseReturn = baseStep(defList, pathList, uID, unitName, targetDict)
            tempList = baseReturn[0]
            baseError = baseReturn[1]
        
            # Partly to prevent endless looping on mal-formed elements,
            # but also just to call it a day if generating errors      
            if baseError == "OK":
                actionList = not argsDone(tempList)    
            else:
                actionList = False

        # When tempList fully processed place value in as new key into dictionary
        outputDict[unitName]['baseList'] = tempList
        
        # Then create new key that 'combines like terms' within baseList
        tempList = fGen.combineLike(tempList)
        outputDict[unitName]['combList'] = tempList

        # Having creating a series of base-unit related tuples, then matter of extracting coefficients
        # (Note, verbosity here with intermediate variable assignment helpful with de-bugger)
        coeff = processCoeff(tempList)[0]
        symList = processCoeff(tempList)[1]

        outputDict[unitName]['coeff'] = coeff
        outputDict[unitName]['symList'] = symList

        # Set Boolean variable based on coefficient and symList
        outputDict[unitName]['baseUnit'] = tagBase(coeff, symList)

        # Set value of constructed pathList into new key value in outputDict
        outputDict[unitName]['pathList'] = pathList

    return outputDict

def tagBase(coeff, symList):
    # All that's needed is to test the first tuple in list
    # If list has > 1 tuple, then not going to be a base unit anyway

    symbol = symList[0][0]
    degree = symList[0][1]
    
    # Conditions for base unit fairly self explanatory from 4 required conditions
    if len(symList) == 1 and coeff == 1 and isBase(symbol) and degree == 1:
        tagBase = True
    else:
        tagBase = False
        
    return tagBase        

def processCoeff(argList):
    # Function that identifies each numeric tuple in argList, calculates float from values
    # and creates a new def-type list with these elements then removes the numeric tuples in symList version.
    # Are (1, 1) tuples present in any entries other than base units?  Would these just be different names for same unit?

    symList = []
    coeff = 1.0

    for argTuple in argList:

        symbol = argTuple[0]
        degree = argTuple[1]

        if isNumber(symbol):
            if symbol == '1':
                symbol = 1
            coeff = coeff * symbol ** degree

        else:
            symList.append(argTuple)

    return (coeff, symList)

def baseStep(defList, pathList, unitID, unitName, unitsDict):

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
                
        if not symDone(argSymbol):
            
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

                    # Also add the unit ID for the matched unit onto pathList
                    pathList.append(( entry[1]['Uid'], entry[1]['name']))
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

def argsDone(unitList):
    # This function tests all arguments in a list of 2tuples to see if unit letters require further iteration
    # 2tuple presumed to have structure: symbol, degree
    # Returns boolean "argsDone"

    argsDone = True
    
    for unitTuple in unitList:

        if len(unitTuple) != 2:
            # Just an error trap in the event something clearly busted with formation of unitList
            breakStop = True
        # A bit more robust against mal-formed unit list to manual unpack after above test
        symbol = unitTuple[0]
        degree = unitTuple[1]

        if not symDone(symbol):
            argsDone = False
            break

    return argsDone

def symDone(symbol):
    # Function simply test a single unit letter to see if in SIBU list, ignoring integers or floats
    
    stopSym = {'#'}
    # "#", which is symbol being tested for 'count of number of units' isn't designed as SI, but just to say buying 2 cars, instead of 3
    # The same (as above) will hold for currency symbols when we get to that point
    
    if isNumber(symbol) or isBase(symbol) or symbol in stopSym:
        symDone = True
    else:
        symDone = False
        
    return symDone

def isNumber(symbol):

    isNumber = isinstance(symbol, int) or isinstance(symbol, float) or symbol == '1'
    # Note, inclusion of '1' is an artifact of simplified spreadsheet parser, where this is simplest way
    # to handle the definitions where 1 is only value in numerator; generally frequency-related units, e.g. 1/s for Hz
    # This creates a ('1', 1) argument tuple.  This is somewhat distinct by the (1, 1) tuple that relates from a unitary coefficient

    return isNumber

def isBase(symbol):

    SIBUlist = ('m', 'kg', 's', 'A', 'K', 'mol', 'cd')

    if symbol in SIBUlist:
        isBase = True
    else:
        isBase = False

    return isBase

def extractSubDict(selectionList, rawDict):
    # Builds new dictionary based on passed list, using values in list as key in new (nested) dictionary
    # Also creates a 'proper list' from what is string in JSON file via ast.literal_eval function

    outputDict = {}
    for rawEntry in rawDict:

        unitID = rawEntry['Uid']
        if unitID in selectionList:
        
            outputDict[unitID] = rawEntry
            defString = rawEntry['defString']
        
            # JSON structure of defString formatted to 'look' like Python list, but needs to be converted into one
            # and added into dictionary under new 'defList' key
            defList = ast.literal_eval(defString)
            outputDict[unitID]['defList'] = defList

    return outputDict

def buildIDlist(SOUset, rawDict):
    # Function builds a simple list of unit id (keys), i.e. key = Uid, where the system of units (SOU)
    # of the unit is in set passed SOUset

    IDlist = []
    for unitEntry in rawDict:

        if unitEntry['SOU'] in SOUset:
            IDlist.append(unitEntry['Uid'])

    # Extract the unit IDs for all SI and metric dictionary entries in the raw file
    
    return IDlist