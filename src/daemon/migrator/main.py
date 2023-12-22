import sys
import time

import psycopg2
from psycopg2 import OperationalError

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

        cursor_org = db_org.cursor()
        cursor_dst = db_dst.cursor()

        print("Checking updates...")        
        # !TODO: 1- Execute a SELECT query to check for any changes on the table        
        cursor_org.execute("SELECT * FROM imported_documents WHERE is_migrated = FALSE")
        records_to_migrate = cursor_org.fetchall()
        
        for record in records_to_migrate:
            # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
            # !TODO: 3- Execute INSERT queries in the destination db
            # Car data
            cursor_org.execute("""
                SELECT unnest(xpath('/ElectricCars/Makers/Maker/@name', xml))::text[] as maker,
                unnest(xpath('/ElectricCars/Makers/Maker/Model/@name', xml))::text[] as model,
                unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@type', xml))::text[] as type,
                unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@DOL', xml))::text[] as dol,
                unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@VIN', xml))::text[] as vin,
                unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@year', xml))::text[] as year,
                unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@range', xml))::text[] as range,
                unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@location_id', xml))::text[] as location_id,
                unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@cafv_id', xml))::text[] as cafv_id,
                unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@utility_id', xml))::text[] as utility_id
                FROM imported_documents WHERE id = %s
            """, (record[0],)) 
            data = cursor_org.fetchall()
            
            for row in data:
                cursor_dst.execute("""
                    INSERT INTO Cars (maker, model, type, DOL, VIN, year, range, location_id, cafv_id, utility_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
            
            # Location data
            cursor_org.execute("""
                SELECT unnest(xpath('/ElectricCars/Locations/State/@name', xml))::text[] as state,
                unnest(xpath('/ElectricCars/Locations/State/City/@name', xml))::text[] as city
                FROM imported_documents WHERE id = %s
            """, (record[0],))
            data = cursor_org.fetchall()
            
            for row in data:
                cursor_dst.execute("""
                    INSERT INTO Locations (state, city, geom)
                    VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                """, (row[0], row[1], row[2], row[3]))

            # CAFV data
            cursor_org.execute("""
                SELECT unnest(xpath('/ElectricCars/CAFVEligibility/Eligibility/@name', xml))::text[] as name
                FROM imported_documents WHERE id = %s
            """, (record[0],))
            data = cursor_org.fetchall()

            for row in data:
                cursor_dst.execute("""
                    INSERT INTO CAFV (name)
                    VALUES (%s)
                """, (row[0],))       

            # Utility data
            cursor_org.execute("""
                SELECT unnest(xpath('/ElectricCars/ElectricUtility/Utility/@name', xml))::text[] as name
                FROM imported_documents WHERE id = %s
            """, (record[0],))
            data = cursor_org.fetchall()

            for row in data:
                cursor_dst.execute("""
                    INSERT INTO Utility (name)
                    VALUES (%s)
                """, (row[0],))
                
            # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
            #          Change the db structure if needed.
            cursor_org.execute("""
                UPDATE imported_documents
                SET is_migrated = TRUE
                WHERE id = %s
            """, (record[0],))
        
        db_org.close()
        db_dst.close()

        time.sleep(POLLING_FREQ)
