from pymongo import MongoClient
config = {
	'entity_name_field': 'name',
    "mongo_host": "10.141.208.26:27017",
    "authDB": "admin",
    "username": "gdmdbuser",
    "password": "6QEUI8dhnq",
    "db": "huawei_sample",
    "user_table": "user",
    "entity_table": "entity",
    "relation_table": "triple_rel",
    "attribute_table": "triple_attr",
    "ment2ent_table": "ment2ent",
    "schema_table": "schema",
    "mongo_entity_id": False,
    "prefix_match": True,
}

client = MongoClient(config["mongo_host"])
client[config["authDB"]].authenticate(config["username"], config["password"], mechanism='SCRAM-SHA-1')

db = client.get_database(config['db'])
user_table = db.get_collection(config['user_table'])
entity_table = db.get_collection(config['entity_table'])
relation_table = db.get_collection(config['relation_table'])
attribute_table = db.get_collection(config['attribute_table'])
ment2ent_table = db.get_collection(config['ment2ent_table'])
schema_table = db.get_collection(config['schema_table'])
mongo_entity_id = config["mongo_entity_id"]
prefix_match = config["prefix_match"]