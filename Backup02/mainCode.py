import os
import ast
import json
import pprint

os.chdir("C:\\0_Python\dap-api-test\\")
print(os.getcwd())
import functionsDAP as fDAP

dictPath = "C:\\0_Python\dap-api-test\\"
rawName = 'UnitsDict09hacked.json'    

with open(dictPath + rawName, 'r') as file:      # Open connection to file, read only
    rawDict = json.load(file)
# rawDict has the structure as list of dictionaries, i.e. each entry is un-keyed and only a member of a list

# Creat list of SI and other metric unit labels
metricUnits = []
for unitEntry in rawDict:

    if unitEntry['SOU'] in {'SI', 'non-SI metric', 'universal'}:
        metricUnits.append(unitEntry['name'])

# Extract SI and metric dictionary entries and build new dictionary, using 'name' of unit entry as key in new dictionary
# Also create proper list from string version of definition string, defString
metricDict = {}

for rawEntry in rawDict:
    unitName = rawEntry['name']
    if unitName in metricUnits:
        
        metricDict[unitName] = rawEntry
        defString = rawEntry['defString']
        defList = ast.literal_eval(defString)
        metricDict[unitName]['defList'] = defList

for item in metricDict.items():
    # print("Stage 1:", item[0], item[1]['defList'])

for entry in metricDict.items():
    breakStop = False
    tempList = []
    unitName = entry[0]
    unitInfo = entry[1]
    uID = unitInfo['Uid']
    actionList = True
    if uID == 525:
        breakStop = True
    
    # print("Now working on . . .:", uID, ". ", unitName)
    defList = unitInfo['defList']

    unitaryList = False
    if defList[0] == (1,1) and len(defList) == 1:
        breakStop = True
    
    while actionList:
    # baseStep defList and assign to tempList for iteration on this loop
        tempList = fDAP.baseStep(unitName, defList, metricDict)
        # print(uID, ". ", unitName, tempList)
        actionList = not fDAP.allSIBU(tempList)
    
    # When tempList fully processed place value in as new key into dictionary
    metricDict[unitName]['baseList'] = tempList
        
    tempList = fDAP.simplify(tempList)
    metricDict[unitName]['simpList'] = tempList

#   print("baseList: ", metricDict[unitName]['baseList'])
#   print("simpList: ", metricDict[unitName]['simpList'])
#   print("__________")

for entry in metricDict.items():

    unitName = entry[0]
    unitInfo = entry[1]
    uID = unitInfo['Uid']

    print("Stage 2: ", uID, ". ", unitName, unitInfo['defList'])
    print("baseList: ", unitInfo['baseList'])
    print("simpList: ", unitInfo['simpList'])
    print("__________")


