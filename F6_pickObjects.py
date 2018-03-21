"""
Prototype main processing, front to back at this point, with no separation of 'static' from 'dynamic' requirements
However, with that said, nascent efforts to start to organize into what needs to be calculated on each API call
from those elements that are static pre-processing of raw JSON files (and could then be exported and read in once)

"""
import F0_general as fGen
import random as rand

def setObjects(paramList, probType, dimDict, probDict):
    
    # For each the dimension for each parameter, find object compatible with both dimension and probType
    paramObjList = []
    for pDim, degree in paramList:
        
        dimObjects = dimDict[pDim]['dimObjects']
        # print(pDim, "possible parameter objects: ", paramObjects)
        
        probObjects = probDict[probType]['probObjects']
        # print(probType, "probObjects: ", probObjects)

        if len(probObjects) != 0:
            paramObjects = [i for i in probObjects if i in dimObjects]
        else:
            paramObjects = dimObjects[:]

        # print(pDim, "+for+", probType, "dimObjects:", dimObjects)
        numObj = len(paramObjects)
        if numObj > 0:
            pass
            # objIndex = rand.randint(1, numObj) - 1
        else:
            print("No valid dimensions found")
        
        # selectedObj = dimObjects[objIndex]
        newTuple = (pDim, degree, paramObjects)
        paramObjList.append(newTuple)
        
    return paramObjList