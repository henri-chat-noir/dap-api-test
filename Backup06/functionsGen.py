import json

def simplify(targList):
    # Function that cycles through list of string, degree tuples and combines like terms

    textList = []
    
    for text, degree in targList:
        if len(textList) == 0:
        # If first entry, just add text to string list
            textList = [text]
        
        else:
        # If text entry not already in text list, then append it
            if text not in textList:
                textList.append(text)  
    
    simplified = []
    for uniqueText in textList:
        
        combDegree = 0
        for text, degree in targList:

            if text == uniqueText:
                combDegree = combDegree + degree
        
        simplified.append( (uniqueText, combDegree) )

    return simplified


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


