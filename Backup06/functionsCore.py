import random as rand
import ast
import os

os.chdir("C:\\0_Python\dap-api-test\\")
print(os.getcwd())
import functionsGen as fGen

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
    while len(residTuples) > 0 and count < maxArgs:

        count = count + 1

        # Add new dimension to parameter list        
        newDim = nextDim(residTuples, paramList, dimDict)

        newTuples = dimDict[newDim]['baseTuples']
        argLambda = calcLambda(residTuples, newTuples)
    
        newBaseDims = [i[0] for i in newTuples]
        paramList.append( (newDim, argLambda) )
        # Make a shallow? copy of residual tuples into replacement for processing
        repTuples = residTuples[:]

        for baseDim, degree in newTuples:
            repTuple = (baseDim, -1 * argLambda * degree)
            repTuples.append(repTuple)
        
        # This function 'simplify' essentially combines like terms only (doesn't remove zero degree terms)
        repTuples = fGen.simplify(repTuples)

        # Therefore, only retain those tuples with degree <> 0 (figure out why mod to simplify function can't handle this)
        residTuples = []
        for tuple in repTuples:
            if tuple[1] != 0:
                residTuples.append(tuple)
        
        print('paramList:', paramList)
        print("residTuples: ", residTuples)
        print("----------")
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

def nextDim(residualBaseTuples, paramList, dimDict):

    paramDims = [i[0] for i in paramList]

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
    exclDims = ['acceleration', 'action', 'dynamic viscosity', 'kinematic viscosity', 'surface tension', 'torque']    
    dimsDict = selectDims(subject, exclDims, rawDims)
    
    return dimsDict


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