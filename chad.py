def buildEchoback(subject, sou, diffString, title, context, queryText, assList, defHelp, symHelp, ansPack, instruction):

    answerVal = ansPack[0]
    answerUnits = ansPack[1]
    
    echoback = {
        'subject' : "A problem related to: " + subject + ".",
        'sou' : "The system of units are: " + sou + ".",
        'difficulty' : "The difficulty level is: " + diffString + ".",
        'title' : title,
        'context' : context,
        'query' : queryText,
        'assumptions' : assList,
        'defHelp' : defHelp,
        'symHelp' : symHelp,
        'answerVal': answerVal,
        'aUnits' : answerUnits,
        'instruction' : instruction
    }

    return echoback
