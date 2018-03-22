import os

os.chdir("/Users/Riston/qrmockup/dap/dap-api-test/")
print(os.getcwd())
import functionsDict as fDict

rawDict = fDict.loadRaw('UnitsDict13.json')

# Create list of SI and other metric unit labels
metricSOUs = {'SI', 'non-SI metric', 'universal'}
metricIDs = fDict.buildIDs(metricSOUs, rawDict)

metricDict = fDict.selectSubDict(metricIDs, rawDict)

metricOmits = {}
metricDict = fDict.listProcess(metricDict, metricOmits)

fDict.printDict(metricDict, metricOmits)
# fDict.printBaseUnits(metricDict)
