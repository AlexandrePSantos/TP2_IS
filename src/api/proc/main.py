import sys
import xmlrpc.client
from flask import Flask, jsonify, request

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True


# Query server
def query_server(method_name):
    print("connecting to server...")
    server = xmlrpc.client.ServerProxy("http://rpc-server:8080")
    result = getattr(server, method_name)()
    return jsonify(result)

# Query 1 - Get all cars from TESLA
@app.route('/api/tesla', methods=['GET'])
def get_tesla():
    return query_server('get_tesla')

# Query 2 - Get all cars from from 2022
@app.route('/api/2022', methods=['GET'])
def get_cars2022():
    return query_server('get_cars2022')

# Query 3 - Get all cars with a range higer then 100  
@app.route('/api/100km', methods=['GET'])
def get_100km():
    return query_server('get_100km')

# Query 4 - Get all cars with cafv "Clean Alternative Fuel Vehicle Eligible"
@app.route('/api/elegible', methods=['GET'])
def get_elegible():
    return query_server('get_elegible')

# Query 5 - Get all cars with model type "Plug-in Hybrid Electric Vehicle (PHEV)"
@app.route('/api/phev', methods=['GET'])
def get_phev():
    return query_server('get_phev')

# Query 6 - Get all cars located in "Seattle"
@app.route('/api/seattle', methods=['GET'])
def get_seattle():
    return query_server('get_seattle')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
