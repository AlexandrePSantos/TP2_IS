import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.db_functions import import_xml, soft_delete_doc, list_undeleted_docs
from functions.db_functions import get_tesla, get_cars2022, get_100km, get_elegible, get_phev, get_seattle


PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(('localhost', PORT), requestHandler=RequestHandler) as server:
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
        server.register_function(get_tesla)
        server.register_function(get_cars2022)
        server.register_function(get_100km)
        server.register_function(get_elegible)
        server.register_function(get_phev)
        server.register_function(get_seattle)
        
        # Test the get_tesla function
        # # # print("Testing the function...")
        # # # result = get_tesla()
        # # # print(result)
        
        
        # start the server
        print(f"Starting the RPC Server in port {PORT}...")
        server.serve_forever()
