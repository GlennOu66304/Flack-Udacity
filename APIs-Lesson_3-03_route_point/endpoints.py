from flask import Flask
app = Flask(__name__) 

# Routing
# https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing

# testing route
@app.route('/')
def helloword():
    return"Hello word!"
# Create the appropriate app.route functions. Test and see if they work

#Make an app.route() decorator here for when the client sends the URI "/puppies"
@app.route('/puppies')
def puppiesFunction():
  return "Yes, puppies!"
  
 
#Make another app.route() decorator here that takes in an integer named 'id' for when the client visits a URI like "/puppies/5"
@app.route('/puppies/<int:id>')
def puppiesFunctionId(id):
  return "This method will act on the puppy with id %s" % id

# Please use the localhost to send the api request to the route, under the VPN mode, the ip adddress does not work well
# http://localhost:5000/puppies/5
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)	
