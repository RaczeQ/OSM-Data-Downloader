from src.relation import load_area

cities = [
    'Greater London, UK',
    2604796
]

for city in cities:
    relation = load_area(city)
    if relation is not None:
        relation.load_relations_to_file()
