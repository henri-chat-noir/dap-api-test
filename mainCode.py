# import os
import ast
import json

# print(os.getcwd())
# os.chdir("C:\\0_Python\dap-api-test\\")
import functionsJR as fJR

dictPath = "C:\\0_Python\dap-api-test\\"
rawName = 'UnitsDict07.json'    

with open(dictPath + rawName, 'r') as file:      # Open connection to file, read only
    rawDict = json.load(file)
# rawDict has the structure as list of dictionaries, i.e. each entry is un-keyed and only a member of a list

# Creat list of SI and other metric unit labels
metricUnits = []
for unitEntry in rawDict:

    if unitEntry['SOU'] in {'SI', 'non-SI metric'}:
        metricUnits.append(unitEntry['name'])

# Extract SI and metric dictionary entries and build new dictionary, using 'name' of unit entry as key in new dictionary
# Also create proper list from string version of definition string, defString
metricDict = {}
for rawEntry in rawDict:
    unitName = rawEntry['name']
    if unitName in metricUnits:
        
        metricDict[unitName] = rawEntry
        defList = ast.literal_eval(rawEntry['defString'])
        metricDict[unitName]['defList'] = defList

print(metricDict)

for entry in metricDict:

    pass

counter = 1
not_allSIBU = False
while counter <= 5:

    not_allSIBU = True
    for entry in unitsListing:

        defList = entry['defList']
        # print("This is target defList: ", defList)

        if entry['SOU'] == 'SI':

            if not fJR.allSIBU(defList):
                not_allSIBU = False
                rep_defList = fJR.base_step(defList, unitsListing)
                new_defList = fJR.simplify(rep_defList)
                entry['defList'] = new_defList
    
    counter = counter + 1

for entry in unitsListing:
    if entry['SOU'] == 'SI':
        print(entry['Uid'], ".", entry['name'], " revised defList ", entry['defList'])