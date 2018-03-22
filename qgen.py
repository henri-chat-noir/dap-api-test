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

    localRun = False
    # subject, sou, and difficulty are search string arguments set-up for API
    if localRun:
        subject = 'mechanics'
        sou = 'SI'
        difficulty = 'hard'

    else:
        print("Hello World")
        subject = request.args.get('subject')
        sou = request.args.get('sou')
        difficulty = request.args.get('difficulty')

    echoback = fMaster.problemGen(subject, sou, difficulty)
    
    returnString = json.dumps(echoback)
    if localRun:
        print("echoback JSON: ", returnString)

    return returnString
    
# get_question()
if __name__ == '__main__':
    app.run(debug = True, use_reloader=True)