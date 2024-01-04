import time
import psycopg2
from psycopg2 import OperationalError
from lxml import etree

# Database connection
def connect_db():
    while True:
        try:
            connection = psycopg2.connect(user="is", password="is", host="db-xml", database="is")
            return connection, connection.cursor()
        except OperationalError:
            print("Unable to connect to the database. Retrying in 5 seconds...")
            time.sleep(5)

# Execute SQL query
def execute_sql(query, params=None):
    connection, cursor = None, None
    try:
        connection, cursor = connect_db()
        cursor.execute(query, params)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to execute query", error)
    finally:
        return connection, cursor

# XML functions
def import_xml(file_path, name_file):
    with open(file_path, encoding='latin-1') as file:
        data = file.read()
        execute_sql("INSERT INTO imported_documents(file_name, xml) VALUES(%s, %s)", (name_file, data))

def soft_delete_doc(doc_id):
    return execute_sql(f"UPDATE imported_documents SET is_deleted = t, deleted_on = NOW() WHERE id = {doc_id}").fetchall()

def list_undeleted_docs():
    return execute_sql(f"select id, file_name from imported_documents where \"is_deleted\" = f").fetchall()

def fetch_and_parse_xml():
    while True:
        connection, cursor = execute_sql("SELECT xml FROM imported_documents WHERE is_deleted = 'f' ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row is None:
            print("No data found. Retrying in 5 seconds...")
            cursor.close()
            connection.close()
            time.sleep(5)
            continue

        xml_data = row[0]
        cursor.close()
        connection.close()
        return etree.fromstring(xml_data)

root = fetch_and_parse_xml()

# Create dictionaries for Eligibility, Utility, and City elements
eligibility_dict = {el.get('id'): el.get('name') for el in root.xpath('//CAFVEligibility/Eligibility')}
utility_dict = {ut.get('id'): ut.get('name') for ut in root.xpath('//ElectricUtility/Utility')}
city_dict = {city.get('id'): city.get('name') for city in root.xpath('//Locations//City')}

def create_car_dict(car, exclude=None):
    model = car.getparent()
    car_dict = {
        "maker": model.getparent().get("name"),
        "model": model.get("name"),
        "type": model.get("type"),
        "id": car.get("id"),
        "DOL": car.get("DOL"),
        "VIN": car.get("VIN"),
        "year": car.get("year"),
        "range": car.get("range"),
        "cafv_ref": eligibility_dict[car.get('cafv_ref')],
        "utility_ref": utility_dict[car.get('utility_ref')],
        "city_ref": city_dict[car.get('city_ref')],
    }
    if exclude and exclude in car_dict:
        del car_dict[exclude]
    return car_dict
    
# Query 0 - Get all makers
def get_all_makers():
    makers = root.xpath("//Maker")
    return [maker.get("name") for maker in makers]

# Query 1 - Get all cars from maker
def get_maker(maker):
    cars = root.xpath(f"//Maker[@name='{maker}']/Model/Car")
    return [create_car_dict(car, exclude="maker") for car in cars]

# Query 2 - Get all cars from from 2022
def get_year(year):
    cars = root.xpath(f"//Car[@year='{year}']")
    return [create_car_dict(car, exclude="year") for car in cars]

# Query 4 - Get all cars with cafv "Clean Alternative Fuel Vehicle Eligible"
def get_elegible(cafv):
    cars = root.xpath(f"//Car[@cafv_ref='{cafv}']")
    return [create_car_dict(car, exclude="cafv") for car in cars]

# Query 5 - Get all cars with model type "Plug-in Hybrid Electric Vehicle (PHEV)"
def get_type(phev):
    cars = root.xpath(f"//Model[@type='{phev}']/Car")
    return [create_car_dict(car, exclude="type") for car in cars]

# Query 6 - Get all cars located in "Seattle"
def get_city(city):
    cars = root.xpath(f"//Car[@city_ref='{city}']")
    return [create_car_dict(car, exclude="city_ref") for car in cars]