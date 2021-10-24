from dataclasses import dataclass

OSM_W = 'way'
OSM_R = 'relation'
OSM_N = 'node'


@dataclass
class CategoryQuery:
    name: str
    types: list
    queries: list
    subdirectory: str = None

QUERIES = [
    CategoryQuery("water", [OSM_W, OSM_R], [
        '["natural"="water"]["water"="river"]',
        '["natural"="water"]["water"="moat"]',
        '["natural"="water"]["water"="reflecting_pool"]',
        '["natural"="water"]["water"="canal"]',
        '["natural"="water"]["water"="lake"]',
        '["natural"="water"]["water"="pond"]',
        '["natural"="water"]["water"="oxbow"]',
        '["natural"="water"]["water"="lagoon"]',
        '["natural"="water"]["water"="stream_pool"]',
        '["natural"="bay"]',
        '["natural"="beach"]',
        '["natural"="coastline"]',
        '["waterway"="riverbank"]'
    ]),
    CategoryQuery("aerialway", [OSM_N, OSM_W, OSM_R], [
        '["aerialway"]["aerialway"!="pylon"]'
    ]),
    CategoryQuery("airports", [OSM_N, OSM_R], [
        '["aeroway"="aerodrome"]',
        '["aeroway"="heliport"]',
        '["aeroway"="spaceport"]',
    ]),
    CategoryQuery("sustenance", [OSM_N, OSM_R], [
        '["amenity"="bar"]',
        '["amenity"="bbq"]',
        '["amenity"="biergarten"]',
        '["amenity"="cafe"]',
        '["amenity"="fast_food"]',
        '["amenity"="food_court"]',
        '["amenity"="ice_cream"]',
        '["amenity"="pub"]',
        '["amenity"="restaurant"]',
    ]),
    CategoryQuery("education", [OSM_N, OSM_R], [
        '["amenity"="college"]',
        '["amenity"="driving_school"]',
        '["amenity"="kindergarten"]',
        '["amenity"="language_school"]',
        '["amenity"="library"]',
        '["amenity"="toy_library"]',
        '["amenity"="music_school"]',
        '["amenity"="school"]',
        '["amenity"="university"]'
    ]),
    CategoryQuery("transportation", [OSM_N, OSM_R], [
        '["amenity"="bicycle_parking"]',
        '["amenity"="bicycle_repair_station"]',
        '["amenity"="bicycle_rental"]',
        '["amenity"="boat_rental"]',
        '["amenity"="boat_sharing"]',
        '["amenity"="car_rental"]',
        '["amenity"="car_sharing"]',
        '["amenity"="car_wash"]',
        '["amenity"="charging_station"]',
        '["amenity"="bus_stop"]',
        '["public_transport"="station"]',
        '["public_transport"="stop_position"]',
        '["amenity"="ferry_terminal"]'
        '["amenity"="fuel"]',
        '["amenity"="motorcycle_parking"]',
        '["amenity"="parking"]',
        '["amenity"="taxi"]',
        '["building"="train_station"]'
        '["railway"="station"]',
        '["railway"="subway_entrance"]',
        '["railway"="tram_stop"]'
    ]),
    CategoryQuery("finances", [OSM_N, OSM_R], [
        '["amenity"="atm"]',
        '["amenity"="bank"]',
        '["amenity"="bureau_de_change"]'
    ]),
    CategoryQuery("healthcare", [OSM_N, OSM_R], [
        '["amenity"="baby_hatch"]',
        '["amenity"="clinic"]',
        '["amenity"="dentist"]',
        '["amenity"="doctors"]',
        '["amenity"="hospital"]',
        '["amenity"="nursing_home"]',
        '["amenity"="pharmacy"]',
        '["amenity"="social_facility"]',
        '["amenity"="veterinary"]'
    ]),
    CategoryQuery("culture_art_entertainment", [OSM_N, OSM_R], [
        '["amenity"="arts_centre"]',
        '["amenity"="brothel"]',
        '["amenity"="casino"]',
        '["amenity"="cinema"]',
        '["amenity"="community_centre"]',
        '["amenity"="gambling"]',
        '["amenity"="nightclub"]',
        '["amenity"="planetarium"]',
        '["amenity"="public_bookcase"]',
        '["amenity"="social_centre"]',
        '["amenity"="stripclub"]',
        '["amenity"="studio"]',
        '["amenity"="theatre"]'
    ]),
    CategoryQuery("other", [OSM_N, OSM_R], [
        '["amenity"="animal_boarding"]',
        '["amenity"="animal_shelter"]',
        '["amenity"="childcare"]',
        '["amenity"="conference_centre"]',
        '["amenity"="courthouse"]',
        '["amenity"="crematorium"]',
        '["amenity"="embassy"]',
        '["amenity"="fire_station"]',
        '["amenity"="grave_yard"]',
        '["amenity"="internet_cafe"]',
        '["amenity"="marketplace"]',
        '["amenity"="monastery"]',
        '["amenity"="place_of_worship"]',
        '["amenity"="police"]',
        '["amenity"="post_office"]',
        '["amenity"="prison"]',
        '["amenity"="ranger_station"]',
        '["amenity"="refugee_site"]',
        '["amenity"="townhall"]'
    ]),
    CategoryQuery("buildings", [OSM_N, OSM_R], [
        '["building"="commercial"]',
        '["building"="industrial"]',
        '["office"]',
        '["building"="warehouse"]',
        '["waterway"="dock"]',
        '["waterway"="boatyard"]',
    ]),
    CategoryQuery("emergency", [OSM_N, OSM_R], [
        '["emergency"="ambulance_station"]',
        '["emergency"="defibrillator"]',
        '["emergency"="landing_site"]'
    ]),
    CategoryQuery("historic", [OSM_N, OSM_W, OSM_R], [
        '["historic"="aqueduct"]',
        '["historic"="battlefield"]',
        '["historic"="building"]',
        '["historic"="castle"]',
        '["historic"="church"]',
        '["historic"="citywalls"]',
        '["historic"="fort"]',
        '["historic"="memorial"]',
        '["historic"="monastery"]',
        '["historic"="monument"]',
        '["historic"="ruins"]',
        '["historic"="tower"]'
    ]),
    CategoryQuery("leisure", [OSM_N, OSM_W, OSM_R], [
        '["leisure"="adult_gaming_centre"]',
        '["leisure"="amusement_arcade"]',
        '["leisure"="beach_resort"]',
        '["leisure"="common"]',
        '["leisure"="dance"]',
        '["leisure"="dog_park"]',
        '["leisure"="escape_game"]',
        '["leisure"="fitness_centre"]',
        '["leisure"="fitness_station"]',
        '["leisure"="garden"]',
        '["leisure"="hackerspace"]',
        '["leisure"="horse_riding"]',
        '["leisure"="ice_rink"]',
        '["leisure"="marina"]',
        '["leisure"="miniature_golf"]',
        '["leisure"="nature_reserve"]',
        '["leisure"="park"]',
        '["leisure"="pitch"]',
        '["leisure"="slipway"]',
        '["leisure"="sports_centre"]',
        '["leisure"="stadium"]',
        '["leisure"="summer_camp"]',
        '["leisure"="swimming_area"]',
        '["leisure"="swimming_pool"]',
        '["leisure"="track"]',
        '["leisure"="water_park"]',
        '["amenity"="public_bath"]',
        '["amenity"="dive_centre"]',
    ]),
    CategoryQuery("shops", [OSM_N, OSM_W, OSM_R], [
        '["shop"]',
    ]),
    CategoryQuery("sport", [OSM_N, OSM_W, OSM_R], [
        '["sport"]',
    ]),
    CategoryQuery("tourism", [OSM_N, OSM_W, OSM_R], [
        '["tourism"]',
    ]),
    CategoryQuery("roads_drive", [OSM_W], [
        '["highway"]["area"!~"yes"]["highway"!~"abandoned|bridleway|construction|corridor|cycleway|elevator|escalator|footway|path|pedestrian|planned|platform|proposed|raceway|service|steps|track"]["motor_vehicle"!~"no"]["motorcar"!~"no"]["service"!~"alley|driveway|emergency_access|parking|parking_aisle|private"]',
    ]),
    CategoryQuery("roads_walk", [OSM_W], [
        '["highway"]["area"!~"yes"]["highway"!~"abandoned|construction|cycleway|motor|planned|platform|proposed|raceway"]["foot"!~"no"]["service"!~"private"]',
    ]),
    CategoryQuery("roads_bike", [OSM_W], [
        '["highway"]["area"!~"yes"]["highway"!~"abandoned|construction|corridor|elevator|escalator|footway|motor|planned|platform|proposed|raceway|steps"]["bicycle"!~"no"]["service"!~"private"]',
    ]),
    CategoryQuery("greenery", [OSM_N, OSM_W, OSM_R], [
        '["landuse"="grass"]',
        '["landuse"="allotments"]',
        '["landuse"="forest"]',
        '["landuse"="flowerbed"]',
        '["landuse"="meadow"]',
        '["landuse"="village_green"]',
        '["natural"="grassland"]',
        '["natural"="scrub"]',
        '["landuse"="garden"]',
        '["leisure"="park"]',
        '["landuse"="recreation_ground"]'
    ]),
]
