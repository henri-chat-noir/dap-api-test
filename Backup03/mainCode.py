import os
import ast
import json
import pprint

os.chdir("C:\\0_Python\dap-api-test\\")
print(os.getcwd())
import functionsDAP as fDAP

dictPath = "C:\\0_Python\dap-api-test\\"
rawName = 'UnitsDict13.json'    

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
        
        # JSON structure of defString formatted to 'look' like Python list, but needs to be converted into one
        # and added into dictionary under new 'defList' key
        defList = ast.literal_eval(defString)
        metricDict[unitName]['defList'] = defList

for entry in metricDict.items():
    # Main processing of next dictionary, creating baseList and simpList keys
    
    breakStop = False
    unitName = entry[0]

    unitInfo = entry[1]
    uID = unitInfo['Uid']
    actionList = True

    # Several entries English system (why?).  Also ('1', 1) tuples vs. (1, 1), "n.a.' symbol on steradians, bust with set-up on reciprocal meter
    # Dict09: exclUIDs = {50, 146, 268, 297, 374, 535, 661, 662, 591, 596, 525}
    exclUIDs = {}
    # If uID excluded, simply move on to next entry in dictionary
    if uID in exclUIDs:
        breakStop = True
        continue
    
    # print("Now working on . . .:", uID, ". ", unitName)
    # Bucket used where expectation is mutable; defList variable used as non-mutable        
    tempList = []           
    defList = unitInfo['defList']
    
    # Attack defList until all arguments have SIBU units returned into baseList
    actionList = not fDAP.allSIBU(defList)    
    
    while actionList:
        # baseStep defList and assign to tempList for iteration on this loop
        
        baseReturn = fDAP.baseStep(defList, uID, unitName, metricDict)
        tempList = baseReturn[0]
        baseError = baseReturn[1]
        
        # Partly to prevent endless looping on mal-formed elements,
        # but also just to call it a day if generating errors      
        if baseError == "OK":
            actionList = not fDAP.allSIBU(tempList)    
        else:
            actionList = False

    # When tempList fully processed place value in as new key into dictionary
    metricDict[unitName]['baseList'] = tempList
        
    tempList = fDAP.simplify(tempList)
    metricDict[unitName]['simpList'] = tempList

for entry in metricDict.items():
    # Output loop
    unitName = entry[0]
    unitInfo = entry[1]
    
    uID = unitInfo['Uid']
    if uID not in exclUIDs:

        print("Stage 2: ", uID, ". ", unitName, unitInfo['defList'])
        print("baseList: ", unitInfo['baseList'])
        print("simpList: ", unitInfo['simpList'])
        print("------------")