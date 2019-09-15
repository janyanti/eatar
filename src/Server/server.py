#########################
##       imports       ##
#########################
import json, datetime, flask, pymongo, dns
from flask import request, url_for, jsonify
from yelpapi import YelpAPI
from collections import Counter
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS, cross_origin
from constants import *
#########################

app = FlaskAPI(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
yelp_api = YelpAPI(API_KEY)


#########################
##   MongoDB Database  ##
#########################

client = pymongo.MongoClient(MONGO_URL)
db = client['Eatar_test'] # Database Name
users = db['users'] # User Collection
queries = db['query'] # Query Collection


"""
Compare two string values;
Ignore case
"""
def str_cmp(s1,s2):
    return s1.lower() == s2.lower()

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
        print(user)
    result = users.find_one({"email": user['email']})
    if user == None:
        return ('User Authenticfication Failed: User Not Found exists', 400)
    print(result)
    if (result['password'] != user['password']):
        return ('User Authenticfication Failed: Incorrect Credentials', 400)
    return ('User Authenticfication Successful', 201)

"""
query_user_data: request -> response
REQUIRES: True
ENSURES: Produces json string from request
"""
def query_user_data(request):

    query = dict()
    print(request.get_json(force=True))
    for key in QUERY_KEYS:
        query[key] = request.get_json(force=True)[key]

    result = queries.insert_one(query)
    if not result.inserted_id:
        return ('Query Operartion Failed', 400)
    return ('Successfuly Pushed Query', 201)

"""
get_query_data: request -> response
REQUIRES: True
ENSURES: Produces json string from request
"""
def get_query_data(request):

    res = []
    id = request.get_json(force=True)['group_id']
    groups = queries.find({'group_id' : id})
    for val in groups:
        res.append(val)
    print(len(res))
    return jsonify(len(res))


"""
exec_query: request -> response
REQUIRES: True
ENSURES: Produces json string from request
"""
def exec_query(request):

    res = []
    id = request.get_json(force=True)['group_id']
    groups = queries.find({'group_id' : id})
    print(request)
    for val in groups:
        res.append(val)
    print(res)
    return exec_yelp_query(res)



def exec_yelp_query(list):
    counter = Counter()
    trackers = {}
    for item in list:
        results1 = None
        results2 = None
        results3 = None
        if item['location'] is None:
            results1 = yelp_api.search_query(latitude = item['latitude'], longitude = item['longitude'], limit = 50, term="restaurant", attributes='deals')
            results2 = yelp_api.search_query(latitude = item['latitude'], longitude = item['longitude'], limit = 50, term="restaurant")
            results3 = yelp_api.search_query(latitude = item['latitude'], longitude = item['longitude'], limit = 50, term="restaurant", attributes='hot_and_new')
        else:
            results1 = yelp_api.search_query(location=item['location'], limit = 50, term="restaurant", attributes='deals')
            results2 = yelp_api.search_query(location=item['location'], limit = 50, term="restaurant")
            results3 = yelp_api.search_query(location=item['location'], limit = 50, term="restaurant", attributes='hot_and_new')

        for item in results1["businesses"]:
            if item['name'] not in trackers:
                trackers[item['name']] = item
            counter[item['name']] += 1
        for item in results2["businesses"]:
            if item['name'] not in trackers:
                trackers[item['name']] = item
            counter[item['name']] += 1
        for item in results3["businesses"]:
            if item['name'] not in trackers:
                trackers[item['name']] = item
            counter[item['name']] += 1

    itemMaxValue = max(counter.items(), key=lambda x: x[1])

    listOfKeys = []
    for key, value in counter.items():
        if value == itemMaxValue[1]:
            listOfKeys.append(trackers[key])
    result = []
    for item in listOfKeys:
        price = item['price'] if 'price' in item else 'N/A'
        result.append({'name':item['name'], 'rating':item['rating'], 'price':price , 'address':item['location']['display_address']})
    print(result)
    return jsonify(result)


#########################
##  REST API Methods   ##
#########################

@app.route('/', methods=['GET'])
@cross_origin()
def default():
    return "<h1>Test Server</h1><p>This is just a test!</p>"

@app.route('/register', methods=['POST', 'DELETE'])
@cross_origin()
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
@cross_origin()
def authUser():
    """
    authenticate user in the database
    """
    if request.method == "POST":
        (result, status) = auth_user_data(request)
        return jsonify(result), status # HTTP Status Created [201]

@app.route('/query', methods=['POST'])
@cross_origin()
def queryUser():
    """
    authenticate user in the database
    """
    if request.method == "POST":
        (result, status) = query_user_data(request)
        return jsonify(result), status # HTTP Status Created [201]

@app.route('/queries', methods=['POST'])
@cross_origin()
def getUserQueries():
    """
    get number of users in group_id
    """
    if request.method == "POST":
        result = get_query_data(request)
        if result:
            status = 200
        else:
            status = 400
        return result, status # HTTP Status Created [201]

@app.route('/execute_query', methods=['POST'])
@cross_origin()
def execQuery():
    """
    execute search query database
    """

    if request.method == "POST":
        result = exec_query(request)
        if result:
            status = 200
        else:
            status = 400
        return result, status # HTTP Status Created [201]


#########################
##        Main         ##
#########################

if __name__ == '__main__':
    app.run(debug=True)
