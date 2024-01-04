import sys
import os
import time
import psycopg2
from pip._vendor import requests
import pika

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

def get_data(city, state):
    base_url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': f'{city}, {state}',
        'format': 'json'
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        try:
            coordinates = response.json()
            return [
                coordinates[0]["lat"],
                coordinates[0]["lon"]
            ]
        except (ValueError, IndexError, KeyError):
            print(f"Error parsing JSON response: {response.text}")
            return None
    else:
        print(f"Error making request: {response.status_code}, {response.text}")
        return None

def callback(ch, method, properties, body):
    message = body.decode()
    print(f"Received message: {message}")

    if message == "Activate":
        # print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...") // comentado por razoes de teste
        print(f"Getting all entities without coordinates...")
        connection = psycopg2.connect(user="is", password="is", host="db-rel", database="is")
        cur = connection.cursor()
        # cur.execute(f"SELECT id, city, state FROM Locations WHERE geom IS NULL LIMIT {ENTITIES_PER_ITERATION}") // comentado por razoes de teste
        cur.execute(f"SELECT id, city, state FROM Locations WHERE geom IS NULL")
        countries = cur.fetchall()

        for id, city, state in countries:
            coordinates = get_data(city, state)
            if coordinates is not None:
                cur.execute(f"UPDATE Locations SET geom = ST_SetSRID(ST_MakePoint({coordinates[1]}, {coordinates[0]}), 4326) WHERE id = '{id}'")
                connection.commit()
                
        print("Finished updating coordinates")

        cur.close()
        connection.close()

if __name__ == "__main__":
    user = os.getenv('RABBITMQ_DEFAULT_USER')
    password = os.getenv('RABBITMQ_DEFAULT_PASS')
    vhost = os.getenv('RABBITMQ_DEFAULT_VHOST')
    credentials = pika.PlainCredentials(user, password)
          
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='broker', virtual_host=vhost, credentials=credentials))
            channel = connection.channel()

            channel.queue_declare(queue='gis_updater_queue', durable=True) 

            channel.basic_consume(queue='gis_updater_queue', on_message_callback=callback, auto_ack=True)

            print('Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print("Connection was closed, retrying...")
            time.sleep(5)  # wait for 5 seconds before retrying
            
