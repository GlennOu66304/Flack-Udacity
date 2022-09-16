# -*- coding: utf-8 -*-
import json
import httplib2
import requests
from environs import Env
import sys
import codecs

# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)
env = Env()
# Read .env into os.environ
env.read_env()
google_api_key=env.str("google_api_key")
four_square_api_key=env.str("four_square_api_key")
print(google_api_key)
print(four_square_api_key)
# foursquare_api_key="fsq3kkGDfSbSIUluvji+agZTCZRcJseDaGStGxmq63fp96E="
google_api_key = google_api_key
headers = {"Authorization": four_square_api_key}


# Google API function
def getGeocodeLocation(inputString):
    # Replace Spaces with '+' in URL
    locationString = inputString.replace(" ", "+")
    # print(locationString)
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (
        locationString,
        google_api_key,
    )
    # print(url)
    h = httplib2.Http()
    # print(h)
    # result = json.loads(h.request(url,'GET',headers=headers)[1])
    result = json.loads(h.request(url, "GET")[1])
    # print(result)
    # print response
    latitude = result["results"][0]["geometry"]["location"]["lat"]
    longitude = result["results"][0]["geometry"]["location"]["lng"]
    print(latitude, longitude)
    return (latitude, longitude)


# FourSuqare API
# This function takes in a string representation of a location and cuisine type, geocodes the location, and then pass in the latitude and longitude coordinates to the Foursquare API
def findARestaurant(mealType, location):
    # find the latitude and longitude from the function above
    latitude, longitude = getGeocodeLocation(location)
    # print(latitude, longitude, mealType)
    url = "https://api.foursquare.com/v3/places/match?name=%s&ll=%s,%s" % (
        mealType,
        latitude,
        longitude,
    )
    print(url)
    h = httplib2.Http()
    result = json.loads(h.request(url, "GET", headers=headers)[1])
    # result = h.request(url, "GET", headers=headers)
    print(result)
    if result["fsq_id"]:
        # Grab the first restaurant
        restaurant = result
        fsq_id = restaurant["fsq_id"]
        # print(fsq_id)
        restaurant_name = restaurant["name"]
        # print(restaurant_name)
        restaurant_address = restaurant["location"]["formatted_address"]
        # print(restaurant_address)
        # Format the Restaurant Address into one string

        address = ""
        for i in restaurant_address:
            address += i + " "
        restaurant_address = address
        # print(address)
        # Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
        url = "https://api.foursquare.com/v3/places/%s/photos" % ((fsq_id))
        # print(url)
        result = json.loads(h.request(url, "GET",headers=headers)[1])
        # print(result)
        # Grab the first image
        # if no image available, insert default image url
        if result:
            firstpic = result[0]
            prefix = firstpic["prefix"]
            suffix = firstpic["suffix"]
            imageURL = prefix + "300x300" + suffix
        else:
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png"
        # print(imageURL)
        restaurantInfo = {
            "name": restaurant_name,
            "address": restaurant_address,
            "image": imageURL,
        }
        print(restaurantInfo)
        # print "Restaurant Name: %s " % restaurantInfo['name']
        # print "Restaurant Address: %s " % restaurantInfo['address']
        # print "Image: %s \n " % restaurantInfo['image']
        return restaurantInfo
    else:
        # print "No Restaurants Found for %s" % location
        return "No Restaurants Found"


if __name__ == "__main__":
    findARestaurant("Pizza", "Tokyo, Japan")
    # findARestaurant("Tacos", "Jakarta, Indonesia")
    # findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    # findARestaurant("Spaghetti", "New Delhi, India")
    # findARestaurant("Cappuccino", "Geneva, Switzerland")
    # findARestaurant("Sushi", "Los Angeles, California")
    # findARestaurant("Steak", "La Paz, Bolivia")
    # findARestaurant("Gyros", "Sydney Austrailia")
