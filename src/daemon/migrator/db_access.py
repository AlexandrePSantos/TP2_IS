import psycopg2
import xml.etree.ElementTree as ET

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

    def updateIsMigrated(self, id):
        connection = self.connect_connection_xml()
        with connection.cursor() as cursor:
            sql = "UPDATE imported_documents SET is_migrated = 't' WHERE id = %s"
            cursor.execute(sql, (id,))
        connection.commit()
        
    # SELECTS
    # WORKING
    def cars_to_store(self, id):
        cars = None
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_xml()
            cursor = self.connect_cursor(connection)

            query = """SELECT xml FROM public.imported_documents WHERE id = %s"""
            
            cursor.execute(query, (id,))
            result = cursor.fetchone()

            if result:
                xml_data = result[0]
                root = ET.fromstring(xml_data)

                cars = []

                for maker_elem in root.findall('.//Maker'):
                    maker_name = maker_elem.attrib['name']

                    models = []

                    for model_elem in maker_elem.findall('.//Model'):
                        model_name = model_elem.attrib['name']
                        model_type = model_elem.attrib['type']
                        
                        cars_data = []
                        
                        for car_elem in model_elem.findall('.//Car'):
                            car_data = {
                                'DOL': car_elem.attrib['DOL'],
                                'VIN': car_elem.attrib['VIN'],
                                'year': car_elem.attrib['year'],
                                'range': car_elem.attrib['range'],
                                'cafv_ref': car_elem.attrib['cafv_ref'],
                                'utility_ref': car_elem.attrib['utility_ref'],
                                'city_ref': car_elem.attrib['city_ref'],
                            }
                            cars_data.append(car_data)

                        models.append((model_name, model_type, cars_data))
                    
                    cars.append((maker_name, models))

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
        return cars

    # WORKING
    def locations_to_store(self, id):
        locations = None
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_xml()
            cursor = self.connect_cursor(connection)

            query = """SELECT xml FROM public.imported_documents WHERE id = %s"""
            
            cursor.execute(query, (id,))
            result = cursor.fetchone()

            if result:
                xml_data = result[0]
                root = ET.fromstring(xml_data)

                locations = []
                    
                for state_elem in root.findall('.//State'):
                    state_name = state_elem.attrib['name']
                    cities = [(city.attrib['id'], city.attrib['name']) for city in state_elem.findall('.//City')]
                    locations.append((state_name, cities))

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                return locations

    # WORKING
    def cafv_to_store(self, id):
        cafv = None
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_xml()
            cursor = self.connect_cursor(connection)

            query = """SELECT xml FROM public.imported_documents WHERE id = %s"""
            cursor.execute(query, (id,))
            result = cursor.fetchone()

            if result:
                xml_data = result[0]
                root = ET.fromstring(xml_data)

                cafv = []

                for eligibility_elem in root.findall('.//CAFVEligibility/Eligibility'):
                    idc = eligibility_elem.attrib.get('id', '')
                    name = eligibility_elem.attrib.get('name', '')
                    cafv.append((idc, name))

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                return cafv
    
    # WORKING    
    def utility_to_store(self, id):
        utilities = None
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_xml()
            cursor = self.connect_cursor(connection)

            query = """SELECT xml FROM public.imported_documents WHERE id = %s"""
            cursor.execute(query, (id,))
            result = cursor.fetchone()

            if result:
                xml_data = result[0]
                root = ET.fromstring(xml_data)

                utilities = []

                for utility_elem in root.findall('.//ElectricUtility/Utility'):
                    idc = utility_elem.attrib.get('id', '')
                    name = utility_elem.attrib.get('name', '')
                    utilities.append((idc, name))

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

            # Iterate over the locations
            for location in locations:
                state = location[0]
                cities = location[1]

                # Iterate over the cities in the current state
                for city_tuple in cities:
                    city_id = city_tuple[0]
                    city_name = city_tuple[1]
                    query = "INSERT INTO locations (xml_id, state, city) VALUES (%s, %s, %s)"
                    cursor.execute(query, (city_id, state, city_name))
   
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

            # Iterate over the values and construct and execute an INSERT statement for each value
            for row in cafvs:
                xml_id, name = row
                query = "INSERT INTO cafv (xml_id, name) VALUES (%s, %s)"
                cursor.execute(query, (xml_id, name))

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
            
            # Iterate over the values and construct and execute an INSERT statement for each value
            for row in utilities:
                xml_id, name = row
                query = "INSERT INTO utility (xml_id, name) VALUES (%s, %s)"
                cursor.execute(query, (xml_id, name))

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
            # print (cars)

            # Append the values we want to insert
            for car in cars:
                maker = car[0]
                # print (maker)
                for model_data in car[1]:
                    model = model_data[0]
                    model_type = model_data[1]  # Extract the model type here
                    for detail in model_data[2]:
                        # Execute the queries directly instead of calling the get_ methods
                        cursor.execute(f"SELECT id FROM locations WHERE xml_id = '{detail['city_ref']}'")
                        car_location_id = cursor.fetchone()[0]
                        cursor.execute(f"SELECT id FROM cafv WHERE xml_id = '{detail['cafv_ref']}'")
                        car_cafv_id = cursor.fetchone()[0]
                        cursor.execute(f"SELECT id FROM utility WHERE xml_id = '{detail['utility_ref']}'")
                        car_utility_id = cursor.fetchone()[0]

                        # Append the values with the foreign keys
                        values_to_insert.append((maker, model, model_type, detail['DOL'], detail['VIN'], detail['year'], detail['range'], car_location_id, car_cafv_id, car_utility_id))
                        
            # Iterate over the values and construct and execute an INSERT statement for each value
            for values in values_to_insert:
                query = "INSERT INTO cars (maker, model, type, DOL, VIN, year, range, location_id, cafv_id, utility_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, values)
                
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch dataaaaa", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
