import asyncio
import time
import uuid
import psycopg2
import os

from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from utils.db_access import DBAccess

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
            if file not in asyncio.run(self.get_converted_files()):
                event = FileCreatedEvent(os.path.join(CSV_INPUT_PATH, file))
                event.event_type = "created"
                self.dispatch(event)

    async def convert_csv(self, csv_path):
        # here we avoid converting the same file again
        # !TODO: check converted files in the database
        if csv_path in await self.get_converted_files():
            print(f"File '{csv_path}' has already been converted. Skipping.")
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
        
        # import the document to the db
        db_access = DBAccess()
        db_access.convert_document(csv_path, xml_path, file_size)
                
        # !TODO: we should store the XML document into the imported_documents table
        #open the file to send the xml data
        with open(xml_path,encoding='latin-1') as file:
            data = file.read()
            file.close()

        # import the file into the db
        db_access.import_xml_document(xml_path, data)

    async def get_converted_files(self):
        csv_files = []
        # !TODO: you should retrieve from the database the files that were already converted before
        db_access = DBAccess()
        files = db_access.get_converted_files()
        
        for file_tuple in files:
            # print(f"____Converted files: ", file_tuple) # ('/csv/dataset.csv',)
            file = file_tuple[0]  # extract the file path from the tuple
            # print(f"____Converted files: ", file) # /csv/dataset.csv
            csv_files.append(file)
        return csv_files

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            time.sleep(1)  # wait for 1 second before processing the file
            converted_files = asyncio.run(self.get_converted_files())
            print(f"_______Files to convert: ", event.src_path)
            if event.src_path not in converted_files:
                asyncio.run(self.convert_csv(event.src_path))
            elif event.src_path in converted_files:
                print(f"File '{event.src_path}' has already been converted. Skipping.")


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
