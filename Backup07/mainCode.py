import functionsGen as fGen
import functionsDict as fDict
import functionsCore as fCore

rawDict = fGen.loadRaw('UnitsDict13.json')

# Create list, metricIDs, of SI and other metric unit labels
metricSOUs = {'SI', 'non-SI metric', 'universal'}
metricIDs = fDict.buildIDs(metricSOUs, rawDict)

# Build 'sub dictionary' (from raw load) based on metricIDs
metricDict = fDict.selectSubDict(metricIDs, rawDict)
metricOmits = {}
metricDict = fDict.listProcess(metricDict, metricOmits)

# Build appropriate dimensions dictionary (from raw JSON)
subject = "mechanics"
SOU = 'SI'
rawDims = "DimensionDict04.json"
mechSIdims = fCore.buildDims(subject, SOU, rawDims)

# Main procedure to create tuple list of dimensions, lambdas that are dimensionally congruent
answerDim = 'mass'
difficulty = 2

tryCount = 0
maxTry = 50
 
paramList = []
goodList = False
maxArgs = difficulty + 3
while not goodList and tryCount < maxTry:
    tryCount = tryCount + 1

    # Going to use difficulty variable as a threshold on minimum number of arguments before routine clears remaining base dimensions
    paramList = fCore.selectParameters(answerDim, difficulty, mechSIdims)
    
    if len(paramList) != 0 and len(paramList) <= maxArgs:
        goodList = True
    
argList = paramList[1:]
print(answerDim, "can be calculated with this combination of arguments: ")
print(argList)
print("Number of tries: ", tryCount)
print("----------")

probDict = fCore.createProbDict('ProblemDict03.json')

paramDims = [i[0] for i in paramList]
probType = fCore.findProbType(paramDims, probDict)

# fDict.printDict(metricDict, metricOmits)

# fDict.printBaseUnits(metricDict)
# fGen.outputJson(metricDict, 'metricDict-v01.json')

# print( json.dumps(metricDict, indent=4, sort_keys=True))

# printSet = {438}
# learn.printPath(metricDict, printSet)