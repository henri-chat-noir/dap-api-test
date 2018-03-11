import os
import pprint

os.chdir("C:\\0_Python\dap-api-test\\")
print(os.getcwd())
import functionsDAP as fDAP

rawDict = fDAP.loadRaw('UnitsDict13.json')

# Create list of SI and other metric unit labels
metricSOUs = {'SI', 'non-SI metric', 'universal'}
metricUnits = fDAP.buildSOUnames(metricSOUs, rawDict)

metricDict = fDAP.selectSubDict(metricUnits, rawDict)

metricOmits = {}
metricDict = fDAP.baseProcess(metricDict, metricOmits)

fDAP.printDict(metricDict, metricOmits)