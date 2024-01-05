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

# Get all makers
@app.route('/api/makers', methods=['GET'])
def get_makers():
    print("connecting to server...")
    server = xmlrpc.client.ServerProxy("http://rpc-server:8080")
    result = server.get_all_makers()
    print(f"API-PROC RESULT: ", result)
    return jsonify(result)

# Query 1 - Get all cars from x
@app.route('/api/maker', methods=['GET'])
def get_maker():
    maker = request.args.get('maker')

    print("connecting to server...")
    server = xmlrpc.client.ServerProxy("http://rpc-server:8080")
    result = server.get_maker(maker)
    return jsonify(result)

# Query 2 - Get all cars from x
@app.route('/api/year', methods=['GET'])
def get_year(year):
    return query_server('get_year')

# Query 3 - Get all cars with cafv x
@app.route('/api/elegible', methods=['GET'])
def get_elegible():
    return query_server('get_elegible')

# Query 4 - Get all cars with model type x 
@app.route('/api/type', methods=['GET'])
def get_type(phev):
    return query_server('get_type')

# Query 5 - Get all cars located in x
@app.route('/api/city', methods=['GET'])
def get_city(city):
    return query_server('get_city')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
