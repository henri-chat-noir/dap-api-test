"""
Prototype main processing, front to back at this point, with no separation of 'static' from 'dynamic' requirements
However, with that said, nascent efforts to start to organize into what needs to be calculated on each API call
from those elements that are static pre-processing of raw JSON files (and could then be exported and read in once)

<<<<<<< HEAD

#original C:\\0_Python\dap-api-test\\
#local /Users/Riston/qrmockup/dap/dap-api-test/
os.chdir("C:\\0_Python\dap-api-test\\")
print(os.getcwd())
import functionsDict as fDict
=======
"""
import F0_general as fGen
import F1_utility as fUtil
import F2_unitsDict as fUnits
import F3_buildDicts as fBuild
import F4_dealParams as fParam
import F5_findProb as fProb
import F6_pickObjects as fObj
import F7_buildText as fText
>>>>>>> upstream/master

rawUnitsDict = fGen.loadRaw('UnitsDict13.json')

# Create list, metricIDs, of SI and other metric unit labels
<<<<<<< HEAD
# Require then to
=======
# Require then to 
>>>>>>> upstream/master
metricSOUs = {'SI', 'non-SI metric', 'universal'}
metricIDs = fUnits.buildIDlist(metricSOUs, rawUnitsDict)

# Build 'sub dictionary' (from raw load) based on metricIDs
metricDict = fUnits.extractSubDict(metricIDs, rawUnitsDict)
metricOmits = {}
metricDict = fUnits.unitProcess(metricDict, metricOmits)

# Need to use objDict in order to resolve the object class indicators that exist in either or both
# dimensions' and 'problems' dictionaries
objDict = fBuild.buildObjDict('dictObjects08.json')
probDict = fBuild.buildProbDict('dictProblems17.json', objDict)

# Process raw JSON into fully built-out dimensions dictionary
rawDims = fGen.loadRaw("dictDimensions17.json")
dimsDict = fBuild.buildDimsDict(rawDims, objDict)

# Build appropriate dimensions dictionary (from raw JSON)
subject = 'mechanics'
exclDims = ['acceleration', 'action', 'currency', 'dynamic viscosity', 'energy density', 'frequency', 'kinematic viscosity', 'surface tension', 'torque']
mechDimDict = fParam.selectDims(subject, exclDims, dimsDict)

# Main procedure to create tuple list of dimensions, lambdas that are dimensionally congruent
answerDim = fParam.dealAnswer(mechDimDict)
print(answerDim, "can be calculated with this combination of arguments: ")

difficulty = 2

tryCount = 0
maxTry = 50

paramList = []
goodList = False
maxArgs = difficulty + 3
while not goodList and tryCount < maxTry:
    tryCount = tryCount + 1

    # Going to use difficulty variable as a threshold on minimum number of arguments before routine clears remaining base dimensions
    paramList = fParam.dealArguments(answerDim, difficulty, mechDimDict)
<<<<<<< HEAD

    if len(paramList) != 0 and len(paramList) <= maxArgs:
        goodList = True

=======
    
    if len(paramList) != 0 and len(paramList) <= maxArgs:
        goodList = True
    
>>>>>>> upstream/master
argList = paramList[1:]

print(argList)
print("\n")
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

<<<<<<< HEAD
<<<<<<< HEAD
fDict.printDict(metricDict, metricOmits)
# fDict.printBaseUnits(metricDict)
=======
print("Problem context: ", context)
print("Query: ", queryText)
print("\n")
print(assumptionText)
>>>>>>> b9e45c323cba9fce591bb7603c97b9c76b088286
=======
print("Problem context: ", context)
print("Query: ", queryText)
print("\n")
print(assumptionText)
>>>>>>> upstream/master
