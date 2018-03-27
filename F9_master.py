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
import F7_quantities as fQuant
import F8_buildText as fText

import chad

def problemGen(subject, sou, diffString):

    rawUnitsDict = fGen.loadRaw('UnitsDict16.json')

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
    objDict = fBuild.buildObjDict('dictObjects12.json')
    probDict = fBuild.buildProbDict('dictProblems22.json', objDict)

    # Process raw JSONs into Python nexted dictionaries
    rawDims = fGen.loadRaw('dictDimensions18.json')
    dimsDict = fBuild.buildDimsDict(rawDims, objDict)
    symDict = fBuild.buildSymjDict('dictSymbols04.json')

    # Build appropriate dimensions dictionary (from dimsDict)
    exclDims = ['acceleration', 'action', 'currency', 'dynamic viscosity', 'energy density', 'frequency', 'kinematic viscosity', 'surface tension', 'torque']
    mechDimDict = fParam.selectDims(subject, exclDims, dimsDict)

#-----------MAIN PROCEDURE TO GENERATE PARAMETER LIST OF TUPLES, I.E. ANSWER AND REQUIRED ARGUMENTS THAT ARE DIMENSIONALLY CONGRUENT

    # Need to convert whatever is set by web page into integer; plus 1 added so Simple doesn't generate a 'zero', which is problematic for code
    difficulty = ["Simple", "Fairly easy", "Challenging", "Very hard", "Brutal"].index(diffString) + 1
    tryCount = 0
    maxTry = 50

    # Start by simply picking an Answer dimension randomly, i.e. 'dealing'
    answerDim = fParam.dealAnswer(mechDimDict)
    print(answerDim, "can be calculated with this combination of arguments: ")
    
    # Main loop that calls "dealArguments" function until seemingly valid set of parameters formed uprepeat
    # Primary objective is to construct a list of 2tuples with (dim, lamda) called dimLambdas
    
    goodList = False
    maxArgs = difficulty + 3
    while not goodList and tryCount < maxTry:
        tryCount = tryCount + 1

        # Going to use difficulty variable as a threshold on minimum number of arguments before routine clears remaining base dimensions
        # which is done via call to simpleDim function
        dimLambdas = fParam.dealArguments(answerDim, difficulty, mechDimDict)
    
        if len(dimLambdas) != 0 and len(dimLambdas) <= maxArgs:
            goodList = True
    
    argDimLambdas = dimLambdas[1:]

    print(argDimLambdas)
    print("Number of tries: ", tryCount)

    # Extract just dimension element from 2tuples and place into simple list
    # Finding relevant problem is a function of dimensions along, not their lambdas
    paramDims = [i[0] for i in dimLambdas]
    probType = fProb.findProbType(paramDims, probDict)
    print("Problem type: ", probType)
    print("----------")
    print("\n")

    # DLOlist is augmentation of dimLambda 2tuple with 3rd argument representing the "object" for each dimension
    DLOlist = fObj.setObjects(dimLambdas, probType, mechDimDict, probDict)
    DLOlist = fObj.conformObjects(DLOlist, objDict)

    # Produce 5tuple, by adding a units and (appropriate) value to each dimension
    DLOUVlist = fQuant.dealUnits(DLOlist, sou, metricDict)


# OUTPUT STATEMENTS

    print("Established parameters, lambdas, connected objects, units, and values:")
    for element in DLOUVlist:
        print(element)
    print("----------")
    print("\n")

    title = fText.buildTitle(probType, DLOlist, probDict)
    context = fText.buildContext(probType, DLOlist, probDict)
    
    ansTuple = DLOUVlist[0]
    queryText = fText.buildQuery(ansTuple)
    ansPack = fQuant.buildAnswer(DLOUVlist, metricDict)
    instruction = fText.buildInstruction(ansPack)

    assList = fText.buildAss(DLOUVlist[1:])
    defHelp = fText.buidDefHelp(DLOUVlist, metricDict)
    symHelp = fText.buidSymHelp(defHelp[1], symDict)
    
    print("Title: ", title)
    print("===============")
    
    print("Problem context: ", context)
    print("\n")
    print("Query: ", queryText)
    print("\n")
    for line in assList:
        print(line)
    print("\n")
    for line in defHelp[0]:
        print(line)
    
    print("\n")
    for line in symHelp:
        print(line)

    print("\n")
    print("Parameters of answer:")
    print("Answer value: ", ansPack[0])
    print("Units: ", ansPack[1])
    print("Instruction: ", instruction)

    echoback = chad.buildEchoback(subject, sou, diffString, title, context, queryText, assList, defHelp[0], symHelp, ansPack, instruction)
    print("\n")
    print("ECHOBACK:")
    print(echoback)
    
    return echoback