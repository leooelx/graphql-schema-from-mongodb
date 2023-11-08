from pymongo import MongoClient
from graphql import (
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLString,
    GraphQLList,
    print_schema,
)

# Conecte-se ao banco de dados MongoDB
client = MongoClient("<mongodb_connection_string>") 
db = client["<db_name>"]

# Defina um tipo GraphQL para os documentos no banco de dados
def create_graphql_type(collection_name):
    collection = db[collection_name]
    fields = {}
    for field in collection.find_one().keys():
        fields[field] = GraphQLString

    return GraphQLObjectType(collection_name, fields)

# Crie tipos GraphQL para cada coleção no banco de dados
def create_graphql_types():
    collection_names = db.list_collection_names()
    types = {}
    for collection_name in collection_names:
        types[collection_name] = create_graphql_type(collection_name)
    return types

graphql_types = create_graphql_types()

# Crie um tipo de consulta GraphQL que retorna todos os documentos em todas as coleções
root_query = GraphQLObjectType(
    "Query",
    {collection: GraphQLList(graphql_types[collection]) for collection in graphql_types},
)

# Crie o esquema GraphQL
schema = GraphQLSchema(query=root_query)

# Gere o esquema GraphQL como uma string
graphql_schema = print_schema(schema)

# Salve o esquema em um arquivo
with open("graphql_schema.graphql", "w") as f:
    f.write(graphql_schema)

print("Esquema GraphQL gerado e salvo em 'graphql_schema.graphql'")
