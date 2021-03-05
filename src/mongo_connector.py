import pandas as pd
from pymongo import ASCENDING, GEOSPHERE, MongoClient
from pymongo.errors import WriteError
from shapely import geometry
from alive_progress import alive_bar


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

def save_gdf(connection_string, gdf, parent_osm_id, category):
    client = MongoClient(connection_string)
    db = client.osmDataDB
    coll = db.relations
    dict_records = []
    gdf_columns = gdf.columns
    with alive_bar(gdf.shape[0], title="Cleaning records from empty values") as bar:
        for row in gdf.itertuples():
            dct = {col:row[i + 1] for i, col in enumerate(gdf_columns) if pd.notnull(row[i + 1])}
            dict_records.append(dct)
            bar()
    with alive_bar(len(dict_records), title="Saving relations to MongoDB") as bar:
        for record in dict_records:
            document = record
            document['osm_id'] = int(document['id'])
            document['parent_osm_id'] = int(parent_osm_id)
            document['category'] = category
            del document['id']
            document['geometry'] = geometry.mapping(document['geometry'])
            try:
                coll.update({'parent_osm_id':document['parent_osm_id'], 'osm_id':document['osm_id']}, document, True)
            except WriteError as err:
                print(err)
                print(f"Skipping record: {document['osm_id']}")
            bar()
