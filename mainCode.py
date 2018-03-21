import F_general as fGen
import F_unitsDict as fUnits
import F_buildDicts as fBuild
import F_coreProc as fCore

rawUnitsDict = fGen.loadRaw('UnitsDict13.json')

# Create list, metricIDs, of SI and other metric unit labels
# Require then to 
metricSOUs = {'SI', 'non-SI metric', 'universal'}
metricIDs = fUnits.buildIDlist(metricSOUs, rawUnitsDict)

# Build 'sub dictionary' (from raw load) based on metricIDs
metricDict = fUnits.extractSubDict(metricIDs, rawUnitsDict)
metricOmits = {}
metricDict = fUnits.unitProcess(metricDict, metricOmits)

# Need to use objDict in order to resolve the object class indicators that exist in either or both
# dimensions' and 'problems' dictionaries
objDict = fBuild.buildObjDict('dictObjects06.json')
probDict = fBuild.buildProbDict('dictProblems09.json', objDict)

# Process raw JSON into fully built-out dimensions dictionary
rawDims = fGen.loadRaw("dictDimensions12.json")
dimsDict = fBuild.buildDimsDict(rawDims, objDict)

# Build appropriate dimensions dictionary (from raw JSON)
subject = 'mechanics'
exclDims = ['acceleration', 'action', 'dynamic viscosity', 'energy density', 'frequency', 'kinematic viscosity', 'surface tension', 'torque']
mechDimDict = fCore.selectDims(subject, exclDims, dimsDict)

# Main procedure to create tuple list of dimensions, lambdas that are dimensionally congruent
answerDim = 'energy'
difficulty = 2

tryCount = 0
maxTry = 50

paramList = []
goodList = False
maxArgs = difficulty + 3
while not goodList and tryCount < maxTry:
    tryCount = tryCount + 1

    # Going to use difficulty variable as a threshold on minimum number of arguments before routine clears remaining base dimensions
    paramList = fCore.dealParameters(answerDim, difficulty, mechDimDict)
    
    if len(paramList) != 0 and len(paramList) <= maxArgs:
        goodList = True
    
argList = paramList[1:]
print(answerDim, "can be calculated with this combination of arguments: ")
print(argList)
print("\n")
print("Number of tries: ", tryCount)

# print(objDict.items())

paramDims = [i[0] for i in paramList]
probType = fCore.findProbType(paramDims, probDict)
print("Problem type: ", probType)
print("----------")
print("\n")

paramObjList = fCore.setObjects(paramList, probType, mechDimDict, probDict)
print("Established parameters, degrees, and objects:")
for param in paramObjList:
    print(param)
print("----------")
print("\n")

# fDict.printDict(metricDict, metricOmits)

# fUtil.printBaseUnits(metricDict)
# fGen.outputJson(metricDict, 'metricDict-v01.json')

# print( json.dumps(metricDict, indent=4, sort_keys=True))

# printSet = {438}
# learn.printPath(metricDict, printSet)