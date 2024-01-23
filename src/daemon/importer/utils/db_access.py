import time
from psycopg2 import OperationalError
import psycopg2

class DBAccess:
    def connect_connection(self):
        connection = None
        while connection is None:
            try:
                connection = psycopg2.connect(user="is",
                                              password="is",
                                              host="db-xml",
                                              database="is")
                print("Connection to PostgreSQL DB successful")
            except OperationalError as e:
                print(f"The error '{e}' occurred")
                print("PostgreSQL not ready yet, waiting for a while...")
                time.sleep(5)
        return connection

    def connect_cursor(self, connection):
        cursor = connection.cursor()

        return cursor

    # insert csv into db
    def convert_document(self,csv_path,xml_path,file_size):
        connection = None
        cursor = None
        try:
            connection = self.connect_connection()
            cursor = self.connect_cursor(connection)

            # cursor.execute(f"insert into converted_documents(src,file_size,dst) values ('{csv_path}', {file_size}, '{xml_path}')")
            query = "insert into converted_documents(src,file_size,dst) values (%s, %s, %s)"
            cursor.execute(query, (csv_path, file_size, xml_path))

            connection.commit()

            if connection:
                cursor.close()
                connection.close()

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

    # insert xml into db
    def import_xml_document(self,file_name,xml_data):
        connection = None
        cursor = None

        try:
            connection = self.connect_connection()
            cursor = self.connect_cursor(connection)

            cursor.execute("INSERT INTO imported_documents(file_name, xml) VALUES(%s, %s)", (file_name, xml_data))

            connection.commit()

            if connection:
                cursor.close()
                connection.close()

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

    # get converted csv files
    def get_converted_files(self):
        connection = None
        cursor = None
        try:
            connection = self.connect_connection()
            cursor = self.connect_cursor(connection)

            cursor.execute("select src from converted_documents")

            files = cursor.fetchall()

            if connection:
                cursor.close()
                connection.close()

                return files

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()



