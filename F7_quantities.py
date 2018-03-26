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
