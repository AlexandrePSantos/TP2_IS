import os
import sys
import time
import pika

import psycopg2
from psycopg2 import OperationalError
from db_access import DBAccessMigrator

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60

def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")

def callback(ch, method, properties, body):
    document_id = int(body.decode().split(":")[1].strip())
    print(f"Received message with file id: {document_id}")

    db_access_migrator = DBAccessMigrator()
    cars_data = []
    locations_data = []
    cafvs_data = []
    utilities_data = []

    # Execute SELECT queries with xpath to retrieve the data we want to store in the relational db
    cars_data = db_access_migrator.cars_to_store(document_id)
    locations_data = db_access_migrator.locations_to_store(document_id)
    cafvs_data = db_access_migrator.cafv_to_store(document_id)
    utilities_data = db_access_migrator.utility_to_store(document_id)

    # Execute INSERT queries in the destination db
    print("Inserting Locations")
    db_access_migrator.insert_locations(locations_data)
    print("Inserting CAFVs")
    db_access_migrator.insert_cafv(cafvs_data)
    print("Inserting Utilities")
    db_access_migrator.insert_utility(utilities_data)
    print("Inserting Cars")
    db_access_migrator.insert_cars(cars_data)
    print("Inserts done!")

    # Update the is_migrated column for the document
    db_access_migrator.updateIsMigrated(document_id)
    print(f"Updated is_migrated for document {document_id}")
        

if __name__ == "__main__":
    user = os.getenv('RABBITMQ_DEFAULT_USER')
    password = os.getenv('RABBITMQ_DEFAULT_PASS')
    vhost = os.getenv('RABBITMQ_DEFAULT_VHOST')
    credentials = pika.PlainCredentials(user, password)
          
    while True:
        try:
            # print(f"User: {user}, Password: {password}, VHost: {vhost}")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='broker', virtual_host=vhost, credentials=credentials))
            channel = connection.channel()

            channel.queue_declare(queue='migrator_queue', durable=True) 

            channel.basic_consume(queue='migrator_queue', on_message_callback=callback, auto_ack=True)

            print('Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            # print(f"User: {user}, Password: {password}, VHost: {vhost}")
            print("Connection was closed, retrying...")
            time.sleep(5)  # wait for 5 seconds before retrying