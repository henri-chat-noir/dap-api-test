"""
Attempt at carving out some of the 'static' processing from three (3) raw JSON files that provide key data:
    dictDimensions
    dictProblems
    dictObjects
partly for later processing modularity (as this doesn't need to be re-processed on each call) and partly to declutter other module(s)

Of these three primary dictionary, dictObjects is used to support new keys in the other two, by interpreting and expanding
the 'object classes' that were included in them, and returning full lists of 'viable objects' for each
problem type and dimension respectively

"""
import ast
import F0_general as fGen

def buildDimsDict(rawDict, objDict):
    # Processes what is essentially raw, non-nested JSON import and adds keys as noted in module documention
    # Also creates a 'proper list' from what is string in JSON file via ast.literal_eval function

    # First pass simply forms up proper Python data types from imported JSON
    # (For now) these are added on top of a full cloingin of 'rawEntry' for diagnostic and debugging (of data) purposes
    outputDict = {}
    for rawEntry in rawDict:

        # Full clone of raw entry under key name equal to 'dimension' label
        dimension = rawEntry['dimension']
        outputDict[dimension] = rawEntry

        # Initial variable assignments just to assist when using debugger
        subjectString = rawEntry['subjectString']
        primDimsString = rawEntry['primDimString']
        objRaw = rawEntry['objClassString']
        
        # JSON structure for subjectString and baseDims formatted to 'look' like Python list.
        # However, needs to be converted into one with ast.literal_eval
        subjectList = ast.literal_eval(subjectString)
        primTuples = ast.literal_eval(primDimsString)
        rawObjClasses = ast.literal_eval(objRaw)
       
        outputDict[dimension]['subjectList'] = subjectList
        outputDict[dimension]['primTuples'] = primTuples
        outputDict[dimension]['rawObjClasses'] = rawObjClasses

    # Then need to reloop through intermediate dictionary to decode the 'raw' object class list,
    # where there are instances of [keyVal!] pointers to other dimensions
    for keyVal, entryInfo in outputDict.items():
        
        # Initialize by setting expandedObjects to rawObjects
        rawList = list(entryInfo['rawObjClasses'])
        tempList = rawList[:]
        for element in rawList:
            if element[-1] == "!":
                subsetLabel = element[:-1]
                # print("subsetLabel: ", subsetLabel)
                tempList.remove(element)
                subsetList = list(outputDict[subsetLabel]['rawObjClasses'])
                tempList.extend(subsetList)
                # print("Object list: ", tempList)
                
        entryInfo['dimObjClasses'] = tempList

    # Then final loop through to resolve create an actual 'object list' from object classes
    for keyVal, entryInfo in outputDict.items():
        
        dimObjClasses = entryInfo['dimObjClasses']
        objClassList = objDict.keys()
        # print("Possible parameter object classes: ", paramObjectClasses)
        dimObjects = []
        for objClass in dimObjClasses:
            if objClass in objClassList:
                newDimObjects = objDict[objClass]
           
            else:
                if objClass[-1] == "#":
                    newDimObjects = objClass[:-1]
                else:            
                    print("Dimension obj class value not object class and no # suffix")
            
            # Clunky way of handling variability in type determination with append vs. extend, oh well (for now)
            if type(newDimObjects) is str:
                dimObjects.append(newDimObjects)
            else:
                dimObjects.extend(newDimObjects)

            entryInfo['dimObjects'] = dimObjects

    return outputDict

def buildProbDict(JSONfile, objDict):

    # Start simply by creating a nested dictionary from raw JSON file, with probType as key
    # Add proper dictionary structure with/for odPacks, as 'raw' (as not processed for ! and # entries)
    problemRoster = fGen.loadRaw(JSONfile)
    probDict = {}

    for entry in problemRoster:
        keyVal = entry['probType']
        probDict[keyVal] = {}
        
        probDict[keyVal]['probContext'] = entry['probContext']

        odPacksRaw = ast.literal_eval(entry['odPacks'])
        probDict[keyVal]['odPacksRaw'] = odPacksRaw
        
#       entry['probDimTuple'] = ast.literal_eval(entry['dimString'])
#       entry['probObjClassTuples'] = ast.literal_eval(entry['objClassString'])
        
    # Then need to decode the odPacksRaw dictionary, where there are instances of "!" pointers to other keys
    # As well, separate decoding of those elements in objClasses that reference objects themselves
    # (as indicated by # suffix)
    for keyVal, entryInfo in probDict.items():
        
        allObjects = []         # useful to build list of all objects (separately from object-dimension packages)
        allDims = []         # ditto to previous comment
        odPacks = []
        odPacksRaw = entryInfo['odPacksRaw']
        for objRaw, dimRaw in odPacksRaw:
            
            # First iterate through objects list, filtering on # and looking up rest (which are object classes)
            # in objDict, returning full list of all objects
            rawList = objRaw
            tempList = rawList[:]
            for element in rawList:
                if element[-1] == "#":
                    tempList.remove(element)
                    tempList.append(element[:-1])
                else:
                    tempList.remove(element)
                    objList = objDict[element]
                    tempList.extend(objList)
            
            objList = tempList[:]
            allObjects.extend(objList)
            
            # Then iterate through dimensions list, filtering on ! pointers to other keys (for their dim lists)
            # With new doPack structure, which are lists of 2tuples (themselves lists), it's presumed that ! calls can only be to
            # a) odPack[0] (set as fixed constant); and b) that those references themselves do not contain ! elements
            rawList = dimRaw
            tempList = rawList[:]
            for element in rawList:
                if element[-1] == "!":
                    pointerLabel = element[:-1]
                    tempList.remove(element)
                    newDims = probDict[pointerLabel]['odPacksRaw'][0][1]
                    # subsetList = list(probDict[subsetLabel]['probDimTuple'])
                    tempList.extend(newDims)
            
            dimList = tempList[:]
            allDims.extend(dimList)
            
            odPackTuple = (objList, dimList)
            odPacks.append(odPackTuple)

            # Assign constructed tempList into entry odPack
            # and accumulate objects in allObjects list for assignment outside of odPacksRaw loop
            
            # odPacks[keyVar]['dimList'] = tempList
            
        # End of looping through doPackRaw dictionary
        entryInfo['odPacks'] = odPacks

        # With advent of 'packs', opportunity for deliberate duplicates of dimensions and/or objects
        # SO comments that set function de-duplicates, and then can convert that back to list
        entryInfo['allObjects'] = list(set(allObjects))
        entryInfo['allDims'] = list(set(allDims))

        # Create a new entry which is size of full dimSet
        # This is used in (later) processing to select the problem that has the smallest number of dimensions
        # that still 'fits' the 'dealt' parameters.
        entryInfo['dimSetSize'] = len(allDims)

    return probDict

def buildObjDict(JSONfile):
    # Start simply by creating a nested dictionary from raw JSON file with
    # with key = to class of object and value list of objects
    # Also add proper list and/or tuple objects from what would otherwise be simple JSON strings

    objects = fGen.loadRaw(JSONfile)
    objDict = {}
    for entry in objects:
        keyVal = entry['objClass']
        objTuple = ast.literal_eval(entry['objects'])
        objList = list(objTuple)
        objDict[keyVal] = objList
        
    return objDict