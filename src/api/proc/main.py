import sys
import xmlrpc.client
from flask import Flask, jsonify, request
from flask_cors import CORS

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
CORS(app) # Allow external origin to access
app.config["DEBUG"] = True


# Query server
def query_server(method_name, param=None):
    print("connecting to server...")
    try:
        server = xmlrpc.client.ServerProxy("http://rpc-server:9000")
        if param:
            result = getattr(server, method_name)(param)
        else:
            result = getattr(server, method_name)()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/api/makers', methods=['GET'])
def get_makers():
    return query_server("get_all_makers")

# Query 1 - Get all cars from x
@app.route('/api/maker', methods=['GET'])
def get_maker():
    maker = request.args.get('maker')
    return query_server('get_maker', maker)

@app.route('/api/years', methods=['GET'])
def get_all_years():
    return query_server('get_all_years')

# Query 2 - Get all cars from x
@app.route('/api/year', methods=['GET'])
def get_year():
    year = request.args.get('year')
    return query_server('get_year', year)

@app.route('/api/elegibles', methods=['GET'])
def get_all_elegibles():
    return query_server('get_all_elegibles')

# Query 3 - Get all cars with cafv x
@app.route('/api/elegible', methods=['GET'])
def get_elegible():
    elegible = request.args.get('elegible')
    return query_server('get_elegible', elegible)

@app.route('/api/cities', methods=['GET'])
def get_all_cities():
    return query_server('get_all_cities')

# Query 4 - Get all cars located in x
@app.route('/api/city', methods=['GET'])
def get_city():
    city = request.args.get('city')
    return query_server('get_city', city)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
