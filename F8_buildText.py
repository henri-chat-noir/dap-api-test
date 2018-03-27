"""
Last mile -- building text that will feed JSON return

"""
import F3_buildDicts as fBuild
import re

def  buildTitle(probType, paramObjList, probDict):
    
    titleTemplate = probDict[probType]['title']
    # print("Template: ", conTemplate)
    titleLower = swapObjects(titleTemplate, paramObjList, True)
    title = titleLower

    return title

def  buildContext(probType, paramObjList, probDict):
    
    preamble = "You need to run some calculations related to"
    conTemplate = probDict[probType]['probContext']
    # print("Template: ", conTemplate)
    context = preamble + " " + swapObjects(conTemplate, paramObjList, False)

    return context

def swapObjects(inputString, paramObjList, firstCap):

    # First, build simple list of objects connected with problem from paramObjList tuple
    # Note effort to create unique list may not strictly be required for following operations, but good practice
    probObjList = []
    for paramTuple in paramObjList:
        probObj = paramTuple[2]
        if probObj not in probObjList:
            probObjList.append(probObj)

    # Look through object dictionary and create list of 2tuples that can relate an object class to object
    objDict = fBuild.buildObjDict('dictObjects12.json')
    probClassObjList = []
    for probObj in probObjList:

        for objClass, objTuple in objDict.items():
            objList = objTuple[0]
            if probObj in objList:
                classObjTuple = (objClass, probObj)
                probClassObjList.append(classObjTuple)

    # print("objClass, object 2tuple list: ", probClassObjList)

    # Replaced bracketed class indicators with object consistent with those dealt for problem
    # Presumes that there is only a single object specified in any given object class (for now)
    bracketSearch = re.compile(r'<.+?>')
    outputString = inputString[:]
    bracketElements = re.findall(bracketSearch, outputString)
    
    # Top/outside loop is to run through the 'bracketed strings'
    for bElement in bracketElements:
        
        bElementMatch = False
        parseString = bElement[1:-1].split(", ")

        # Loop through each element with brackets to see if can get a match
        for parseObjClass in parseString:
            # print("Object class: ", objClass)
            for probObjClass, probObj in probClassObjList:
                if firstCap:
                    repWord = probObj[0].upper() + probObj[1:]
                else:
                    repWord = probObj
                if parseObjClass == probObjClass:
                    outputString = outputString.replace(bElement, repWord)
                    bElementMatch = True
        
        # If run through each element within brackets with no match to problem objects,
        # then swap in with defObj assigned to last parsObjClass tested
        if not bElementMatch:
            defObj = objDict[parseObjClass][1]
            if firstCap:
                repWord = defObj[0].upper() + defObj[1:]
            else:
                repWord = defObj
            outputString = outputString.replace(bElement, repWord)
    

    # If somehow NONE of all that 'works', then at least re-form original template string with a message
    if outputString == '':
        outputString = inputString + " (no substitutions matched)"

    return outputString

def buildQuery(ansTuple):

    queryText = "What is the " + ansTuple[0] + " " + dimPrep(ansTuple[0]) + " " + ansTuple[2] + "?"

    return queryText

def buildAss(argTuple):

    count = 0
    assList = []
    assList.append(". . . if you are given the following assumptions:" + "\n")
    for dim, deg, obj, units, value in argTuple:
        count = count + 1
        valString = str(round(value, 2))
        coreText = dim[0].upper() + dim[1:] + " " + dimPrep(dim) + " " + obj + " = " + valString + " " + units
        assList.append(coreText)

    return assList

def dimPrep(dim):
    # Sets preposition appled for objects based on dimension, e.g. "energy output of" [object], rather than simply "of"

    if dim in ['energy', 'power']:
        preposition = "output of"

    elif dim in ['force', 'pressure']:
        preposition = "applied by"

    else:
        preposition = "of"
        
    return preposition

def buidDefHelp(DLOUVlist, metricDict):

    defText = []
    symList = []
    defText.append("You may find the following unit conversions useful:")
    
    for dim, paramLamba, object, unit, value in DLOUVlist:

        defList = metricDict[unit]['defList']
        symbol = metricDict[unit]['symbol']
        if symbol not in symList:
            symList.append(symbol)

        newText = "1 " + symbol + " = "  + metricDict[unit]['defText']
        defText.append(newText)

        pathList = metricDict[unit]['pathList']
        for uID, unitName in pathList:

            # print("Pathlist: ", pathList)
            symbol = metricDict[unitName]['symbol']
            if symbol not in symList:
                symList.append(symbol)

            newText = metricDict[unitName]['defText']
            defText.append("1 " + symbol + " = " + newText)

    return (defText, symList)

def buidSymHelp(symList, symDict):

    symHelp = []
    symHelp.append(". . . where each of the symbols indicate:")

    for paramSym in symList:

        for keyVal, entry in symDict.items():
            if paramSym in entry['symTup']:
                if paramSym != entry['unitName']:
                    symHelp.append(paramSym + " = " + entry['unitName'])
                break
        
    return symHelp

def buildInstruction(ansPack):
    
    if ansPack[2] == 'regular':
        instruction = "Enter your answer in " + ansPack[1] + " to 3 sig figures"
    else:
        instruction = "Enter your answer in " + ansPack[1] + " to 3 sig figures in scientic notation"
    
    return instruction