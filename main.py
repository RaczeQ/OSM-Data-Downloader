from src.relation import load_area

# for city in ["Wrocław, PL"]:
for city in ["Greater London, UK"]:
    relation = load_area(city)
    relation.load_relations_to_mongo()
