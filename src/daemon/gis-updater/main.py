import sys
import time
import psycopg2
from pip._vendor import requests
import urllib.parse

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

def get_data(city, state):
    address = f"{city}, {state}"
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'

    coordinates = requests.get(url).json()

    return [
        coordinates[0]["lat"],
        coordinates[0]["lon"]
    ]

if __name__ == "__main__":

    while True:
        print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...")
        # !TODO: 1- Use api-gis to retrieve a fixed amount of entities without coordinates (e.g. 100 entities per iteration, use ENTITIES_PER_ITERATION)
        connection = psycopg2.connect(user="is", password="is", host="db-rel", database="is")

        cur = connection.cursor()
        cur.execute(f"SELECT id, city, state FROM Locations WHERE geom IS NULL LIMIT {ENTITIES_PER_ITERATION}")
        countries = cur.fetchall()
        
        # !TODO: 2- Use the entity information to retrieve coordinates from an external API
        for id, city, state in countries:
            coordinates = get_data(city, state)

            cur.execute(f"UPDATE Locations SET geom = ST_SetSRID(ST_MakePoint({coordinates[1]}, {coordinates[0]}), 4326) WHERE id = {id}")

        
        # !TODO: 3- Submit the changes
        connection.commit()

        cur.close()
        connection.close()
        time.sleep(POLLING_FREQ)
