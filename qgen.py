# Using request to load in parsing option on GET command
from flask import Flask, request
from flask_cors import CORS, cross_origin

import F8_master as fMaster
# import datetime
import json

app = Flask(__name__)
CORS(app)

# Defined endpoint at /getq
@app.route('/getq')

def get_question():
    
    apiRun = True

    # subject, sou, and difficulty are search string arguments set-up for API
    if apiRun:
        subject = request.args.get('subject')
        sou = request.args.get('sou')
        diffString = request.args.get('difficulty')
    
    else:
        subject = 'mechanics'
        sou = 'SI'
        diffString = 'Challenging'

    echoback = fMaster.problemGen(subject, sou, diffString)
    returnString = json.dumps(echoback)
    
    return returnString

if __name__ == '__main__':
    app.run(debug = True, use_reloader=True)
