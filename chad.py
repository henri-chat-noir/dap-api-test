def buildEchoback(subject, sou, diffString, title, context, queryText, assList, defHelp, symHelp):

    answerVal = 42
    answerUnits = "kg-m/s2"
    instruction = "Please enter in Light-years per hour..."
    
    echoback = {
        'subject' : "A problem related to: " + subject,
        'sou' : "The system of units are: " + sou,
        'difficulty' : "The difficulty level is: " + diffString,
        'title' : title,
        'context' : context,
        'query' : queryText,
        'assumptions' : assList,
        'defHelp' : defHelp,
        'symfHelp' : symHelp,
        'answerVal': answerVal,
        'aUnits' : answerUnits,
        'instruction' : instruction
    }

    return echoback
