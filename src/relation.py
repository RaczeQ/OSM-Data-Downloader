import logging
from pathlib import Path
from typing import Union

import geopandas as gpd
import requests
from alive_progress import alive_bar
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from shapely.geometry import shape

from .mongo_connector import save_relation
from .overpass_wrapper import load_relations_to_file, load_relations_to_mongo

BASE_URL = "https://nominatim.openstreetmap.org/search.php?q={}&polygon_geojson=1&format=json"
BASE_URL_ID = "https://nominatim.openstreetmap.org/lookup?osm_ids=R{}&polygon_geojson=1&format=json"

def load_area(relation: Union[str, int]):
    relation_name = None
    if isinstance(relation, str):
        url = BASE_URL.format(relation)
        relation_name = relation
    else:
        url = BASE_URL_ID.format(relation)
    req_proxy = RequestProxy(log_level=logging.ERROR)
    r = None
    with alive_bar(title=f"[{str(relation)}] | Loading Nominatim query", title_length=60) as bar:
        while r is None:
            r = req_proxy.generate_proxied_request(url)
            if r is None:
                print('Changing faulty proxy')
        bar()
    relations = r.json()
    for relation in relations:
        if relation['osm_type'] != 'relation' and relation["class"] != "boundary":
            print('skipping relation - not boundary')
            continue
        osm_id = relation['osm_id']
        name = relation['display_name']
        if relation_name is None:
            relation_name = name
        bbox = relation['boundingbox']
        shp = shape(relation['geojson'])
        gdf = gpd.GeoDataFrame({'geometry':[shp]})
        relation_cls = BoundaryRelation(osm_id, relation_name, name, bbox, gdf)
        return relation_cls

class BoundaryRelation:
    def __init__(self, osm_id, relation_name, administration_name, bbox, geojson_shp):
        self.gdf = geojson_shp
        self.gdf['osm_id'] = osm_id
        self.gdf['relation_name'] = relation_name
        self.gdf['administration_name'] = administration_name
        print(self.gdf)

    def _get_dir_path(self):
        return f'relation/{self.gdf.relation_name[0]}'

    def save_relation_to_file(self):
        path = self._get_dir_path()
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        self.gdf.to_file(str(p.joinpath("relation.geojson")), driver='GeoJSON', encoding='utf-8')

    def load_relations_to_file(self):
        self.save_relation_to_file()
        p = Path(self._get_dir_path())
        p = p.joinpath("elements")
        load_relations_to_file(self.gdf.osm_id[0], p)

    def load_relations_to_mongo(self, connection_string = 'mongodb://localhost:27017/'):
        save_relation(connection_string, self.gdf)
        load_relations_to_mongo(self.gdf.osm_id[0], connection_string)

    def __str__(self):
        return f"Osm Id: {self.gdf.osm_id[0]}\nName: {self.gdf.administration_name[0]}"
