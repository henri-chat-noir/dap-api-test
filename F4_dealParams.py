import F0_general as fGen
import random as rand

def dealAnswer(dimDict):

    dims = list(dimDict.keys())
    maxIndex = len(dims) - 1
    dimIndex = rand.randint(0, maxIndex)
    answerDim = dims[dimIndex]
    
    return answerDim

def dealArguments(answerDim, difficulty, dimDict):
    
    # Residual tuples is the current combination of base dimensions and degrees that remain to be 'cancelled out'
    # Initialize the residual tuples list with definition of answer; development list of strings for resid Dims
    residTuples = dimDict[answerDim]['primTuples']
    residBaseDims = [i[0] for i in residTuples]

    # Initialize paraemeter dimension list, which holds dimensions and lambda values for answer plus each argument
    # Load passed answerDim along with its lambda, which is (by definition) = 1
    dimLambdas = []
    dimLambdas.append((answerDim, 1))

    # Set (somewhat arbitrary) maximum limit on iterations of while loop in event residual base dimensions cannot be 'cancelled out'
    maxArgs = 9
    count = 0

    # This first loop simply builds a set of arguments (based on difficulty level) that involve 'some cancelling'
    while len(residTuples) > 0 and count < maxArgs:

        count = count + 1

        # Construct simple list of current dimensions
        dimsList = [i[0] for i in dimLambdas]

        # Could work to conform random and simple functions perhaps by passing a Boolean as to which algorithm should be applied.
        if count <= difficulty:    
            newDim = randomDim(residTuples, dimsList, dimDict)
        else:
            newDim = simpleDim(residTuples, dimsList, dimDict)

        if newDim == 'NoMatch':
        # Exit out of function and essentially retry, as this effort didn't work
            breakStop = True
            dimsList = []
            break
        else:
        # Process new dimension, adding to the related 'primTuples' from dimDict, calculating lambda, figuring out residual base dimensions, etc.
            newTuples = dimDict[newDim]['primTuples']
            argLambda = calcLambda(residTuples, newTuples)
    
            newBaseDims = [i[0] for i in newTuples]
            dimLambdas.append( (newDim, argLambda) )
            # Make a copy of residual tuples into replacement for processing
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
        
    return dimLambdas

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

def randomDim(residualPrimTuples, dimsList, dimDict):

    # First for loop through residual to pick argument to attack time (if an 'issue')
    attackTime = False
    maxDeg = 0
    for primTuple in residualPrimTuples:
        
        if abs(primTuple[1]) > maxDeg:
            maxDeg = abs(primTuple[1])
            maxBaseDim = primTuple[0]
        
        if primTuple[0] == 'TIM' and abs(primTuple[1]) > 1:
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
        entryBaseDims = [i[0] for i in entryDict['primTuples']]
        if nextBaseDim in entryBaseDims and dimLabel not in dimsList:
            nextDims[dimLabel] = entryDict

    keyList = list(nextDims.keys())
    maxIndex = len(keyList) - 1
    dimIndex = rand.randint(0, maxIndex)
    dimension = keyList[dimIndex]
    
    return dimension

def simpleDim(residTuples, dimsList, dimDict):

    simpleDim = 'NoMatch'
    for primDim, degree in residTuples:

        # Should use some dictionary comprehension here, but for now I'll just loop through all dimensions
        # Purpose here is to pick dimensions that have single character of remaining base dimensions
        for entry in dimDict.items():
            newDim = entry[0]
            entryDict = entry[1]
            primTuples = entryDict['primTuples']

            if len(primTuples) == 1 and primTuples[0][0] == primDim and newDim not in dimsList:
                if abs(primTuples[0][1]) == abs(degree):
                    simpleDim = newDim
                    # print("simpleDim: ", simpleDim)
                    return simpleDim
      
    return simpleDim

def selectDims(subject, exclDims, targetDict):
    # Sub-selects dimensions based on subject
    # I'm sure this could be replaced by single dictionary comprehension statement, but for now
    # mechanical build by simple loop
       
    outputDict = {}
    for key, entryInfo in targetDict.items():
        subjectList = entryInfo['subjectList']
        dimension = key
        
        if subject in subjectList and dimension not in exclDims:
            outputDict[dimension] = entryInfo
            
    return outputDict