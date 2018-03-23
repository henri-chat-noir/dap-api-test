"""
Last mile -- building text that will feed JSON return

"""
import F3_buildDicts as fBuild
import re

def  buildContext(probType, paramObjList, probDict):
    
    preamble = "You need to run some calculations related to"
    conTemplate = probDict[probType]['probContext']
    context = preamble + " " + swapObjects(conTemplate, paramObjList)

    return context

def swapObjects(tempString, paramObjList):

    # Build simple list of objects connected with problem from paramObjList tuple
    # Note effort to create unique list may not strictly be required for following operations, but good practice
    probObjList = []
    for paramTuple in paramObjList:
        probObj = paramTuple[2]
        if probObj not in probObjList:
            probObjList.append(probObj)

    # Look through object dictionary and create list of 2tuples that can relate an object class to object
    objDict = fBuild.buildObjDict('dictObjects10.json')
    probClassObjList = []
    for probObj in probObjList:

        for objClass, objList in objDict.items():
            if probObj in objList:
                classObjTuple = (objClass, probObj)
                probClassObjList.append(classObjTuple)

    print("objClass, object 2tuple list: ", probClassObjList)

    # Replaced bracketed class indicators with object consistent with what dealt for problem
    bracketSearch = re.compile(r'\[.+?\]')
    bracketElements = re.findall(bracketSearch, tempString)
    
    outputString = tempString[:]
    for bElement in bracketElements:
        
        parseString = bElement[1:-1].split(", ")
        for parseObjClass in parseString:
            print("Object class: ", objClass)
            for probObjClass, probObj in probClassObjList:
                if parseObjClass == probObjClass:
                    test = bElement in outputString
                    outputString.replace(bElement, probObj)

        print(tempString, " replaced with:")
        print(outputString)
        print("=====")

        outputString = ""

    return outputString

def findObject(objClass, objList):

    pass

    return

def buildQuery(ansTuple):

    queryText = "What is the " + ansTuple[0] + " " + dimPrep(ansTuple[0]) + " " + ansTuple[2] + "?"

    return queryText

def buildAss(argTuple):

    count = 0
    assText = ". . . if you are given the following assumptions:" + "\n"
    for dim, deg, obj in argTuple:
        count = count + 1
        value = "[value]"
        units = "[units]"
        coreText = dim[0].upper() + dim[1:] + " " + dimPrep(dim) + " " + obj + " = " + value + " " + units
        assText = assText + str(count) + ".  " + coreText + "\n"

    return assText

def dimPrep(dim):
    # Sets preposition appled for objects based on dimension, e.g. "energy output of" [object], rather than simply "of"

    if dim in ['energy', 'power']:
        preposition = "output of"

    elif dim in ['force', 'pressure']:
        preposition = "applied by"

    else:
        preposition = "of"
        
    return preposition

def buildEchoback(subject, sou, difficulty, title, context, queryText, assumptionText):

    answerVal = 42
    answerUnits = "kg-m/s2"
    instruction = "Please enter in Light-years per hour..."

    echoback = {
        'subject' : "A problem related to " + subject,
        'sou' : sou,
        'difficulty' : difficulty,
        'title' : title + " (" + sou + " units)",
        'context' : context,
        'query' : queryText,
        'assumptions' : assumptionText,
        'answerVal': answerVal,
        'aUnits' : answerUnits,
        'instruction' : instruction
    }

    return echoback