from findARestaurant import findARestaurant
from xml.sax import SAXException
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

# import sys
# import codecs

# sys.stdout = codecs.getwriter("utf8")(sys.stdout)
# sys.stderr = codecs.getwriter("utf8")(sys.stderr)




engine = create_engine("sqlite:///restaurants.db")

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route("/")
def TestRoute():
    mealType = request.args.get("mealType", "")
    location = request.args.get("location", "")
    restaurantInfo = findARestaurant(mealType, location)
    print(restaurantInfo)
    return restaurantInfo


@app.route("/restaurants", methods=["GET", "POST"])
def all_restaurants_handler():
    if request.method == "GET":
        return getAllRestaurants()
    elif request.method == "POST":
        print("make a new restaurant")
        # restaurant_name = request.args.get("restaurant_name", "")
        # restaurant_address = request.args.get("restaurant_address", "")
        # restaurant_image = request.args.get("restaurant_image", "")
        mealType = request.args.get("mealType", "")
        location = request.args.get("location", "")
        restaurant_info = findARestaurant(mealType, location)
        if restaurant_info != "No Restaurants Found":
            restaurant = Restaurant(
                # NameError: name 'unicode' is not defined in Python
                # https://bobbyhadz.com/blog/python-nameerror-name-unicode-is-not-defined#:~:text=The%20Python%20%22NameError%20name%20'unicode,to%20str%20in%20Python%203.&text=Copied!&text=Make%20sure%20to%20replace%20all,with%20str%20in%20your%20code.
                restaurant_name=str(restaurant_info["name"]),
                restaurant_address=str(restaurant_info["address"]),
                restaurant_image=restaurant_info["image"],
            )
            session.add(restaurant)
            session.commit()
            return jsonify(Restaurant=restaurant.serialize)
        else:
            return jsonify(
                {"error": "No Restaurants Found for %s in %s" % (mealType, location)}
            )


@app.route("/restaurants/<int:id>", methods=["GET", "PUT", "DELETE"])
def restaurant_handler(id):
    # YOUR CODE HERE
    if request.method == "GET":
        return getRestaurant(id)
    elif request.method == "PUT":
        print("update a new restaurant")
        address = request.args.get("address", "")
        name = request.args.get("name", "")
        image = request.args.get("image", "")
        return updateRestaurant(id, address, name, image)
    elif request.method == "DELETE":
        return deleteRestaurant(id)


def getAllRestaurants():
    restaurants = session.query(Restaurant).all()

    return jsonify(restaurants=[i.serialize for i in restaurants])


def makeANewRestaurant(restaurant_name, restaurant_address, restaurant_image):
    restaurant = Restaurant(restaurant_name, restaurant_address, restaurant_image)
    session.add(restaurant)
    session.commit()
    return jsonify(Restaurant=restaurant.serialize)


def getRestaurant(id):
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    return jsonify(restaurant=restaurant.serialize)


def updateRestaurant(id, name, address, image):
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    if name:
        restaurant.restaurant_name = name
    if address:
        restaurant.restaurant_address = address
    if image:
        restaurant.restaurant_image = image
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
