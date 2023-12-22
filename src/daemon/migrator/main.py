import sys
import time

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


if __name__ == "__main__":

    db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    while True:

        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
            db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None or db_org is None:
            continue

        db_access_migrator = DBAccessMigrator()
        cars_data = []
        locations_data = []
        cafvs_data = []
        utilities_data = []
                
        print("Checking updates...")
              
        # !TODO: 1- Execute a SELECT query to check for any changes on the table     
        cursor_org = db_org.cursor()
        cursor_org.execute("SELECT id FROM imported_documents WHERE is_migrated = 'f' ORDER BY id DESC LIMIT 1")
        result = cursor_org.fetchone()
        document_id = result[0]
        print("Last document to migrate: ", result[0])  
        print("Fetching cars data...")
        cars_data = db_access_migrator.cars_to_store(document_id)
        print("Cars data fetched.")
        print("Fetching locations data...")
        locations_data = db_access_migrator.locations_to_store(document_id)
        cafvs_data = db_access_migrator.cafv_to_store(document_id)
        utilities_data = db_access_migrator.utility_to_store(document_id)

         
        # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
        print("Cars to store:")
        for car in cars_data:
            print("Maker:", car[0], "Model:", car[1], "Type:", car[2], "DOL:", car[3], "VIN:", car[4], "Year:", car[5], "Range:", car[6], "Location ID:", car[7], "CAFV ID:", car[8], "Utility ID:", car[9])

        print("Locations data to store:")
        for location in locations_data:
            print("Id:", location[0], "Name:", location[1], "Lat:", location[2], "Lon:", location[3])

        print("CAFVs to store:")
        for cafv in cafvs_data:
            print("Year:", cafv[0], "City:", cafv[1])
            
        print("Utilities to store:")
        for utility in utilities_data:
            print("Year:", utility[0], "City:", utility[1])
            
        # !TODO: 3- Execute INSERT queries in the destination db
        db_access_migrator.insert_cars(cars_data)
        
        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.
        cursor_org = db_dst.cursor()
        cursor_org.execute(f"UPDATE imported_documents SET is_migrated = TRUE WHERE id = {document_id}")
        
        db_org.close()
        db_dst.close()

        time.sleep(POLLING_FREQ)
