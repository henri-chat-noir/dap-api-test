def findProbType(paramDims, probDict):
    
    # Create a list of keys sorted in ascending order based on dimSetSize
    # I don't pretend to comprehend this (list comprehension?) code, copied from SO.  However, will understand at some point
    setSizeSort = sorted(probDict.keys(), key=lambda x: probDict[x]['dimSetSize'])
    processMessage = ''
    for keyVal in setSizeSort:
        # For problem selection, the pairing of objects with dims not important
        # So allDims entry is easiest to use
        dimSet = probDict[keyVal]['allDims']
        inSet = True
        for probDim in paramDims:
            if probDim not in dimSet:
                inSet = False
                # print(probDim, " not in ", keyVal, ": ", dimSet)
                processMessage = processMessage + "\n" + probDim + " not in " + keyVal + ": " + str(dimSet)
                break
        if inSet:
        # If each probDim within dimSet, then inSet would have survived as True, and must stop checking further keyVals
            break
    if inSet:
        print("Simplest problem type: ", keyVal)
        problemType = keyVal
    else:
        print("No problem context matches selected dimensions, as per following:")
        print(processMessage)
        problemType = 'None fit'

    return problemType
