import random as rand
import ast
import functionsGen as fGen

def findProbType(paramDims, probDict):
    
    # Create a list of keys sorted in ascending order based on dimSetSize
    # I don't pretend to comprehend this (list comprehension?) code, copied from SO.  However, will understand at some point
    setSizeSort = sorted(probDict.keys(), key=lambda x: probDict[x]['dimSetSize'])
    
    for keyVal in setSizeSort:
        dimSet = probDict[keyVal]['expandedDims']
        inSet = True
        for probDim in paramDims:
            if probDim not in dimSet:
                inSet = False
                print(probDim, " not in ", keyVal, ": ", dimSet)
                break
        if inSet:
        # If each probDim within dimSet, then inSet would have survived as True, and must stop checking further keyVals
            break
    if inSet:
        print("Simplest problem type: ", keyVal)
        problemType = keyVal
    else:
        print("No problem context matches selected dimensions")
        problemType = 'None fit'

    return problemType

def createProbDict(JSONfile):

    # Start simply by creating a nested dictionary from raw JSON file
    # Also add proper list and/or tuple objects from what would otherwise be simple JSON strings
    problemTypes = fGen.loadRaw(JSONfile)
    probDict = {}
    for entry in problemTypes:
        keyVal = entry['probType']
        probDict[keyVal] = entry
        entry['rawDims'] = ast.literal_eval(entry['dimensionSet'])
        entry['objTuples'] = ast.literal_eval(entry['objectSet'])
        
    # Then need to decode the rawDims list, where there are instances of [keyVal!] pointers to other sets
    for keyVal, entryInfo in probDict.items():
        
        # Initialize by setting expandedDims to rawDims
        rawList = list(entryInfo['rawDims'])
        tempList = rawList[:]
        for element in rawList:
            if element[-1] == "!":
                subsetLabel = element[:-1]
                tempList.remove(element)
                subsetList = list(probDict[subsetLabel]['rawDims'])
                tempList.extend(subsetList)
                
        entryInfo['expandedDims'] = tempList
        # Create a new entry which is size of full dimSet, which is used in sorting (to select minimal set that 'fits')
        probDict[keyVal]['dimSetSize'] = len(tempList)
    
    return probDict

def selectParameters(answerDim, difficulty, dimDict):
    
    # Initialize the residual tuples list with definition of answer; development list of strings for resid Dims
    residTuples = dimDict[answerDim]['baseTuples']
    residBaseDims = [i[0] for i in residTuples]

    # Initialize paraemeter list, which holds dimensions and lambda values for answer plus each argument
    paramList = []
    paramList.append((answerDim, 1))

    # Set maximum limit on iterations of while loop in event residual base dimensions not 'cancelled out'
    maxArgs = 9
    count = 0
    # This first loop simply builds a set of arguments (based on difficulty level) that involve 'some cancelling'
    while len(residTuples) > 0 and count < maxArgs:

        count = count + 1

        # Add new dimension to parameter list
        paramDims = [i[0] for i in paramList]
        if count <= difficulty:    
            newDim = randomDim(residTuples, paramDims, dimDict)
        else:
            newDim = simpleDim(residTuples, paramDims, dimDict)
        if newDim == 'NoMatch':
        # Exit out of function and essentially retry, as this effort didn't work
            breakStop = True
            paramList = []
            break
        else:
        # Process new dimension, adding to paramList, calculating lambda, figuring out residual base dimensions, etc.
            newTuples = dimDict[newDim]['baseTuples']
            argLambda = calcLambda(residTuples, newTuples)
    
            newBaseDims = [i[0] for i in newTuples]
            paramList.append( (newDim, argLambda) )
            # Make a shallow? copy of residual tuples into replacement for processing
            repTuples = residTuples[:]

            for baseDim, degree in newTuples:
                repTuple = (baseDim, -1 * argLambda * degree)
                repTuples.append(repTuple)
        
            # This function combines like terms only (doesn't remove zero degree terms)
            # Figure out why mod to simplify function can't handle 'dropping' deg zero terms; something to do with operation of tagBase
            repTuples = fGen.combineLike(repTuples)

            # Therefore, only retain those tuples with degree <> 0
            residTuples = []
            for tuple in repTuples:
                if tuple[1] != 0:
                    residTuples.append(tuple)
        
            paramDims = [i[0] for i in paramList]
            # print('paramList:', paramList)
            # print("residTuples: ", residTuples)
            # print("----------")
    
    return paramList

def calcLambda(residTuples, newTuples):
    
    # Loop through both tuples list and take action when dimensions match
    # If dimension in question is time, then it over-rides treatment
    # Even if higher-degreed dimensions may exist

    attackTime = False
    maxDeg = 0
    for residTup in residTuples:
        for newTup in newTuples:
            if residTup[0] == newTup[0]:
                if residTup[0] == 'TIM':
                    targBaseDim = residTup[0]
                    residDeg = residTup[1]
                    newDeg = newTup[1]
                    attackTime = True
                else:
                    if abs(residTup[1]) > maxDeg and not attackTime:
                        targBaseDim = residTup[0]
                        residDeg = residTup[1]
                        newDeg = newTup[1]
   
    # Remember if lambda = 1 (on lhs of equation) it will be 'flipped' when solving/cancelling answer dimensions
    # Hence -1 here on the 'pos' form of lambda is intentional
    lambdaPos = residDeg + -1 * newDeg
    lamdaNeg = residDeg + newDeg
    
    # Set lambda value to whichever form reduces the return degree more
    if abs(lambdaPos) < abs(lamdaNeg):
        argLambda = 1
    else:
        argLambda = -1

    return argLambda

def randomDim(residualBaseTuples, paramDims, dimDict):

    # First for loop through residual to pick argument to attack time (if an 'issue')
    attackTime = False
    maxDeg = 0
    for baseTuple in residualBaseTuples:
        
        if abs(baseTuple[1]) > maxDeg:
            maxDeg = abs(baseTuple[1])
            maxBaseDim = baseTuple[0]
        
        if baseTuple[0] == 'TIM' and abs(baseTuple[1]) > 1:
            attackTime = True
        
    if attackTime:
        nextBaseDim = 'TIM'
    else:
        nextBaseDim = maxBaseDim

    # Build dictionary of candidate dimensions based on whether have nextBaseDim as part of def
    nextDims = {}
    for entry in dimDict.items():
        entryDict = entry[1]
        dimLabel = entryDict['dimension']
        entryBaseDims = [i[0] for i in entryDict['baseTuples']]
        if nextBaseDim in entryBaseDims and dimLabel not in paramDims:
            nextDims[dimLabel] = entryDict

    keyList = list(nextDims.keys())
    maxIndex = len(keyList) - 1
    nextIndex = rand.randint(0, maxIndex)
    dimension = keyList[nextIndex]
    
    return dimension

def buildDims(subject, SOU, rawFile):

    rawDims = fGen.loadRaw(rawFile)
    exclDims = ['acceleration', 'action', 'dynamic viscosity', 'energy density', 'frequency', 'kinematic viscosity', 'surface tension', 'torque']    
    dimsDict = selectDims(subject, exclDims, rawDims)
    
    return dimsDict

def simpleDim(residTuples, paramDims, dimDict):

    simpleDim = 'NoMatch'
    for baseDim, degree in residTuples:

        # Should use some dictionary comprehension here, but for now I'll just loop through all dimensions
        # Purpose here is to pick dimensions that have single character of remaining base dimensions
      
        for entry in dimDict.items():
            newDim = entry[0]
            entryDict = entry[1]
            baseTuples = entryDict['baseTuples']

            if len(baseTuples) == 1 and baseTuples[0][0] == baseDim and newDim not in paramDims:
                if abs(baseTuples[0][1]) == abs(degree):
                    simpleDim = newDim
                    # print("simpleDim: ", simpleDim)
                    return simpleDim
      
    return simpleDim

def selectDims(subject, exclDims, rawDict):
    # Builds new dictionary based on subject
    # Also creates a 'proper list' from what is string in JSON file via ast.literal_eval function

    outputDict = {}
    for rawEntry in rawDict:

        dimension = rawEntry['dimension']
        
        # JSON structure for subjectString and baseDims formatted to 'look' like Python list,
        # but needs to be converted into one with ast.literal_eval
        subjectString = rawEntry['subjectString']
        baseDimsString = rawEntry['baseDims']

        subjectList = ast.literal_eval(subjectString)
        baseTuples = ast.literal_eval(baseDimsString)
 #       baseDims = []
        if subject in subjectList and dimension not in exclDims:
        
            outputDict[dimension] = rawEntry
            outputDict[dimension]['subjectList'] = subjectList
            outputDict[dimension]['baseTuples'] = baseTuples
#            for baseTuple in baseDimTuples:
#                baseDims.append(baseTuple[0])
            
    return outputDict

def printDims(targetDict, exclDims):
    # Simple output function for showing dictionary
    # Provides a 'comment' string next to listing of PathIDs with labels of each unit in path (if any)

    for entry in targetDict.items():
        
        dimension = entry[0]
        dimInfo = entry[1]
        
        if dimension not in exclDims:

            print("dimension:", dimension)
            print("subjectList: ", dimInfo['subjectList'])
            print("baseTuples: ", dimInfo['baseTuples'])
            print("------------")
    return