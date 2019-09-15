#!/usr/bin/env python3
import sys
import random
import argparse
from yelpapi import YelpAPI

def printRestaurant(index, item):
    print(f"\n{index}.")
    print(f"Restaurant:\t\t\t{item['name']}")
    print("Address:\t\t\t" + ", ".join(item['location']['display_address']))
    print(f"Phone Number:\t\t\t{item['phone']}")
    print(f"Rating:\t\t\t\t{item['rating']}")
    if 'price' in item:
        print(f"Price:\t\t\t\t{item['price']}")
    

api_key = "SExOGDQm8T4vWGcwXcPlCQDCzGW3ebCqXtMNJ3iuOF8vXbkvl8q2NrcY7EgBfwgCeyCn5M4VIlcXMbYp9ncMIQ8Mj-CDORkNVu4GylB-_6Hki9uWeSIUMveZOYZ9XXYx" 

yelp_api = YelpAPI(api_key)

parser = argparse.ArgumentParser()
parser.add_argument("-loc", "--location", help="Specify an Address or Location such as a City, Town, or other Landmark", type=str)
parser.add_argument("-lat", "--latitude", help="Specify a Specific Latitude", type=float)
parser.add_argument("-long", "--longitude", help="Specify a Specific Longitude", type=float)
parser.add_argument("-r", "--random", help="Display a Random Restaurant Option, if not supplied, will default to show all the available restaurant options.", action="store_true")
parser.add_argument("-a", "--all", help="Display All Restaurant Options, default option", action="store_true")
parser.add_argument("--limit", help="Max number of Options to Display, by default displays 50, can display any number of restaurants between 1 and 50.", type=int)
args = parser.parse_args()

if args.limit < 1 or args.limit > 50:
    print("The limit must be in between 1 and 50")
    sys.exit(1)

while(True):
    try:
        lim = 50 if args.limit is None else args.limit
        results = None
        if args.location is None:
            if args.latitude is None or args.longitude is None:
                print("Latitude and Longitude or Location need to be supplied!")
                break
            results = yelp_api.search_query(latitude = args.latitude, longitude = args.longitude, limit = lim, term="restaurant")
        else:
            results = yelp_api.search_query(location = args.location, limit = lim, term="restaurant")
        if args.random:
            printRestaurant(1, results["businesses"][random.randint(0, len(results["businesses"]))])
        else:
            count = 1
            for item in results["businesses"]:
                printRestaurant(count, item)
                count += 1
        break
    except Exception:
        val = input("The command failed :(, Run again? y/n?")
        print(val)
        if val != 'y':
             break
    
    