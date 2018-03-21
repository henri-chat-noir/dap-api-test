"""
Module that contains functions used generically across different modules / stages of process, includes
combineLike - takes list of 2tuples in format (base, degree)
loadRaw - simple file load (that works on local system set-up)
outputJSON
"""

import json

def combineLike(targList):
    # Function that cycles through list of string, degree tuples and combines like terms
    # Presumes list is formed of 2tuples in format (string, degree), where return list 'collapses'
    # terms with identical strings by adding degrees together
    # This function does not (yet) eliminate terms with zero degree or convert them to "1"

    textList = []
    for text, degree in targList:
        if len(textList) == 0:
        # If first entry, just add text to string list
            textList = [text]
        else:
        # If text entry not already in text list, then append it
            if text not in textList:
                textList.append(text)  
    
    combined = []
    for uniqueText in textList:
        
        combDegree = 0
        for text, degree in targList:

            if text == uniqueText:
                combDegree = combDegree + degree
        
        combined.append( (uniqueText, combDegree) )

    return combined


def loadRaw(fileName):
    
    dictPath = "C:\\0_Python\dap-api-test\\"
    with open(dictPath + fileName, 'r') as file:      # Open connection to file, read only
        rawDict = json.load(file)
        # rawDict has the structure as list of dictionaries, i.e. each entry is un-keyed and only a member of a list
    
    return rawDict


def outputJson(targetDict, outputName):
    # Write fileName out to rawDict has the structure as list of dictionaries, i.e. each entry is un-keyed and only a member of a list

    outputPath = "C:\\0_Python\dap-api-test\\"
    with open(outputPath + outputName, 'w') as file:      # Open connection to file, write only
        json.dump(targetDict, file)
            
    return