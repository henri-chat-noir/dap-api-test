# Using request to load in parsing option on GET command
from flask import Flask, request
from flask_cors import CORS, cross_origin

import datetime

app = Flask(__name__)
CORS(app)

# Defined endpoint at /getq
@app.route('/getq')

def get_question():
    
    # sector, sou, and difficulty are search string arguments set-up for API
    sector = request.args.get('sector')
    sou = request.args.get('sou')
    difficulty = request.args.get('difficulty')
    
    echo1 = "The sector you've asked for is: " + sector
    echo2 = "The system of units is: " + sou
    echo3 = "The level of difficulty is: " + difficulty
    echoback = echo1 + "\n" + echo2 + "\n" + echo3 + "\n"

    # Need to look into random variable generation, but date/time works for now
    now = datetime.datetime.now()
    time_stamp = now.strftime("%Y-%m-%d %H:%M")
    
    # Temporary component just to have something added back on GET that's created by API code
    word_problem = "This is your question which we've generated for you at: " + time_stamp

    return_string = echoback + word_problem
    return return_string

if __name__ == '__main__':
    app.run(debug = True, use_reloader=True)