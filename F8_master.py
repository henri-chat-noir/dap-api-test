"""
Prototype main processing, front to back at this point, with no separation of 'static' from 'dynamic' requirements
However, with that said, nascent efforts to start to organize into what needs to be calculated on each API call
from those elements that are static pre-processing of raw JSON files (and could then be exported and read in once)

"""
import F0_general as fGen
import F1_utility as fUtil
import F2_unitsDict as fUnits
import F3_buildDicts as fBuild
import F4_dealParams as fParam
import F5_findProb as fProb
import F6_pickObjects as fObj
import F7_buildText as fText

def problemGen(subject, sou, difficulty):

    if sou == 'SI':
    elif sou == 'English':
        pass
    elif sou == 'Imperial':
        pass
    else:
        pass

    rawUnitsDict = fGen.loadRaw('UnitsDict13.json')

    # Create list, metricIDs based on passed system of units
    souSet = {'SI', 'non-SI metric', 'universal'}
    metricSOUs = {'SI', 'non-SI metric', 'universal'}
    unitIDlist = fUnits.buildIDlist(souSet, rawUnitsDict)
    # Build 'sub dictionary' (from raw load) based on unitIDlist
    metricDict = fUnits.extractSubDict(unitIDlist, rawUnitsDict)
    metricOmits = {}
    metricDict = fUnits.unitProcess(metricDict, metricOmits)



    # Need to use objDict in order to resolve the object class indicators that exist in either or both
    # dimensions' and 'problems' dictionaries
    objDict = fBuild.buildObjDict('dictObjects09.json')
    probDict = fBuild.buildProbDict('dictProblems18.json', objDict)

    # Process raw JSON into fully built-out dimensions dictionary
    rawDims = fGen.loadRaw("dictDimensions18.json")
    dimsDict = fBuild.buildDimsDict(rawDims, objDict)

    # Build appropriate dimensions dictionary (from raw JSON)
    
    exclDims = ['acceleration', 'action', 'currency', 'dynamic viscosity', 'energy density', 'frequency', 'kinematic viscosity', 'surface tension', 'torque']
    mechDimDict = fParam.selectDims(subject, exclDims, dimsDict)

    # Main procedure to create tuple list of dimensions, lambdas that are dimensionally congruent
    answerDim = fParam.dealAnswer(mechDimDict)
    print(answerDim, "can be calculated with this combination of arguments: ")

    # Need to convert whatever is set by web page into integer
    difficulty = 3

    tryCount = 0
    maxTry = 50

    paramList = []
    goodList = False
    maxArgs = difficulty + 3
    while not goodList and tryCount < maxTry:
        tryCount = tryCount + 1

        # Going to use difficulty variable as a threshold on minimum number of arguments before routine clears remaining base dimensions
        paramList = fParam.dealArguments(answerDim, difficulty, mechDimDict)
    
        if len(paramList) != 0 and len(paramList) <= maxArgs:
            goodList = True
    
    argList = paramList[1:]

    print(argList)
    print("Number of tries: ", tryCount)

    # print(objDict.items())

    paramDims = [i[0] for i in paramList]
    probType = fProb.findProbType(paramDims, probDict)
    print("Problem type: ", probType)
    print("----------")
    print("\n")

    paramObjList = fObj.setObjects(paramList, probType, mechDimDict, probDict)
    paramObjList = fObj.conformObjects(paramObjList, objDict)

    print("Established parameters, degrees, and connected objects:")
    for param in paramObjList:
        print(param)
    print("----------")
    print("\n")

    ansTuple = paramObjList[0]
    context = fText.buildContext(probType, ansTuple, probDict)
    queryText = fText.buildQuery(ansTuple)
    assumptionText = fText.buildAss(paramObjList[1:])

    print("Problem context: ", context)
    print("Query: ", queryText)
    print("\n")
    print(assumptionText)

    title = "Dummy title"
    echoback = fText.buildEchoback(subject, sou, difficulty, title, context, queryText, assumptionText)
    
    return echoback
