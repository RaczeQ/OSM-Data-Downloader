from pathlib import Path
from typing import Union

import geopandas as gpd
from OSMPythonTools.nominatim import Nominatim
from shapely.wkt import loads

from .mongo_connector import save_relation
from .overpass_wrapper import load_relations_to_file, load_relations_to_mongo

BASE_URL = "https://nominatim.openstreetmap.org/search.php?q={}&polygon_geojson=1&format=json"
BASE_URL_ID = "https://nominatim.openstreetmap.org/lookup?osm_ids=R{}&polygon_geojson=1&format=json"

def load_area(relation: Union[str, int]):
    relation_name = None
    nomin = Nominatim()
    if isinstance(relation, str):
        relations = nomin.query(relation, lookup = False, reverse = False, polygon_geojson = True, format = 'json', wkt = True).toJSON()
        relation_name = relation
    else:
        relations = nomin.query(f'R{relation}', lookup = True, reverse = False, polygon_geojson = True, format = 'json', wkt = True).toJSON()

    for relation in relations:
        if relation['osm_type'] != 'relation' and relation["class"] != "boundary":
            print('skipping relation - not boundary')
            continue
        osm_id = relation['osm_id']
        name = relation['display_name']
        if relation_name is None:
            relation_name = name
        bbox = relation['boundingbox']
        lat = float(relation['lat'])
        lon = float(relation['lon'])
        shp = loads(relation['geotext'])
        gdf = gpd.GeoDataFrame({'geometry':[shp]})
        relation_cls = BoundaryRelation(osm_id, relation_name, name, bbox, lat, lon, gdf)
        return relation_cls

class BoundaryRelation:
    def __init__(self, osm_id, relation_name, administration_name, bbox, lat, lon, geojson_shp):
        self.gdf = geojson_shp
        self.gdf['osm_id'] = osm_id
        self.gdf['lat'] = lat
        self.gdf['lon'] = lon
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
