import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.db_functions import import_xml, soft_delete_doc, list_undeleted_docs
from functions.db_functions import get_maker, get_year, get_elegible, get_city, get_all_makers, get_all_years, get_all_elegibles, get_all_cities

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(('0.0.0.0', PORT), requestHandler=RequestHandler) as server:
        server.register_introspection_functions()

        def signal_handler(signum, frame):
            print("received signal")
            server.server_close()

            # perform clean up, etc. here...
            print("exiting, gracefully")
            sys.exit(0)

        # signals
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        
        # XML functions registration
        server.register_function(import_xml)
        server.register_function(soft_delete_doc)
        server.register_function(list_undeleted_docs)
        
        # Query functions registration
        server.register_function(get_all_makers)
        server.register_function(get_maker)
        server.register_function(get_all_years)
        server.register_function(get_year)
        server.register_function(get_all_elegibles)
        server.register_function(get_elegible)
        server.register_function(get_all_cities)
        server.register_function(get_city)
        
        # print("ALL makers: ", get_all_makers())
        
        # start the server
        print(f"Starting the RPC Server in port {PORT}...")
        server.serve_forever()
