import os
# import json

os.chdir("C:\\0_Python\dap-api-test\\")
print(os.getcwd())
import functionsGen as fGen
import functionsDict as fDict
import functionsCore as fCore
# import learning as learn

rawDict = fGen.loadRaw('UnitsDict13.json')

# Create list of SI and other metric unit labels
metricSOUs = {'SI', 'non-SI metric', 'universal'}
metricIDs = fDict.buildIDs(metricSOUs, rawDict)

# Build 'sub dictionary' (from raw load) based on metricIDs
metricDict = fDict.selectSubDict(metricIDs, rawDict)
metricOmits = {}
metricDict = fDict.listProcess(metricDict, metricOmits)

# Build appropriate dimensions dictionary (from raw JSON)
subject = "mechanics"
rawDims = "DimensionDict04.json"
SOU = 'SI'
metricDims = fCore.buildDims(subject, SOU, rawDims)
breakStop = True
# fCore.printDims(metricDims, [])

fCore.selectParameters('mass', 2, metricDims)


# fDict.printDict(metricDict, metricOmits)

# fDict.printBaseUnits(metricDict)
# fGen.outputJson(metricDict, 'metricDict-v01.json')

# print( json.dumps(metricDict, indent=4, sort_keys=True))

# printSet = {438}
# learn.printPath(metricDict, printSet)