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

<<<<<<< HEAD
    # sector, sou, and difficulty are search string arguments set-up for API
    sector = request.args.get('sector')
    sou = request.args.get('sou')
    difficulty = request.args.get('difficulty')

    echo1 = "The sector you've asked for is: " + sector
    echo2 = "The system of units is: " + sou
    echo3 = "The level of difficulty is: " + difficulty

    # Need to look into random variable generation, but date/time works for now
    now = datetime.datetime.now()
    time_stamp = "Generated at: " + now.strftime("%d-%m-%Y %I:%M %p")

    # Temporary component just to have something added back on GET that's created by API code
    word_problem = "What is the answer to life, the universe, and everything? "
    instructions = "Please enter in miles per hour..."
    the_answer = 42
    answer_units = "miles/hour"

    echoback = {
      'sector' : echo1,
      'sou' : echo2,
      'difficulty' : echo3,
      'wordp' : word_problem,
      'times' : time_stamp,
      'answer': the_answer,
      'instruct' : instructions,
      'a_unit' : answer_units
    }

    return_string = json.dumps(echoback)
    return return_string

=======
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
>>>>>>> 9685c9280e7a7c34dee11f00bfd691bbccdf14f5
if __name__ == '__main__':
    app.run(debug = True, use_reloader=True)