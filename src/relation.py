from pathlib import Path

import geopandas as gpd
import requests
from shapely.geometry import shape

from .overpass_wrapper import load_relations

BASE_URL = "https://nominatim.openstreetmap.org/search.php?q={}&polygon_geojson=1&format=json"

def load_area(relation_name):
    url = BASE_URL.format(relation_name)
    r = requests.get(url)
    relation = r.json()[0]
    osm_id = relation['osm_id']
    name = relation['display_name']
    bbox = relation['boundingbox']
    shp = shape(relation['geojson'])
    # dummy_json = {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {}, "geometry": relation['geojson']}]}
    # gdf = gpd.GeoDataFrame.from_features(dummy_json)
    # gdf = gpd.GeoDataFrame.from_features(dummy_json)
    gdf = gpd.GeoDataFrame({'geometry':[shp]})
    relation_cls = BoundaryRelation(osm_id, relation_name, name, bbox, gdf)
    return relation_cls

class BoundaryRelation:
    def __init__(self, osm_id, relation_name, administration_name, bbox, geojson_shp, save_relation=True):
        self.gdf = geojson_shp
        self.gdf['osm_id'] = osm_id
        self.gdf['area_id'] = 3600000000 + osm_id
        self.gdf['relation_name'] = relation_name
        self.gdf['administration_name'] = administration_name
        print(self.gdf)

        if save_relation:
            self.save_relation()

    def _get_dir_path(self):
        return f'relation/{self.gdf.relation_name[0]}'

    def save_relation(self):
        path = self._get_dir_path()
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        self.gdf.to_file(str(p.joinpath("relation.geojson")), driver='GeoJSON', encoding='utf-8')

    def load_relations(self):
        p = Path(self._get_dir_path())
        p = p.joinpath("elements")
        load_relations(self.gdf.area_id[0], p)

    def __str__(self):
        # return f"Osm Id: {self.gdf.osm_id[0]} ({self.gdf.area_id[0]})\nName: {self.gdf.administration_name[0]}\nBounding box: {self.bounding_box}"
        return f"Osm Id: {self.gdf.osm_id[0]} ({self.gdf.area_id[0]})\nName: {self.gdf.administration_name[0]}"
