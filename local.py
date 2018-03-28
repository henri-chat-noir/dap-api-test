import json
import F9_master as fMaster

# subject, sou, and difficulty are search string arguments set-up for API
subject = 'mechanics'
sou = 'SI'
diffString = 'Simple'

echoback = fMaster.problemGen(subject, sou, diffString)
returnString = json.dumps(echoback)