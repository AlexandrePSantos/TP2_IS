import sys
import psycopg2
from flask import Flask, request, make_response, request, jsonify
from flask_cors import CORS

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/markers', methods=['GET'])
def get_markers():
    args = request.args
    neLng = args.get('neLng')
    neLat = args.get('neLat')
    swLng = args.get('swLng')
    swLat = args.get('swLat')

    # Connect to the database
    connection = psycopg2.connect(user="is", password="is", host="db-rel", database="is")

    # Create a cursor to execute queries
    cur = connection.cursor()

    # Corrigir query
    cur.execute(f"SELECT id, state, city, ST_Y(geom) as latitude, ST_X(geom) as longitude FROM Locations WHERE geom && ST_MakeEnvelope({neLng}, {neLat}, {swLng}, {swLat})")
    points = []

    for row in cur:
        points.append({
            "type": "feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row[3], row[4]]
            },
            "properties": {
                "id": row[0],
                "state": row[1],
                "city": row[2],
                "imgUrl" : "https://cdn-icons-png.flaticon.com/512/3202/3202926.png"
            }
        })

    print(points)

    cur.close()
    connection.close()

    response = make_response(jsonify(points))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
