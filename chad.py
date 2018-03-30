def buildEchoback(subject, sou, diffString, title, context, queryText, assList, defHelp, ansPack, instruction):

    answerVal = ansPack[0]
    answerUnits = ansPack[1]
    ansType = ansPack[2]

    unitConvText = "Unit conversions and symbols used*"
    unitConvNote1 = "Additional base unit symbols used:"
    unitConvNote2 = "m = meter; s = second; kg = kilogram"
    unitNotes = (unitConvText, unitConvNote1, unitConvNote2)

    echoback = {
        'subject' : "A problem related to: " + subject,
        'sou' : "The system of units are: " + sou,
        'difficulty' : "The difficulty level is: " + diffString + ".",
        'title' : title,
        'context' : context,
        'query' : queryText,
        'assumptions' : assList,
        'defHelp' : defHelp,
        'unitNotes' : unitNotes,
        'answerVal': answerVal,
        'aUnits' : answerUnits,
        'ansType': ansType,
        'instruction' : instruction
    }

    return echoback
