import os
# import json

os.chdir("C:\\0_Python\dap-api-test\\")
print(os.getcwd())
import functionsDict as fDict
import learning as learn

rawDict = fDict.loadRaw('UnitsDict13.json')

# Create list of SI and other metric unit labels
metricSOUs = {'SI', 'non-SI metric', 'universal'}
metricIDs = fDict.buildIDs(metricSOUs, rawDict)

metricDict = fDict.selectSubDict(metricIDs, rawDict)

metricOmits = {}
metricDict = fDict.listProcess(metricDict, metricOmits)

# fDict.printDict(metricDict, metricOmits)

# fDict.printBaseUnits(metricDict)
# fDict.outputJson(metricDict, 'metricDict-v01.json')

# print( json.dumps(metricDict, indent=4, sort_keys=True))

printSet = {438}
learn.printPath(metricDict, printSet)

