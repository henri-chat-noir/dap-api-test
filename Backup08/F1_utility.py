"""
Holding pen for functions that are not central to processing, e.g. printing
Declutters other modules
"""

def printDict(targetDict, exclUIDs):
    # Simple output function for showing dictionary
    # Provides a 'comment' string next to listing of PathIDs with labels of each unit in path (if any)

    for entry in targetDict.items():
        
        unitID = entry[0]
        unitInfo = entry[1]
    
        unitName = unitInfo['name']
        if unitID not in exclUIDs:

            pathList = unitInfo['pathList']
            if len(pathList) != 0:
                breakStop = True

            print("Output:", unitID, "-", unitName, "defString = ", unitInfo['defString'])
            print("defList: ", unitInfo['defList'])
            print("baseList: ", unitInfo['baseList'])
            print("simpList: ", unitInfo['simpList'])
            print("coefficient: ", unitInfo['coeff'])
            print("symList: ", unitInfo['symList'])
            print("pathList: ", pathList)
            print("------------")
    return

def printBaseUnits(targetDict):

    for entry in targetDict.items():
        
        unitID = entry[0]
        unitInfo = entry[1]
        unitName = unitInfo['name']
        baseUnit = unitInfo['baseUnit']
        if baseUnit:

            print("Output:", unitID, "-", unitName, unitInfo['defList'])
            print("baseList: ", unitInfo['baseList'])
            print("simpList: ", unitInfo['simpList'])
            print("coefficient: ", unitInfo['coeff'])
            print("symList: ", unitInfo['symList'])
            print("pathList: ", unitInfo['pathList'])
            print("------------")
    
    return

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
