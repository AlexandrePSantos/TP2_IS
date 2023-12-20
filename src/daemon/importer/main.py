import asyncio
import time
import uuid
import psycopg2
import os

from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

# from utils.to_xml_converter import CSVtoXMLConverter
from utils.xml_converter import CSVtoXMLConverter

def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']

def generate_unique_file_name(directory):
    return f"{directory}/{str(uuid.uuid4())}.xml"

def convert_csv_to_xml(in_path, out_path):
    converter = CSVtoXMLConverter(in_path)
    file = open(out_path, "w")
    file.write(converter.to_xml_str())

class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path

        # generate file creation events for existing files
        for file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames]:
            event = FileCreatedEvent(os.path.join(CSV_INPUT_PATH, file))
            event.event_type = "created"
            self.dispatch(event)

    async def convert_csv(self, csv_path):
        # here we avoid converting the same file again
        # !TODO: check converted files in the database
        if csv_path in await self.get_converted_files():
            return

        print(f"new file to convert: '{csv_path}'")

        # we generate a unique file name for the XML file
        xml_path = generate_unique_file_name(self._output_path)

        # we do the conversion
        # !TODO: once the conversion is done, we should updated the converted_documents tables
        convert_csv_to_xml(csv_path, xml_path)
        print(f"new xml file generated: '{xml_path}'")

        # get the file size
        file_size = Path(csv_path).stat().st_size
        
        # update the converted_documents table
        connection = None
        cursor = None
        try:
            connection = self.connect_connection()
            cursor = self.connect_cursor(connection)

            cursor.execute(f"insert into converted_documents(src,file_size,dst) values ('{csv_path}', {file_size}, '{xml_path}')")

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
                
        # !TODO: we should store the XML document into the imported_documents table
       #open the file to send the xml data
        with open(xml_path,encoding='latin-1') as file:
            data = file.read()
            file.close()
            
        connection = None
        cursor = None
        try:
            connection = self.connect_connection()
            cursor = self.connect_cursor(connection)

            cursor.execute("INSERT INTO imported_documents(file_name, xml) VALUES(%s, %s)", (xml_path, data))

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
            
    async def get_converted_files(self):
        # !DONE: you should retrieve from the database the files that were already converted before
        # Connect to the database
        connection = psycopg2.connect(user="is", password="is", host="db-xml", database="is")

        # Create a cursor to execute queries
        cur = connection.cursor()

        # Execute a SELECT query to retrieve the source files from the converted_documents table
        cur.execute("SELECT src FROM converted_documents")

        # Fetch all the results
        converted_files = [item[0] for item in cur.fetchall()]

        # Close the cursor and the connection
        cur.close()
        connection.close()

        return converted_files

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            asyncio.run(self.convert_csv(event.src_path))


if __name__ == "__main__":

    CSV_INPUT_PATH = "/csv"
    XML_OUTPUT_PATH = "/xml"

    # create the file observer
    observer = Observer()
    observer.schedule(
        CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH),
        path=CSV_INPUT_PATH,
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
