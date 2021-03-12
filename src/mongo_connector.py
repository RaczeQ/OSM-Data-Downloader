from alive_progress import alive_bar
from pymongo import ASCENDING, GEOSPHERE, MongoClient
from pymongo.errors import WriteError
from shapely import geometry


def _prepare_database(connection_string):
    client = MongoClient(connection_string)
    if not 'osmDataDB' in client.list_database_names():
        db = client.osmDataDB
        coll_areas = db.areas
        coll_areas.create_index([("osm_id", ASCENDING)])
        coll_areas.create_index([("geometry", GEOSPHERE)])
        coll_relations = db.relations
        coll_relations.create_index([("parent_osm_id", ASCENDING)])
        coll_relations.create_index([("osm_id", ASCENDING)])
        coll_relations.create_index([("category", ASCENDING)])
        coll_relations.create_index([("geometry", GEOSPHERE)])

def save_relation(connection_string, relation_gdf):
    _prepare_database(connection_string)
    row = relation_gdf.iloc[0]
    document = {
        'osm_id': int(row.osm_id),
        'relation_name': row.relation_name,
        'administration_name': row.administration_name,
        'geometry': geometry.mapping(row.geometry)
    }

    client = MongoClient(connection_string)
    db = client.osmDataDB
    coll = db.areas
    coll.update({'osm_id':document['osm_id']}, document, True)

def save_data(connection_string, dicts, parent_osm_id, category):
    client = MongoClient(connection_string)
    db = client.osmDataDB
    coll = db.relations
    with alive_bar(len(dicts), title=f"[{parent_osm_id}] {category} | Saving relations to MongoDB", title_length=60) as bar:
        for record in dicts:
            document = record
            document['osm_id'] = int(document['id'])
            document['parent_osm_id'] = int(parent_osm_id)
            document['category'] = category
            del document['id']
            keys_to_del = [k for k,v in record.items() if v is None]
            for key in keys_to_del:
                del document[key]
            document['geometry'] = geometry.mapping(document['geometry'])
            try:
                coll.update({'parent_osm_id':document['parent_osm_id'], 'osm_id':document['osm_id'], 'category':document['category']}, document, True)
            except WriteError as err:
                # print(err)
                print(f"Skipping record: {document['osm_id']}")
            bar()
