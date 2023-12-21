import psycopg2

# Database connection


def connect_connection():
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-xml",
                                  database="is")

    return connection


def connect_cursor(connection):
    cursor = connection.cursor()

    return cursor

# XML functions


def import_xml(file_path, name_file):
    connection = None
    cursor = None
    try:
        connection = connect_connection()

        cursor = connect_cursor(connection)

        with open(file_path, encoding='latin-1') as file:
            data = file.read()

            cursor.execute(
                "INSERT INTO imported_documents(file_name, xml) VALUES(%s, %s)", (name_file, data))

            connection.commit()

            print("Imported documents list:")
            for imported_file in cursor:
                print(
                    f" > {imported_file[0]}, from {imported_file[1]}, col3: {imported_file[2]}, created on: {imported_file[3]}")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def soft_delete_doc(doc_id):
    try:
        connection = connect_connection()

        cursor = connect_cursor(connection)

        cursor.execute(
            f"UPDATE imported_documents SET is_deleted = true, deleted_on = NOW() WHERE id = {doc_id}")

        query = cursor.fetchall()

        connection.commit()

        if connection:
            cursor.close()
            connection.close()
            return query

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)


def list_undeleted_docs():
    try:
        connection = connect_connection()

        cursor = connect_cursor(connection)

        cursor.execute(
            f"select id, file_name from imported_documents where \"isDeleted\" = false")

        query = cursor.fetchall()

        if connection:
            cursor.close()
            connection.close()
            return query

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

# Query functions (Using XPATH)

# Query 1
# Return all the info of a car by its id


def car_info_by_id(car_id):
    try:
        connection = connect_connection()
        cursor = connect_cursor(connection)

        cursor.execute(f"""
            SELECT
                unnest(xpath('//Car[@id={car_id}]/@id', file)::text[]) as car_id,
                unnest(xpath('//Car[@id={car_id}]/Make/text()', file)::text[]) as make,
                unnest(xpath('//Car[@id={car_id}]/Model/text()', file)::text[]) as model,
            FROM
                imported_documents
            WHERE
                is_deleted = 'FALSE'
        """)

        car_data = cursor.fetchall()
        data = [{"car_id": car["car_id"], "make": car["make"],
                 "model": car["model"]} for car in car_data]

        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            return data

    except psycopg2.Error as error:
        print("Failed to fetch data", error)


# nao sei qual funciona melhor por isso deixei as duas
""" 
def releases_from_car_by_id(car_id):
    data = []
    try:
        connection = connect_connection()

        cursor = connect_cursor(connection)

        cursor.execute(f"SELECT unnest(xpath('//Car[@id={car_id}]', file)::text[]) "
                       f"FROM imported_documents WHERE is_deleted = 'FALSE'"
        )

        car_data = [{"car_id": id} for id in cursor.fetchall()]

        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            return car_data

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)
 """
# Query 2


def car_info_and_count(maker_name, model_name):
    try:
        connection = connect_connection()
        cursor = connect_cursor(connection)

        cursor.execute(f"""
            SELECT
                unnest(xpath('//Maker[@name="{maker_name}"]/Model[@name="{model_name}"]/Maker/text()', file)::text[]) as make,
                unnest(xpath('//Maker[@name="{maker_name}"]/Model[@name="{model_name}"]/Model/text()', file)::text[]) as model,
                count(xpath('//Maker[@name="{maker_name}"]/Model[@name="{model_name}"]/Car', file))::integer as car_count
            FROM
                imported_documents
            WHERE
                is_deleted = 'FALSE'
        """)

        car_data = cursor.fetchall()

        if connection:
            connection.commit()
            cursor.close()
            connection.close()

        return car_data

    except psycopg2.Error as error:
        print("Failed to fetch data", error)

# Query 3

def frequently_referenced_cars_in_city(city_ref):
    try:
        connection = connect_connection()
        cursor = connect_cursor(connection)

        cursor.execute(f"""
            SELECT
                unnest(xpath('//Car[@city_ref="{city_ref}"]/parent::Model/@name', file)::text[]) as model,
                unnest(xpath('//Car[@city_ref="{city_ref}"]/parent::Model/parent::Maker/@name', file)::text[]) as maker,
            FROM
                imported_documents
            WHERE
                is_deleted = 'FALSE'
        """)

        city_data = cursor.fetchall()

        if connection:
            connection.commit()
            cursor.close()
            connection.close()

        return city_data

    except psycopg2.Error as error:
        print("Failed to fetch data", error)

# Query 4

def cars_before_year_and_eligibility(cars_year, eligibility):
    try:
        connection = connect_connection()
        cursor = connect_cursor(connection)

        cursor.execute(f"""
            SELECT
                unnest(xpath('//Model[@year<=\"{cars_year}\" and @cafv_ref=\"{eligibility}\"]', file)::text[]) as car,
            FROM
                imported_documents
            WHERE
                is_deleted = 'FALSE'
        """)

        car_data = cursor.fetchall()

        if connection:
            connection.commit()
            cursor.close()
            connection.close()

        return car_data

    except psycopg2.Error as error:
        print("Failed to fetch data", error)

# Query 5
def cars_of_type_BEV():
    try:
        connection = connect_connection()
        cursor = connect_cursor(connection)

        cursor.execute(f"""
            SELECT
                unnest(xpath('count(//Model[@type=\"Battery Electric Vehicle (BEV)\"]/Car)', file)::text[]) as model,
            FROM
                imported_documents
            WHERE
                is_deleted = 'FALSE'
        """)

        BEV_data = cursor.fetchall()

        if connection:
            connection.commit()
            cursor.close()
            connection.close()

        return BEV_data

    except psycopg2.Error as error:
        print("Failed to fetch data", error)
