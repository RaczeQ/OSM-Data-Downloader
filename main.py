from src.relation import load_area

cities = [
    'Vienna, Austria',
    'Budapest, Hungary',
    'Cork, Ireland',
    'Dublin, Ireland',
    'Milan, Italy',
    'Oslo, Norway',
    'Warsaw, Poland',
    'Greater London, UK',
]

for city in cities:
    relation = load_area(city)
    if relation is not None:
        relation.load_relations_to_file()
