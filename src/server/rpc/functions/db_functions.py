import psycopg2
from psycopg2 import sql
from lxml import etree

# Database connection
def connect_db():
    connection = psycopg2.connect(user="is", password="is", host="db-xml", database="is")
    return connection, connection.cursor()

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
    connection, cursor = execute_sql("SELECT xml FROM imported_documents WHERE is_deleted = 'f' ORDER BY id DESC LIMIT 1")
    xml_data = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return etree.fromstring(xml_data)

# Query functions (Using XPATH)
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
        "cafv_ref": root.xpath(f"//CAFVEligibility/Eligibility[@id='{car.get('cafv_ref')}']")[0].get("name"),
        "utility_ref": root.xpath(f"//ElectricUtility/Utility[@id='{car.get('utility_ref')}']")[0].get("name"),
        "city_ref": root.xpath(f"//Locations//City[@id='{car.get('city_ref')}']")[0].get("name"),
    }
    if exclude and exclude in car_dict:
        del car_dict[exclude]
    return car_dict

root = fetch_and_parse_xml()
    
# Query 1 - Get all cars from TESLA
def get_tesla():
    cars = root.xpath("//Maker[@name='TESLA']/Model/Car")
    return [create_car_dict(car, exclude="maker") for car in cars]

# Query 2 - Get all cars from from 2022
def get_cars2022():
    cars = root.xpath("//Car[@year='2022']")
    return [create_car_dict(car, exclude="year") for car in cars]

# Query 3 - Get all cars with a range higer then 100
def get_100km():
    cars = root.xpath("//Car[@range>'100']")
    return [create_car_dict(car, exclude="range") for car in cars]

# Query 4 - Get all cars with cafv "Clean Alternative Fuel Vehicle Eligible"
def get_elegible():
    cars = root.xpath("//Car[@cafv_ref='1']")
    return [create_car_dict(car, exclude="cafv") for car in cars]

# Query 5 - Get all cars with model type "Plug-in Hybrid Electric Vehicle (PHEV)"
def get_phev():
    cars = root.xpath("//Model[@type='Plug-in Hybrid Electric Vehicle (PHEV)']/Car")
    return [create_car_dict(car, exclude="type") for car in cars]

# Query 6 - Get all cars located in "Seattle"
def get_seattle():
    cars = root.xpath("//Car[@city_ref='1']")
    return [create_car_dict(car, exclude="city_ref") for car in cars]