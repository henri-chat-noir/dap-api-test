def printPath(targetDict, printUIDs):
    # Test of dictionary comprehension logic
    # Can I get this to work (even if makes sense to embed answer in the new 2tuple structure)?
    
    for entry in targetDict.items():
            
        unitID = entry[0]
    
        unitInfo = entry[1]
        unitName = unitInfo['name']
    
        pathText = ""
        pathIDs = []
        pathList = unitInfo['pathList']
        
        for pathTuple in pathList:
                pathIDs.append(pathTuple[0])
    
        if unitID in printUIDs:
                        
            pathEntries = {key:value for (key, value) in targetDict.items() if key in pathIDs}
            for pathEntry in pathEntries.values():
                pathID = pathEntry['Uid']
                pathLabel = pathEntry['name']
                pathText = pathText + str(pathID) + ", " + pathLabel

            print("Output:", unitID, "-", unitName, "defString = ", unitInfo['defString'])
            print("defList: ", unitInfo['defList'])
            print("baseList: ", unitInfo['baseList'])
            print("simpList: ", unitInfo['simpList'])
            print("coefficient: ", unitInfo['coeff'])
            print("symList: ", unitInfo['symList'])
            print("pathList: ", pathList)
            print("pathText: ", pathText)
            print("------------")
    
    return