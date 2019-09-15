#########################
##       imports       ##
#########################
import json, datetime, flask, pymongo, dns
from flask import request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
from constants import *
#########################

app = FlaskAPI(__name__)
CORS(app)

#########################
##   MongoDB Database  ##
#########################

client = pymongo.MongoClient(MONGO_URL)
db = client['Eatar_test'] # Database Name
users = db['users'] # Collection name

"""
Compare two string values;
Ignore case
"""
def str_cmp(s1,s2):
    return s1.lower() == s2.lower()

def is_valid_user(data):
    #TODO implement with mongoDB database verification
    res = True
    status = 403
    voter_id = data['ID']
    first_name = data['first_name']
    last_name = data['last_name']
    DOB = data['DOB']
    voter = users.find_one({"ID": voter_id})
    if voter == None:
        res = False
        return (res, status)
    if voter_id in voted:
        res = False
        status = 400
        return (res, status)
    data_first = voter['first_name']
    data_last = voter['last_name']
    data_dob = voter['DOB']
    res = str_cmp(data_first,first_name) and str_cmp(data_last, last_name) and str_cmp(data_dob, DOB)
    if res:
        voted.append(voter_id)
    return (res, status)

"""
delete_user_data: request -> respone
REQUIRES: True
ENSURES: Produces json string from request
"""
def delete_user_data(request):
    # TODO return HTTP Resposne with regards to validation and vote POST
    voter_id = request.get_json(force=True)["ID"]
    voter = users.find_one({"ID": voter_id})
    if voter == None:
        return ('User Deletion Failed: No Such User Found', 404)
    users.delete_one({"ID": voter_id})
    return ('User Deletion Successful', 200)

"""
parse_user_data: request -> response
REQUIRES: True
ENSURES: Produces json string from request
"""
def parse_user_data(request):
    # TODO return HTTP Resposne with regards to validation and vote POST
    new_user = dict()
    user_id = ''
    print(request.get_json(force=True))
    for key in USER_KEYS:
        if key == 'ID':
            user_id = new_user[key] = request.get_json(force=True)[key]
            print(user_id)
        new_user[key] = request.get_json(force=True)[key]
    user = users.find_one({"ID": user_id})
    if user == None:
        users.insert_one(new_user)
        return ('User Registration Successful', 201)
    return ('User Registration Failed: User with ID exists', 400)


"""
auth_user_data: request -> response
REQUIRES: True
ENSURES: Produces json string from request
"""
def auth_user_data(request):

    user = dict()
    for key in AUTH_KEYS:
        user[key] = request.get_json(force=True)[key]
    result = users.find_one({"email": user['email']})
    if user == None:
        return ('User Authenticfication Failed: User Not Found exists', 400)
    print(result)
    if (result['password'] != user['password']):
        return ('User Authenticfication Failed: Incorrect Credentials', 400)
    return ('User Authenticfication Successful', 201)



#########################
##  REST API Methods   ##
#########################

@app.route('/', methods=['GET'])
def default():
    return "<h1>Test Server</h1><p>This is just a test!</p>"

@app.route('/register', methods=['POST', 'DELETE'])
def addUser():
    """
    Add new user/remove in the database
    """
    if request.method == "POST":
        (result, status) = parse_user_data(request)
        return jsonify(result), status # HTTP Status Created [201]
    if request.method == "DELETE":
        (result, status) = delete_user_data(request)
        return jsonify(result), status # HTTP Status Created [201]


@app.route('/authenticate', methods=['POST'])
def authUser():
    """
    authenticate user in the database
    """
    if request.method == "POST":
        (result, status) = auth_user_data(request)
        return jsonify(result), status # HTTP Status Created [201]

@app.route('/blocks', methods=['GET', 'POST'])
def appendBlock():
    """
    Add new block to exisiting blockchain
    """
    if request.method == 'POST':
        (result, status) = parse_vote_data(request)
        return jsonify(result), status # HTTP Status Created [201]

    return jsonify(votechain.getChain()), 200

@app.route("/block/<int:key>/", methods=['GET'])
def block_detail(key):
    """
    Retrieve block instances
    """
    if key not in blocks:
        raise exceptions.NotFound()
    return block_digest(key)

#########################
##        Main         ##
#########################

if __name__ == '__main__':
    app.run(debug=True)
