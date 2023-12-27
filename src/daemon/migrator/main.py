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
         
        # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
        cars_data = db_access_migrator.cars_to_store(document_id)
        locations_data = db_access_migrator.locations_to_store(document_id)
        cafvs_data = db_access_migrator.cafv_to_store(document_id)
        utilities_data = db_access_migrator.utility_to_store(document_id)
            
        # !TODO: 3- Execute INSERT queries in the destination db
        db_access_migrator.insert_locations(locations_data)
        db_access_migrator.insert_cafv(cafvs_data)
        db_access_migrator.insert_utility(utilities_data)
        db_access_migrator.insert_cars(cars_data) 
        print("Inserts done!")
        
        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.
        cursor_org = db_org.cursor()
        cursor_org.execute(f"UPDATE imported_documents SET is_migrated = TRUE WHERE id = {document_id}")
        db_org.commit()
        
        db_org.close()
        db_dst.close()

        time.sleep(POLLING_FREQ)
