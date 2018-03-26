import F0_general as fGen
import random as rand

def conformObjects(dimLambdas, objDict):
    # Clunky, but having randomly selected a set of objects, simplest process is then to re-set so that
    # Only get one object per object class, using the first one encountered to re-set any others
    # For instance "beer" and "wine" (both of class = fluids) cannont both be in same problem
    # In concept, this should be post-processed, but logic added in formation to prevent different objects from same class
    # However, dual-object problems, e.g. when we intro efficiency, will be required at some point, so deal with it then
    # As well, a single object can appear in multiple classes, e.g. piston as both moving object and force applicator
    # However, we can see how far this gets us (as a rough prototype)

    newDimLambdas = []
    paramObjDict = {}
    for dim, deg, object in dimLambdas:
        currentObjClass = findClass(object, objDict)
        if currentObjClass in list(paramObjDict.keys()):
            newObj = paramObjDict[currentObjClass]
        
        else:
            newObj = object
            paramObjDict[currentObjClass] = object
        
        newTuple = (dim, deg, newObj)
        newDimLambdas.append(newTuple)

    return newDimLambdas

def findClass(targetObj, objDict):

    objHit = False
    for objKey, objTuple in objDict.items():
       
        objList = objTuple[0]
        if targetObj in objList:
            objClass = objKey
            objHit = True
            return objClass
    
    if objHit == False:
        print("No object class identified for:", targetObj)

    return


def setObjects(paramList, probType, dimDict, probDict):
    
    # For each the dimension for each parameter, find object compatible with both dimension and probType
    paramObjList = []
    # Get list of 2tuple 'packs' for given problem, where each 2tuple is composed of two lists, 'objects' and 'dimensions'
    odPack = probDict[probType]['odPacks']

    for pDim, degree in paramList:
        
        dimObjects = dimDict[pDim]['dimObjects']
        # print(pDim, "possible parameter objects: ", paramObjects)
        
        for probObjects, probDims in odPack:
            # If this odPack doesn't contain pDim, then test next pack
            if pDim not in probDims:
                continue
            # print(probType, "probObjects: ", probObjects)
            
            # Data syntax presumes that the absense of probObjects, is 'inclusive of everything'
            if len(probObjects) != 0:
                paramObjects = [i for i in probObjects if i in dimObjects]
            else:
                paramObjects = dimObjects[:]
            # print(pDim, "+for+", probType, "dimObjects:", dimObjects)

            numObj = len(paramObjects)
            if numObj > 0:
                objIndex = rand.randint(1, numObj) - 1
                object = paramObjects[objIndex]
            else:
                print("No valid objects could be found for dimension = ", pDim)
        
            # selectedObj = dimObjects[objIndex]
            newTuple = (pDim, degree, object)
            paramObjList.append(newTuple)
        
    return paramObjList