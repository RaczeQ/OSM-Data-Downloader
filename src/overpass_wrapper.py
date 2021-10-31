from functools import singledispatch

import geopandas as gpd
import pandas as pd
from alive_progress import alive_bar
from geojson import Point
from OSMPythonTools.overpass import Overpass
from shapely.geometry import shape

from .mongo_connector import save_data
from .overpass_queries import QUERIES

query_blank = '''
area({area_id})->.searchArea;
({body});
out skel body geom qt;
'''

@singledispatch
def remove_null_bool(ob):
    return ob

@remove_null_bool.register(list)
def _process_list(ob):
    return [remove_null_bool(v) for v in ob if v is not None]

@remove_null_bool.register(dict)
def _process_list(ob):
    return {k: remove_null_bool(v) for k, v in ob.items() if v is not None}

def _parse_geometry(element):
    dicts = []
    dict_data = {
        'id': str(element.id()),
        'type': element.type(),
        'lat': element.lat(),
        'lon': element.lon()
    }
    if element.tags():
        for key, value in element.tags().items():
            dict_data[key] = value
    try:
        shape(element.geometry())
        dict_data['geometry'] = element.geometry()
        dicts.append(dict_data)
    except Exception as ex:
        bbox = element._json['bounds']
        lat = round(float(bbox['maxlat'] + bbox['minlat']) / 2, 6)
        lon = round(float(bbox['maxlon'] + bbox['minlon']) / 2, 6)
        center_tuple = (lon, lat)
        dict_data['lat'] = lat
        dict_data['lon'] = lon
        dict_data['type'] = 'node'
        dict_data['geometry'] = Point(center_tuple)
        dicts.append(dict_data)
        print(f"Error loading geometry - {ex} (Saved center coordinates: {center_tuple})")
    return dicts

def _load_relation(osm_id, category):
    gdfs = []
    overpass = Overpass()
    query_body = ''
    for q in category.queries:
        for t in category.types:
            query_body += f'{t}{q}(area.searchArea);'
    builded_query = query_blank.format(area_id=3600000000+osm_id, body=query_body)
    with alive_bar(title=f"[{osm_id}] {category.name} | Loading OSM query", title_length=60) as bar:
        result = None
        while result is None:
            try:
                result = overpass.query(builded_query, timeout=600)
            except: # printed by OSMPythonTools already
                pass
        bar()
    elements = result.elements()
    with alive_bar(len(elements), title=f"[{osm_id}] {category.name} | Parsing geometries", title_length=60) as bar:
        for el in elements:
            try:
                gdfs.extend(_parse_geometry(el))
            except Exception as ex:
                # print(f"Error loading geometry for {el.type()} {el.id()} - {ex}")
                print(f"Error loading geometry for {el.type()} {el.id()}")
            bar()
    return gdfs


def load_relations_to_file(osm_id, dir_path_obj):
    for category in QUERIES:
        dicts = _load_relation(osm_id, category)
        if len(dicts) > 0:
            multi_gdf = gpd.GeoDataFrame(dicts)
            multi_gdf.sort_values(by=['id'], inplace=True)

            if category.subdirectory:
                dir_path_obj = dir_path_obj.joinpath(category.subdirectory)
            dir_path_obj.mkdir(parents=True, exist_ok=True)
            file_path = dir_path_obj.joinpath(f"{category.name}.geojson")
            str_path = str(file_path)
            saved = False

            removed_keys = []
            with alive_bar(title=f"[{osm_id}] {category.name} | Saving GeoDataFrame to file", title_length=60) as bar:
                while not saved:
                    try:
                        source_json = multi_gdf.to_json(na='drop')
                        with open(str_path, 'w', encoding='utf-8') as source:
                            source.write(source_json)
                        saved = True
                    except KeyError as err:
                        key = err.args[0]
                        removed_keys.append(key)
                        print(f"Removing key: {key}")
                        multi_gdf = multi_gdf.drop(columns=[key])
                bar()

            if len(removed_keys) > 0:
                print(f"Removed keys because of errors: {removed_keys}")

        print(f"{category.name} - Loaded {len(dicts)} elements")

def load_relations_to_mongo(osm_id, connection_string):
    for category in QUERIES:
        dicts = _load_relation(osm_id, category)
        if len(dicts) > 0:
            save_data(connection_string, dicts, osm_id, category.name)
        