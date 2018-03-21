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
import F_general as fGen

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
                newDimObjects = objDict[objClass]['objList']
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

    # Start simply by creating a nested dictionary from raw JSON file
    # Also add proper list and/or tuple objects from what would otherwise be simple JSON strings
    
    problemTypes = fGen.loadRaw(JSONfile)
    probDict = {}
    for entry in problemTypes:
        keyVal = entry['probType']
        probDict[keyVal] = entry
        entry['probDimTuple'] = ast.literal_eval(entry['dimString'])
        entry['probObjClassTuples'] = ast.literal_eval(entry['objClassString'])
        
    # Then need to decode the rawDims list, where there are instances of [keyVal!] pointers to other sets
    # As well, separate decoding of those elements in objClasses that reference objects themselves
    # (as indicated by # suffix)
    for keyVal, entryInfo in probDict.items():
        
        rawList = list(entryInfo['probDimTuple'])
        tempList = rawList[:]
        for element in rawList:
            if element[-1] == "!":
                subsetLabel = element[:-1]
                tempList.remove(element)
                subsetList = list(probDict[subsetLabel]['probDimTuple'])
                tempList.extend(subsetList)
                
        entryInfo['probDims'] = tempList
        # Create a new entry which is size of full dimSet
        # This is used in (later) processing to select the problem that has the smallest number of dimensions
        # that still 'fits' the 'dealt' parameters.
        probDict[keyVal]['dimSetSize'] = len(tempList)
    
        rawList = entryInfo['probObjClassTuples']
        tempList = list(rawList[:])
        for element in rawList:
            if element[-1] == "#":
                tempList.remove(element)
                tempList.append(element[:-1])
            else:
                tempList.remove(element)
                objectList = list(objDict[element]['objList'])
                tempList.extend(objectList)
                
        entryInfo['probObjects'] = tempList
        
    return probDict

def buildObjDict(JSONfile):
    # Start simply by creating a nested dictionary from raw JSON file with
    # with key = to class of object and value list of objects
    # Also add proper list and/or tuple objects from what would otherwise be simple JSON strings

    objects = fGen.loadRaw(JSONfile)
    objDict = {}
    for entry in objects:
        keyVar = entry['objClass']
        objDict[keyVar] = entry
        entry['objList'] = ast.literal_eval(entry['objects'])
        
    return objDict