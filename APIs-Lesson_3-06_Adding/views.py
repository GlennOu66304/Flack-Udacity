from findARestaurant import findARestaurant
from xml.sax import SAXException
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs

# sys.stdout = codecs.getwriter("utf8")(sys.stdout)
# sys.stderr = codecs.getwriter("utf8")(sys.stderr)


# foursquare_client_id = "PMXQTRX2WOU4EOZTSAXELWD2CYGFJ4TC0E55GIERDIVA2WKQ"
# foursquare_client_secret = "ROKNHTWGHJIEHEYYRFF04FJTXKPCWJWLU2OD5XHSDDHVSBCL"
# google_api_key = "AIzaSyDWKOKHKtSqnE1xFW6bzyRyoFRh2NiBzM8"

engine = create_engine("sqlite:///restaurants.db")

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route("/")
def TestRoute():
    mealType=request.args.get('mealType','')
    location=request.args.get('location','')
    restaurantInfo=findARestaurant(mealType,location)
    print(restaurantInfo)
    return restaurantInfo


@app.route("/restaurants", methods=["GET", "POST"])
def all_restaurants_handler():
    if request.method == "GET":
        return getAllRestaurants()
    elif request.method == "POST":
        print("make a new restaurant")
        restaurant_name = request.args.get("restaurant_name", "")
        restaurant_address = request.args.get("restaurant_address", "")
        restaurant_image = request.args.get("restaurant_image", "")
        return makeANewRestaurant(restaurant_name, restaurant_address, restaurant_image)


@app.route("/restaurants/<int:id>", methods=["GET", "PUT", "DELETE"])
def restaurant_handler(id):
    # YOUR CODE HERE
    if request.method == "GET":
        return getRestaurant(id)
    elif request.method == "PUT":
        print("update a new restaurant")
        restaurant_name = request.args.get("restaurant_name", "")
        restaurant_address = request.args.get("restaurant_address", "")
        restaurant_image = request.args.get("restaurant_image", "")
        return updateRestaurant(
            id, restaurant_name, restaurant_address, restaurant_image
        )
    elif request.method == "DELETE":
        return deleteRestaurant(id)


def getAllRestaurants():
    restaurants = session.query(Restaurant).all()

    return jsonify(restaurants=[i.serialize for i in restaurants])


def makeANewRestaurant(restaurant_name, restaurant_address, restaurant_image):
    restaurant = Restaurant(
        restaurant_name=restaurant_name,
        restaurant_address=restaurant_address,
        restaurant_image=restaurant_image,
    )
    session.add(restaurant)
    session.commit()
    return jsonify(Restaurant=restaurant.serialize)


def getRestaurant(id):
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    return jsonify(restaurant=restaurant.serialize)


def updateRestaurant(id, restaurant_name, restaurant_address, restaurant_image):
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    if not restaurant_name:
        restaurant.restaurant_name = restaurant_name
    if not restaurant_address:
        restaurant.restaurant_address = restaurant_address
    if not restaurant_image:
        restaurant.restaurant_image = restaurant_image
    session.add(restaurant)
    session.commit()
    # return "Updating a Restaurant with id %s" % id
    return jsonify(restaurant=restaurant.serialize)


def deleteRestaurant(id):
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    session.delete(restaurant)
    session.commit()
    return "Removing Restaurant with id %s" % id


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
