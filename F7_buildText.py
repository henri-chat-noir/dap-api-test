"""
Last mile -- building text that will feed JSON return

"""

def  buildContext(probType, paramObjList, probDict):
    
    preamble = "You need to run some calculations related to"

    probContextTemplate = probDict[probType]['probContext']

    probContext = probContextTemplate

    return probContext

def buildQuery(ansTuple):

    queryText = "What is the " + ansTuple[0] + " of " + ansTuple[2]

    return queryText

def buildAss(argTuple):

    count = 0
    assText = ". . . if you are given the following assumptions:" + "\n"
    for dim, deg, obj in argTuple:
        count = count + 1
        value = "[value]"
        units = "[units]"
        coreText = "A " + dim + " [of/on/for] " + obj + " = " + value + " " + units
        assText = assText + str(count) + ".  " + coreText + "\n"

    return assText