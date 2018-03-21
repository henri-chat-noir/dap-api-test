def findProbType(paramDims, probDict):
    
    # Create a list of keys sorted in ascending order based on dimSetSize
    # I don't pretend to comprehend this (list comprehension?) code, copied from SO.  However, will understand at some point
    setSizeSort = sorted(probDict.keys(), key=lambda x: probDict[x]['dimSetSize'])
    
    for keyVal in setSizeSort:
        dimSet = probDict[keyVal]['probDims']
        inSet = True
        for probDim in paramDims:
            if probDim not in dimSet:
                inSet = False
                # print(probDim, " not in ", keyVal, ": ", dimSet)
                break
        if inSet:
        # If each probDim within dimSet, then inSet would have survived as True, and must stop checking further keyVals
            break
    if inSet:
        # print("Simplest problem type: ", keyVal)
        problemType = keyVal
    else:
        print("No problem context matches selected dimensions")
        problemType = 'None fit'

    return problemType
