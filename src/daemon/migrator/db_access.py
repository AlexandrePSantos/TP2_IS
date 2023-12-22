import psycopg2

class DBAccessMigrator:
    def connect_connection_xml(self):
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="db-xml",
                                      database="is")
        return connection

    def connect_connection_rel(self):
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="db-rel",
                                      database="is")
        return connection

    def connect_cursor(self,connection):
        cursor = connection.cursor()
        return cursor

    # SELECTS
    def cars_to_store(self, id):
        cars = None
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_xml()
            cursor = self.connect_cursor(connection)

            query = """ SELECT  
                    (xpath('/ElectricCars/Makers/Maker/@name', xml)::text[])[1] as maker,
                    (xpath('/ElectricCars/Makers/Maker/Model/@name', xml)::text[])[1] as model,
                    (xpath('/ElectricCars/Makers/Maker/Model/@type', xml)::text[])[1] as type,
                    unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@DOL', xml)::text[]) as dol,
                    unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@VIN', xml)::text[]) as vin,
                    unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@year', xml)::text[]) as year,
                    unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@range', xml)::text[]) as range,
                    unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@city_ref', xml)::text[]) as location_id,
                    unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@cafv_ref', xml)::text[]) as cafv_id,
                    unnest(xpath('/ElectricCars/Makers/Maker/Model/Car/@utility_ref', xml)::text[]) as utility_id 
                    FROM imported_documents WHERE id = %s"""
                    
            print(f"Executing query: {query} with id: {id}")
            cursor.execute(query, (id,))

            cars = cursor.fetchall()
            print(f"Fetched cars: {cars}")
            # Print the data
            for car in cars:
                print(f"aaaaMaker: {car[0]}, Model: {car[1]}, Type: {car[2]}, DOL: {car[3]}, VIN: {car[4]}, Year: {car[5]}, Range: {car[6]}, Location ID: {car[7]}, CAFV ID: {car[8]}, Utility ID: {car[9]}")

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
        return cars

    def locations_to_store(self, id):
        locations = None
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_xml()

            cursor = self.connect_cursor(connection)

            query = """
                SELECT unnest(xpath('/ElectricCars/Locations/State/@name', xml)::text[]) as state,
                unnest(xpath('/ElectricCars/Locations/State/City/@name', xml)::text[]) as city
                FROM imported_documents WHERE id = %s
            """
            cursor.execute(query, (id,))

            locations = cursor.fetchall()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                return locations

    def cafv_to_store(self, id):
        cafv = None
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_xml()

            cursor = self.connect_cursor(connection)

            query = """
                SELECT unnest(xpath('/ElectricCars/CAFVEligibility/Eligibility/@name', xml)::text[]) as name
                FROM imported_documents WHERE id = %s
            """
            cursor.execute(query, (id,))

            cafv = cursor.fetchall()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                return cafv
            
    def utility_to_store(self, id):
        utilities = None
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_xml()

            cursor = self.connect_cursor(connection)

            query = """
                SELECT unnest(xpath('/ElectricCars/ElectricUtility/Utility/@name', xml)::text[]) as name
                FROM imported_documents WHERE id = %s
            """
            cursor.execute(query, (id,))

            utilities = cursor.fetchall()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                return utilities
    
    # INSERTS
    def insert_locations(self, locations):
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_rel()

            cursor = self.connect_cursor(connection)

            # Values to be inserted
            values_to_insert = []

            # Append the values we want to insert
            for row in locations: 
                values_to_insert.append((row[0],row[1], f'POINT({row[3]} {row[2]})')) 
            print(values_to_insert) 
            
            for values in values_to_insert:
                query = "INSERT INTO locations (state,city, geom) VALUES (%s,%s, ST_GeomFromText(%s))" 
                cursor.execute(query, values)
   
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

    def insert_cafv(self, cafvs):
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_rel()

            cursor = self.connect_cursor(connection)

            # Values to be inserted
            values_to_insert = []

            # Append the values we want to insert
            for row in cafvs:
                values_to_insert.append((row[0]))

            # Iterate over the values and construct and execute an INSERT statement for each value
            for values in values_to_insert:
                query = "INSERT INTO cafv (name) VALUES (%s)"
                cursor.execute(query, values)

            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                
    def insert_utility(self, utilities):
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_rel()

            cursor = self.connect_cursor(connection)

            # Values to be inserted
            values_to_insert = []

            # Append the values we want to insert
            for row in utilities:
                values_to_insert.append((row[0]))

            # Iterate over the values and construct and execute an INSERT statement for each value
            for values in values_to_insert:
                query = "INSERT INTO utility (name) VALUES (%s)"
                cursor.execute(query, values)

            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

    def insert_cars(self, cars):
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_rel()
            cursor = self.connect_cursor(connection)

            # Values to be inserted
            values_to_insert = []

            # Append the values we want to insert
            for car in cars:
                # Get the foreign keys
                car_location_id = self.get_car_location(car[7])  # locations
                car_cafv_id = self.get_car_cafv(car[8])  # cafvs
                car_utility_id = self.get_car_utility(car[9])  # utilities

                if car_location_id is not None and car_cafv_id is not None and car_utility_id is not None:
                    # Append the values with the foreign keys
                    values_to_insert.append((car[0], car[1], car[2], car[3], car[4], car[5], car[6], car_location_id[0], car_cafv_id[0], car_utility_id[0]))

            # Iterate over the values and construct and execute an INSERT statement for each value
            for values in values_to_insert:
                query = "INSERT INTO cars (maker, model, type, DOL, VIN, year, range, location_id, cafv_id, utility_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, values)

            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

    def get_car_location(self, car_location):
        location_id = None

        connection = None
        cursor = None

        try:
            connection = self.connect_connection_rel()
            cursor = self.connect_cursor(connection)

            query = f"SELECT id FROM locations WHERE name = '{car_location}'"
            cursor.execute(query)

            location_id = cursor.fetchone()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data car location", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
            return location_id

    def get_car_cafv(self, car_cafv):
        cafv_id = None

        connection = None
        cursor = None

        try:
            connection = self.connect_connection_rel()
            cursor = self.connect_cursor(connection)

            query = f"SELECT id FROM cafv WHERE name = '{car_cafv}'"
            cursor.execute(query)

            cafv_id = cursor.fetchone()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data car cafv", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
            return cafv_id

    def get_car_utility(self, car_utility):
        utility_id = None

        connection = None
        cursor = None

        try:
            connection = self.connect_connection_rel()
            cursor = self.connect_cursor(connection)

            query = f"SELECT id FROM utility WHERE name = '{car_utility}'"
            cursor.execute(query)

            utility_id = cursor.fetchone()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data car utility", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
            return utility_id
