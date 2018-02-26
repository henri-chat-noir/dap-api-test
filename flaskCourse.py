# lower case flast - package; upper case Flask is a class / object
from flask import Flask 

# __name__ special Python variable that sets unique file name / location
app = Flask(__name__) 

# @app syntax is a decorator that defines route = endpoint = request that app will understand.  Decorator needs to act on a method.
@app.route('/') 

# home is method being associated with decorator.  Name can be anything you want.
# Whatever method does, it needs to show a response
def home(): 
    return "Hello, World!  Your on home page.  My name is John Richter"

@app.route('/page1')
def page1():
    return "This is page 1"

# If port already being used, just pick another number


# POST - used to receive data, i.e. 'posted by browser'
# GET - used to send some data, i.e. 'request to get some data by browser'

# POST /store data: {name:} - creates new store with given name
@app.route('/store', methods = ['POST'])
def create_store():
    pass

# GET /store/<string:name> - get a store with given name and return some data about it
@app.route('/store/<string:store_name>')
def get_store(store_name):

    pass


# GET /store - will return a list of all the stores
@app.route('/store')
def get_stores():


    pass


# POST /store/<string:name>/item {name:, price:} - creates an item within specific store (with given name)
@app.route('/store/<string:store_name>/item', methods = ['POST'])
def create_item(store_name):
    
    pass


# GET /store/<string:name>/item - list of all items in a store (of given name)
@app.route('/store/<string:store_name>/item')
def get_item(store_name):
    
    pass

app.run(port=5000)