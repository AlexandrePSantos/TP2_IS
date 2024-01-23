import sys
import xmlrpc.client
from flask import Flask
import magql
from flask_magql import MagqlExtension

# Query server
def query_server(method_name, param=None):
    print("connecting to server...")
    try:
        server = xmlrpc.client.ServerProxy("http://rpc-server:9000")
        if param:
            result = getattr(server, method_name)(param)
        else:
            result = getattr(server, method_name)()
        return result
    except Exception as e:
        return {"error": str(e)}

schema = magql.Schema()

@schema.query.field("makers", "[String!]")
def resolve_makers(parent, info):
    return query_server("get_all_makers")

@schema.query.field("maker", "String!", args={"maker": magql.Argument("String!")})
def resolve_maker(parent, info, maker):
    return query_server("get_maker", maker)

@schema.query.field("years", "[Int!]")
def resolve_years(parent, info):
    return query_server("get_all_years")

@schema.query.field("year", "Int!", args={"year": magql.Argument("Int!")})
def resolve_year(parent, info, year):
    return query_server("get_year", year)

@schema.query.field("elegibles", "[String!]")
def resolve_elegibles(parent, info):
    return query_server("get_all_elegibles")

@schema.query.field("elegible", "String!", args={"elegible": magql.Argument("String!")})
def resolve_elegible(parent, info, elegible):
    return query_server("get_elegible", elegible)

@schema.query.field("cities", "[String!]")
def resolve_cities(parent, info):
    return query_server("get_all_cities")

@schema.query.field("city", "String!", args={"city": magql.Argument("String!")})
def resolve_city(parent, info, city):
    return query_server("get_city", city)

magql_ext = MagqlExtension(schema)

app = Flask(__name__)
app.config["DEBUG"] = True
magql_ext.init_app(app)
app.run(host="0.0.0.0", port=sys.argv[1])