"""
Last mile -- building text that will feed JSON return

"""
import F3_buildDicts as fBuild
import re

def  buildContext(probType, paramObjList, probDict):
    
    preamble = "You need to run some calculations related to"
    conTemplate = probDict[probType]['probContext']
    # print("Template: ", conTemplate)
    context = preamble + " " + swapObjects(conTemplate, paramObjList)

    return context

def swapObjects(inputString, paramObjList):

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

    print("objClass, object 2tuple list: ", probClassObjList)

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
                if parseObjClass == probObjClass:
                    outputString = outputString.replace(bElement, probObj)
                    bElementMatch = True
        
        # If run through each element within brackets with no match to problem objects,
        # then swap in with defObj assigned to last parsObjClass tested
        if not bElementMatch:
            defObj = objDict[parseObjClass][1]
            outputString = outputString.replace(bElement, defObj)
    

    # If somehow NONE of all that 'works', then at least re-form original template string with a message
    if outputString == '':
        outputString = inputString + " (no substitutions matched)"

    return outputString

def findObject(objClass, objList):

    pass

    return

def buildQuery(ansTuple):

    queryText = "What is the " + ansTuple[0] + " " + dimPrep(ansTuple[0]) + " " + ansTuple[2] + "?"

    return queryText

def buildAss(argTuple):

    count = 0
    assList = []
    assList.append(". . . if you are given the following assumptions:" + "\n")
    for dim, deg, obj in argTuple:
        count = count + 1
        value = "[value]"
        units = "[units]"
        coreText = dim[0].upper() + dim[1:] + " " + dimPrep(dim) + " " + obj + " = " + value + " " + units
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

def buildEchoback(subject, sou, difficulty, title, context, queryText, assList):

    answerVal = 42
    answerUnits = "kg-m/s2"
    instruction = "Please enter in Light-years per hour..."
    difString = {
        1 : "Simple",
        2 : "Fairly Easy",
        3 : "Challenging",
        4 : "Very Hard",
        5 : "Brutal"
    }

    echoback = {
        'subject' : "A problem related to: " + subject + ".",
        'sou' : "The system of units are: "+sou +".",
        'difficulty' : "The difficulty level is: " + difString[difficulty] + ".",
        'title' : title + " (" + sou + " units)",
        'context' : context,
        'query' : queryText,
        'assumptions' : assList,
        'answerVal': answerVal,
        'aUnits' : answerUnits,
        'instruction' : instruction
    }

    return echoback
