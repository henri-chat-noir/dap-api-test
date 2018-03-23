"""
Last mile -- building text that will feed JSON return

"""

def  buildContext(probType, paramObjList, probDict):
    
    preamble = "You need to run some calculations related to"

    probContextTemplate = probDict[probType]['probContext']

    probContext = preamble + " " + probContextTemplate

    return probContext

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
        'subject' : "A problem related to: " + subject + ".",
        'sou' : "The system of units are: "+sou +".",
        'difficulty' : "The difficulty level is: " + str(difficulty) + ".",
        'title' : title + " (" + sou + " units)",
        'context' : context,
        'query' : queryText,
        'assumptions' : assumptionText,
        'answerVal': answerVal,
        'aUnits' : answerUnits,
        'instruction' : instruction
    }

    return echoback
