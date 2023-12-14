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
def import_xml(file_path,name_file):
    connection = None
    cursor = None
    try:
        connection = connect_connection()

        cursor = connect_cursor(connection)

        with open(file_path,encoding='latin-1') as file:
            data = file.read()

            cursor.execute("INSERT INTO imported_documents(file_name, xml) VALUES(%s, %s)", (name_file,data))

            connection.commit()
            
            print("Imported documents list:")
            for imported_file in cursor:
                print(f" > {imported_file[0]}, from {imported_file[1]}, col3: {imported_file[2]}, created on: {imported_file[3]}")



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

        cursor.execute(f"UPDATE imported_documents SET is_deleted = true, deleted_on = NOW() WHERE id = {doc_id}")

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

        cursor.execute(f"select id, file_name from imported_documents where \"isDeleted\" = false")

        query = cursor.fetchall()

        if connection:
            cursor.close()
            connection.close()
            return query

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

# Query functions

