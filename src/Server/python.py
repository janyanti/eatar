
from yelpapi import YelpAPI
from collections import Counter
from flask_restful import Resource, Api
from flask import Flask, request, jsonify

app = Flask(__name__)
api = Api(app)

api_key = "SExOGDQm8T4vWGcwXcPlCQDCzGW3ebCqXtMNJ3iuOF8vXbkvl8q2NrcY7EgBfwgCeyCn5M4VIlcXMbYp9ncMIQ8Mj-CDORkNVu4GylB-_6Hki9uWeSIUMveZOYZ9XXYx" 

yelp_api = YelpAPI(api_key)

"""
search_results = yelp_api.search_query(latitude = 42.358, longitude = -71.094, 
limit = 50,
term="businesses")

#42°21'46.2"N 71°05'46.0"W
Search2 = yelp_api.search_query(latitude = 42.362, longitude = -71.096, limit = 50,
term="restaurant")
Map = dict()
# search_results = yelp_api.search_query(location="New York, New York", term="businesses")
print(type(search_results))
print(len(search_results))
C = Counter()
for item in search_results["businesses"]:
    C[item['name']] += 1
for item in Search2["businesses"]:
    C[item['name']] += 1
print(C)"""

class SignUp(Resource):
    def post(self):
        # first name, last name, email, unique user id, password
        name = f"{request.json['first_name']} {request.json['last_name']}"
        username = request.json['email']
        id = request.json['id']
        password = request.json['password']
        
	# store in mongo
	

class Login(Resource):
    
    def post(self):
        username = request.json['email']
        password = request.json['password'] 
	
        # retrieve and verify from mongo


class Queue(Resource):
    def get(self):
        print("lol")

class Request(Resource):
    def get(self):
        group_id = request['group_id']
        # retrieve list of items from mongo with group id
        list = []
	# this represents the group queries
        
        counter = Counter()
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
            for item in search_results["businesses"]:
                counter[item] += 1        

        itemMaxValue = max(counter.items(), key=lambda x: x[1])
 
        listOfKeys = list()
        for key, value in sampleDict.items():
            if value == itemMaxValue[1]:
                listOfKeys.append(key)
        result = []
        for item in listOfKeys:
            result.append({'name':item[''], 
})

# name, display address, rating, price

        

api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Queue, '/queue')
api.add_resource(Request, '/request')

# try with deals
# try with basic match
# distance splicing, find midpoint
