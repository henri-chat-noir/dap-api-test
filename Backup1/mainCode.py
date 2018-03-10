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

# Extract SI and metric dictionary entries and build new dictionary
metricDict = {}
metricDict['unit'] = {}

for unitEntry in rawDict:

    if unitEntry['name'] in metricUnits:
        metricDict[unitEntry['name']] = unitEntry
 

node = metricDict
for key in metricUnits[:-1]:
    kv = unitLabel[i]
    next_node = node.get(kv, {})
    node[kv] = next_node
    node = next_node
    i = i + 1
last_node = node.get(unitLabel[keys[-1]], [])
last_node.append(unitLabel)
node[unitLabel[metricDict[-1]]] = last_node

for unitEntry in rawDict:
    
    defString = unitEntry['defString']
    unitEntry['defList'] = ast.literal_eval(defString)
    # print(entry)

# i = 0
# for entry in unitsListing:

#    if entry['SOU'] == 'SI':
#       print(i, entry)
#    i = i + 1

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