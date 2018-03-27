import random as rand

def dealUnits(DLOlist, sou, metricDict):

    DLOUVlist = []
    for dim, argLam, obj in DLOlist:

        matchDims = []
        for unitName, unitInfo in metricDict.items():
            if unitInfo['dimension'] == dim:
                matchDims.append(unitName)
            
        maxIndex = len(matchDims) - 1
        pickIndex = rand.randint(0, maxIndex)
        unit = matchDims[pickIndex]

        unitVal = dealValue(unit)
        DLOUVlist.append((dim, argLam, obj, unit, unitVal))

    return DLOUVlist


def dealValue(unit):

    unitValue = rand.uniform(1, 10)

    return unitValue


def buildAnswer(DLOUVlist, unitDict):
    
    ansVal = 1.0

    for dim, argLambda, argObj, unit, value in DLOUVlist:

        unitCoeff = unitDict[unit]['coeff']
        ansVal *= (unitCoeff * value) ** argLambda

    ansUnits = DLOUVlist[0][3]
    if abs(ansVal) < 100000 and abs(ansVal) > .0001:
        ansFormat = "regular"
    else:
        ansFormat = "scinot"

    ansPack = (ansVal, ansUnits, ansFormat)
    
    return ansPack